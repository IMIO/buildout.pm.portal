#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Run every pending GenericSetup upgrade step for the Plone site(s), then commit.
#   ./bin/instance run scripts/run-upgrades.py
import os
import transaction
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_base
from Testing.makerequest import makerequest
from zope.component.hooks import setSite


def iter_plone_sites(app):
    site_id = os.environ.get('SITE_ID')
    if site_id and site_id in app.objectIds():
        yield app[site_id]
        return
    for obj in app.objectValues():
        if hasattr(aq_base(obj), 'portal_setup'):
            yield obj


def become_admin(app):
    # Mirror collective.big.bang: run as the Zope root 'admin' (Manager
    # everywhere) so upgrade steps that check permissions succeed.
    user = app.acl_users.getUser('admin')
    if user is not None:
        newSecurityManager(None, user.__of__(app.acl_users))


def upgrade_site(portal):
    setSite(portal)
    setup = portal.portal_setup
    profiles = list(setup.listProfilesWithPendingUpgrades())
    for profile_id in profiles:
        setup.upgradeProfile(profile_id)
        print('UPGRADED=%s' % profile_id)
    return len(profiles)


def main(app):
    app = makerequest(app)
    become_admin(app)
    total = 0
    for portal in iter_plone_sites(app):
        total += upgrade_site(portal)
    transaction.commit()
    print('UPGRADED_PROFILES=%d' % total)


if __name__ == '__main__':
    main(app)  # noqa: F821 - `app` is injected by `bin/instance run`
