#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Prints "PENDING=<n>" — the number of proposed GenericSetup upgrade steps for
# the Plone site(s) in this instance. Run inside an instance container:
#   ./bin/instance run check-pending-upgrades.py
#
# The target site is taken from the SITE_ID env var (set in the compose for the
# instance); if absent or not found, every Plone site under the Zope root is
# summed. We deliberately do NOT read sys.argv: `bin/instance run` does not pass
# script arguments through cleanly (the interpreter's own -c leaks in).
import os
from Acquisition import aq_base


def iter_plone_sites(app):
    site_id = os.environ.get('SITE_ID')
    if site_id and site_id in app.objectIds():
        yield app[site_id]
        return
    for obj in app.objectValues():
        if hasattr(aq_base(obj), 'portal_setup'):
            yield obj


def count_pending(setup):
    pending = 0
    try:
        profiles = setup.listProfilesWithPendingUpgrades()
    except AttributeError:
        profiles = [p['id'] for p in setup.listProfileInfo()]
    for profile_id in profiles:
        try:
            steps = setup.listUpgrades(profile_id)
        except (KeyError, AttributeError):
            continue
        for entry in steps:
            group = entry if isinstance(entry, list) else [entry]
            pending += sum(1 for s in group if s.get('proposed', True))
    return pending


def main(app):
    total = 0
    for portal in iter_plone_sites(app):
        total += count_pending(portal.portal_setup)
    print('PENDING=%d' % total)


if __name__ == '__main__':
    main(app)  # noqa: F821 - `app` is injected by `bin/instance run`
