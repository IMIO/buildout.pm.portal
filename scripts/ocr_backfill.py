"""
Generate the text version of the PDF file of the existing publications.

The script sends the PDF file of each publication to the Omnia OCR API and
stores the text that comes back. It skips a publication without a PDF file
and a publication whose text version is up to date, so a second run
continues the work of the first one. It tries a failed generation again.

Dry run by default. Without --commit, nothing is written and the OCR is not
called.

Timestamp guard: the generation must not change a publication. Before the
generation, the script records for each publication of a batch the digest of
the timestamp token, the digest of the timestamped archive, the digest of the
content that a timestamp covers, the modification date, the children and the
catalog values. It compares them before the commit of the batch. If a value
is different, it aborts the transaction, prints the publication and exits
with an error status.

After --max-failures failures in a row, the script removes the failures of
this row from the current batch, commits the rest and exits with an error
status. A write conflict rolls back the current batch: run the script again.

Usage:
    bin/instance run scripts/ocr_backfill.py (<institution> | --all)
        [--site conseil] [--commit] [--states published,archived]
        [--batch 10] [--limit N] [--force] [--max-failures 5]
"""

from collections import Counter
from collective.timestamp.interfaces import ITimeStamper
from hashlib import sha256
from imio.omnia.ocr import api as ocr_api
from imio.omnia.ocr.config import STATUS_DONE
from imio.omnia.ocr.config import STATUS_FAILED
from io import BytesIO
from plone.browserlayer.layer import mark_layer
from Products.CMFCore.indexing import processQueue
from Testing.makerequest import makerequest
from ZODB.POSException import ConflictError
from zope.component.hooks import setSite
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest
from zope.traversing.interfaces import BeforeTraverseEvent

import argparse
import sys
import time
import transaction
import zipfile


CHUNK_SIZE = 1 << 20


def file_digest(value):
    """Return the SHA-256 hex digest of a file field value. Return None when there is no file."""
    if value is None:
        return None
    digest = sha256()
    if hasattr(value, "open"):
        with value.open("r") as handle:
            for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
                digest.update(chunk)
    else:
        digest.update(value.data)
    return digest.hexdigest()


def archive_digest(obj):
    """Return a digest of the content that a timestamp of ``obj`` covers.

    The bytes of the archive hold the time of its creation. The digest uses
    the names and the content of the files in the archive.
    """
    digest = sha256()
    with zipfile.ZipFile(BytesIO(ITimeStamper(obj).get_data())) as archive:
        for name in sorted(archive.namelist()):
            digest.update(name.encode("utf-8"))
            digest.update(sha256(archive.read(name)).digest())
    return digest.hexdigest()


def snapshot(obj, catalog):
    """Return the values of ``obj`` that the generation must not change."""
    rid = catalog.getrid("/".join(obj.getPhysicalPath()))
    indexes = catalog.getIndexDataForRID(rid) if rid is not None else {}
    metadata = catalog.getMetadataForRID(rid) if rid is not None else {}
    return {
        "timestamp token": file_digest(obj.timestamp),
        "timestamped archive": file_digest(obj.timestamped_file),
        "content that a timestamp covers": archive_digest(obj),
        "modification date": obj.modified().ISO8601(),
        "children": tuple(obj.objectIds()),
        "is_timestamped": ITimeStamper(obj).is_timestamped(),
        "is_timestamped in the catalog": (indexes.get("is_timestamped"), metadata.get("is_timestamped")),
        "modification date in the catalog": str(indexes.get("modified")),
    }


def check_guard(guarded, catalog):
    """Return the differences between the recorded values and the current values.

    ``guarded`` is a list of (object, recorded values).
    The result is a list of (path, name of the value, before, after).
    """
    # The catalog gets the pending index operations before the comparison.
    processQueue()
    differences = []
    for obj, before in guarded:
        after = snapshot(obj, catalog)
        for name, value in before.items():
            if after[name] != value:
                differences.append(("/".join(obj.getPhysicalPath()), name, value, after[name]))
    return differences


def needs_text(text, force):
    """Return the reason to generate the text version. Return None when the publication is skipped."""
    if force:
        return "forced"
    if not text.exists():
        return "no text version"
    if text.is_stale():
        return "PDF file changed"
    if text.status == STATUS_DONE:
        return None
    return text.status


def main(app):
    try:
        idx = next(i for i, a in enumerate(sys.argv) if a.endswith(".py"))
        script_args = sys.argv[idx + 1:]
    except StopIteration:
        script_args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Generate the text version of the PDF file of the publications.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("institution", nargs="?")
    target.add_argument("--all", action="store_true", help="Work on all institutions of the site.")
    parser.add_argument("--site", default="conseil")
    parser.add_argument("--commit", action="store_true", help="Call the OCR and store the text versions.")
    parser.add_argument("--states", default="published,archived",
                        help="Workflow states of the publications, separated by commas.")
    parser.add_argument("--batch", type=int, default=10, help="Number of generations for each commit.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of generations of this run.")
    parser.add_argument("--force", action="store_true", help="Also generate again the text versions that are done.")
    parser.add_argument("--max-failures", type=int, default=5,
                        help="Stop after this number of failures in a row.")
    args = parser.parse_args(script_args)
    if args.batch < 1 or args.max_failures < 1 or (args.limit is not None and args.limit < 1):
        sys.exit("Error: --batch, --limit and --max-failures must be 1 or more.")

    site = app.get(args.site)
    if site is None:
        sys.exit(f"Error: site '{args.site}' not found.")
    setSite(site)
    # The catalog indexers of the portal use views. The request needs the browser layers of the site.
    request = getRequest()
    if request is None:
        request = makerequest(app).REQUEST
        setRequest(request)
    mark_layer(site, BeforeTraverseEvent(site, request))

    if args.all:
        insts = [o for o in site.objectValues() if getattr(o, "portal_type", None) == "Institution"]
    else:
        inst = site.get(args.institution)
        if inst is None or getattr(inst, "portal_type", None) != "Institution":
            sys.exit(f"Error: institution '{args.institution}' not found in '{args.site}'.")
        insts = [inst]

    states = [state.strip() for state in args.states.split(",") if state.strip()]
    tool = site.portal_catalog
    catalog = tool._catalog
    brains = tool.unrestrictedSearchResults(
        portal_type="Publication",
        review_state=states,
        path=["/".join(i.getPhysicalPath()) for i in insts],
        sort_on="path",
    )

    # Find the publications to process.
    todo = []
    skipped = Counter()
    reasons = Counter()
    per_group = Counter()
    for brain in brains:
        obj = brain._unrestrictedGetObject()
        text = ocr_api.get_text(obj)
        if text is None:
            sys.exit("Error: the publications do not have the imio.omnia.ocr behavior. Run the upgrade steps first.")
        if not text.is_supported():
            skipped["no PDF file"] += 1
            continue
        reason = needs_text(text, args.force)
        if reason is None:
            skipped["text version up to date"] += 1
            continue
        institution_id = brain.getPath().split("/")[2]
        todo.append((brain.getPath(), institution_id, brain.review_state))
        reasons[reason] += 1
        per_group[(institution_id, brain.review_state)] += 1

    print(f"Site: {args.site}. Institutions: {len(insts)}. States: {', '.join(states)}.")
    print(f"Publications found: {len(brains)}")
    print(f"  to process:                       {len(todo)}")
    for reason, count in sorted(reasons.items()):
        print(f"    {reason}: {count}")
    print(f"  skipped, no PDF file:             {skipped['no PDF file']}")
    print(f"  skipped, text version up to date: {skipped['text version up to date']}")
    if per_group:
        print("To process, for each institution and state:")
        for (institution_id, state), count in sorted(per_group.items()):
            print(f"  {institution_id:<30} {state:<12} {count}")
    if args.limit is not None and args.limit < len(todo):
        print(f"This run stops after {args.limit} generation(s) (--limit).")
        todo = todo[:args.limit]

    if not args.commit:
        print("Dry run. Nothing changed and the OCR was not called. Use --commit to apply.")
        return
    if not todo:
        print("Nothing to process.")
        return
    if not ocr_api.get_setting("enabled"):
        sys.exit("Error: the generation is disabled in the OCR settings of the site.")

    start = time.monotonic()
    done = failed = pages = checked = checked_timestamped = 0
    failures_in_a_row = 0
    stopped = False

    def commit_batch(guarded):
        """Compare the guarded values, then commit. Exit when a value changed."""
        nonlocal checked, checked_timestamped
        differences = check_guard(guarded, catalog)
        if differences:
            transaction.abort()
            print("TIMESTAMP GUARD: the generation changed a protected value. The batch is rolled back.")
            for path, name, before, after in differences:
                print(f"  {path}")
                print(f"    {name}: {before!r} -> {after!r}")
            sys.exit(1)
        try:
            transaction.commit()
        except ConflictError:
            transaction.abort()
            sys.exit("ConflictError: the current batch is rolled back. Run the script again to continue.")
        checked += len(guarded)
        checked_timestamped += sum(1 for _obj, before in guarded if before["timestamp token"])
        print(f"  batch committed: {len(guarded)} publication(s) checked by the timestamp guard, no change")
        # Free the memory of the batch.
        site._p_jar.cacheMinimize()

    guarded = []
    batch_results = []
    row_savepoint = None
    for number, (path, _institution_id, _state) in enumerate(todo, 1):
        obj = site.unrestrictedTraverse(path)
        text = ocr_api.get_text(obj)
        guarded.append((obj, snapshot(obj, catalog)))
        savepoint = transaction.savepoint()
        began = time.monotonic()
        # Without force, a failure stays a failure.
        status = ocr_api.process(obj, force=args.force or text.status == STATUS_FAILED)
        seconds = time.monotonic() - began
        print(f"  [{number}/{len(todo)}] {path}: {status}, {text.page_count} page(s), {seconds:.1f} s")
        batch_results.append((status, text.page_count))
        if status == STATUS_FAILED:
            if failures_in_a_row == 0 or row_savepoint is None:
                row_savepoint = (savepoint, len(batch_results) - 1)
            failures_in_a_row += 1
            if failures_in_a_row >= args.max_failures:
                # The API is probably down. These publications must not stay failed.
                row_savepoint[0].rollback()
                del batch_results[row_savepoint[1]:]
                stopped = True
        else:
            failures_in_a_row = 0
            row_savepoint = None
        if stopped or len(guarded) >= args.batch or number == len(todo):
            commit_batch(guarded)
            done += sum(1 for status, _count in batch_results if status == STATUS_DONE)
            failed += sum(1 for status, _count in batch_results if status == STATUS_FAILED)
            pages += sum(count for status, count in batch_results if status == STATUS_DONE)
            guarded = []
            batch_results = []
            # A savepoint does not live after the commit.
            row_savepoint = None
        if stopped:
            break

    elapsed = time.monotonic() - start
    print(
        f"Summary: {done} done, {failed} failed, "
        f"{skipped['no PDF file'] + skipped['text version up to date']} skipped "
        f"({skipped['no PDF file']} without PDF file, {skipped['text version up to date']} up to date), "
        f"{pages} page(s), {elapsed:.1f} s."
    )
    print(
        f"Timestamp guard: {checked} publication(s) checked, {checked_timestamped} with a timestamp, no change."
    )
    if stopped:
        print(
            f"Stopped: {args.max_failures} failures in a row. The failures of this row in the last batch are "
            "not stored. Check the Omnia API, then run the script again."
        )
        sys.exit(1)
    if failed:
        print("Run the script again to try the failed generations again.")


if "app" in dir():
    main(app)  # noqa: F821
