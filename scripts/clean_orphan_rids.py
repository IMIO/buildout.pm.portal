"""
Find and remove orphan rids in the portal_catalog.

An orphan rid has a record in the catalog "data" or "paths", but no entry of
"uids" points to it. The catalog cannot remove or update such a record by path.

Dry run by default. Nothing is written without --commit.

Usage:
    bin/instance run scripts/clean_orphan_rids.py [--site conseil] [--commit]
        [--batch 500]
"""

from collections import Counter
from ZODB.POSException import ConflictError
from zope.component.hooks import setSite

import argparse
import sys
import transaction


def find_orphans(cat):
    """Return the sorted rids that are in data or paths but not in uids."""
    known = set(cat.uids.values())
    return sorted((set(cat.data.keys()) | set(cat.paths.keys())) - known)


def find_lost_uids(uid_idx):
    """Return (uid, rid) for each record whose UID has no entry in the UID index.

    The index refuses a UID that a different record holds. The record then
    keeps its UID in the reverse map only.
    """
    return [(uid, rid) for rid, uid in uid_idx._unindex.items() if uid not in uid_idx._index]


def remove_rid(cat, rid):
    """Remove the record of p_rid from the indexes, the data and the paths."""
    for name in cat.indexes.keys():
        index = cat.getIndex(name)
        if hasattr(index, "unindex_object"):
            index.unindex_object(rid)
    if rid in cat.data:
        del cat.data[rid]
        cat._length.change(-1)
    cat.paths.pop(rid, None)


def main(app):
    try:
        idx = next(i for i, a in enumerate(sys.argv) if a.endswith(".py"))
        script_args = sys.argv[idx + 1:]
    except StopIteration:
        script_args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Remove orphan rids from portal_catalog.")
    parser.add_argument("--site", default="conseil")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--batch", type=int, default=500)
    args = parser.parse_args(script_args)

    site = app.get(args.site)
    if site is None:
        sys.exit(f"Error: site '{args.site}' not found.")
    setSite(site)

    tool = site.portal_catalog
    cat = tool._catalog
    uid_idx = cat.getIndex("UID")

    orphans = find_orphans(cat)
    dangling = [(path, rid) for path, rid in cat.uids.items() if rid not in cat.data or rid not in cat.paths]

    print(f"Catalog records: {len(cat.data)} data, {len(cat.paths)} paths, {len(cat.uids)} uids")
    print(f"Orphan rids: {len(orphans)}")
    print(f"uids entries without data or paths: {len(dangling)}")
    for path, rid in dangling[:30]:
        print(f"    dangling: {rid} {path}")

    per_institution = Counter()
    holders = 0
    for rid in orphans:
        path = cat.paths.get(rid)
        uid = uid_idx._unindex.get(rid)
        live_rid = cat.uids.get(path) if path else None
        holds_uid = uid is not None and uid_idx._index.get(uid) == rid
        holders += holds_uid and live_rid is not None
        parts = (path or "").split("/")
        per_institution[parts[2] if len(parts) > 2 else "?"] += 1
        print(
            f"    rid {rid}: path={path} in_data={rid in cat.data} uid={uid} "
            f"holds_uid={holds_uid} live_rid={live_rid}"
        )
    for inst_id, count in per_institution.most_common():
        print(f"  {inst_id}: {count}")
    lost = find_lost_uids(uid_idx)
    print(f"Records with a UID that the UID index lost: {len(lost)}")
    print(f"Orphans that hold the UID of a live record: {holders}")

    if not args.commit:
        print("Dry run. Nothing changed. Use --commit to apply.")
        return
    if not orphans and not lost:
        print("Nothing to do.")
        return

    try:
        for n, rid in enumerate(orphans, 1):
            remove_rid(cat, rid)
            if n % args.batch == 0:
                transaction.commit()
                print(f"  {n}/{len(orphans)} removed and committed")
        transaction.commit()
        # The removal of an orphan also removes the UID that it holds.
        # Give that UID back to the live record.
        lost = find_lost_uids(uid_idx)
        for uid, rid in lost:
            path = cat.paths.get(rid)
            obj = site.unrestrictedTraverse(path, None) if path else None
            # Do not give the UID to a record that has no object.
            if obj is not None and "/".join(obj.getPhysicalPath()) == path:
                uid_idx.insertForwardIndexEntry(uid, rid)
        transaction.commit()
    except ConflictError:
        transaction.abort()
        sys.exit("ConflictError: the current batch is rolled back. Run the script again to continue.")

    print(f"Done: {len(orphans)} removed, {len(lost)} UID restored.")
    print(f"Check: {len(find_orphans(cat))} orphan rids left, {len(find_lost_uids(uid_idx))} lost UID left (expected 0).")


if "app" in dir():
    main(app)  # noqa: F821
