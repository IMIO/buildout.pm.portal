# Changelog

## Release 2.4.13

**Date:** 2026-06-17


### buildout.pm.portal

- Bake the deliberations.be deploy-automation upgrade helpers into the image
  (`scripts/check-pending-upgrades.py`, `scripts/run-upgrades.py`) and remove the
  dead `scripts/run_portal_upgrades.py` (it imported `collective.upgrade`, which
  is not installed in the image). (DELIBE-311)
  [aduchene]

## Release 2.4.12

**Date:** 2026-06-16


### collective.big.bang (1.0.3 → 1.1.0)

#### Version 1.1.0 (2025-10-14)

- Added expansion feature, which allows to perform all pending upgrade steps in one operation.
  [bsuttor]

- Upgrade dev environment to Plone 6.1
  [remdub]

## Release 2.4.11

**Date:** 2026-06-16


### plonetheme.deliberations (1.8 → 1.9)

#### Version 1.9 (2026-06-16)

- On mobile (<768px), pin the fixed PDF viewer toolbar to the top of the
  viewport (``top: 0``) since the navbar is now fixed at the bottom.
  [aduchene]

## Release 2.4.10

**Date:** 2026-06-16


- Pin ``plone.restapi`` to 9.15.6 to address CVE-2026-54503.
  [aduchene]
- Pin ``plone.app.textfield`` to 3.0.2 (Plone 6.1).
  [aduchene]

## Release 2.4.9

**Date:** 2026-06-15


- Docker: register the cron tick idempotently. The entrypoint now overwrites
  the ``imio`` crontab instead of appending to it, so restarting an instance
  (``docker start`` / ``restart: always``) no longer accumulates duplicate
  ``*/15 * * * * /tick.sh`` entries that fire the tick multiple times.
  [aduchene]

## Release 2.4.8

**Date:** 2026-06-15


### plonemeeting.portal.core (2.4.2 → 2.4.3)

#### Version 2.4.3 (2026-06-15)

- Fix typo.
  [aduchene]

## Release 2.4.7

**Date:** 2026-06-15


### plonemeeting.portal.core (2.4.1 → 2.4.2)

#### Version 2.4.2 (2026-06-15)

- Send the ``Last-Modified`` header again on the ``@@custom_colors.css``
  view, so browsers refresh the CSS when an institution changes its colors.
  [DELIBE-306]
  [aduchene]

- Add Plausible web statistics dashboards: a ``@@statistics`` view on each
  institution and a global control panel. The dashboard is shown in an
  iframe; the Plausible site and its shared link are created (or refreshed)
  on each visit, so the dashboard keeps working even if the link is deleted
  or changed on the Plausible side. The Plausible URL, API key and site
  domain are set in the registry, and a clear message is shown when Plausible
  is not reachable. [DELIBE-307]
  [aduchene]

- Add RSS/Atom feeds of the latest decisions and publications. Feeds are
  available on the usual Plone URLs, e.g.
  ``/<institution>/publications/rss.xml``, and list the most recent
  published items first. An upgrade step turns them on for existing
  institutions. [DELIBE-255]
  [aduchene]

- Add a "Remove expiration date" action on publications, for publications
  managers and site administrators. It clears the expiration date while
  keeping the qualified timestamp. Also improve the help text of the
  expiration date field. [DELIBE-305]
  [aduchene]

- Drop support for Python 3.11; require Python >= 3.12 (``python_requires``,
  classifiers and Ruff ``target-version`` updated accordingly).
  [aduchene]

- Adopt Ruff for Python linting/formatting (``pyproject.toml`` ``[tool.ruff]``,
  ``line-length = 120``) and ``zpretty`` for templates/ZCML/XML; drop the old
  ``.flake8`` / ``.isort.cfg`` / ``setup.cfg``. Run on demand via ``make lint``
  (``ruff check``) and ``make format`` (``ruff`` + ``zpretty``) — no pre-commit,
  tox or CI. The codebase is intentionally not reformatted here; run
  ``make format`` to apply it as a dedicated change. [DELIBE-291]
  [aduchene]

- Add a configurable ``website_url`` field on ``Institution`` that keeps a
  published ``Link`` (``website-url``) to the communal website in sync. The
  link is managed from the add/modify event subscribers
  (``sync_website_link``) instead of a property setter, so it no longer
  crashes when the field is set before the institution is added to the
  portal, and clearing the URL removes the link. [DELIBE-112]
  [aduchene]

- Fix test layer: load ``imio.omnia.core``, ``imio.omnia.assistant`` and
  ``imio.omnia.tinymce`` ZCML in ``testing.py`` so the ``:default`` profile
  dependency chain resolves under the test fixture (``z3c.autoinclude`` is
  disabled there).
  [aduchene]
- Remove dead ``get_api_url_for_meeting_item`` (singular) helper from
  ``utils.py`` — orphaned since 2021 with no callers.
  [aduchene]
- Tighten ``.coveragerc`` ``include`` pattern so it matches regardless of
  the cwd from which coverage is invoked.
  [aduchene]
- Add tests for ``PreSyncReportForm._reconcile_items`` /
  ``_reconcile_annexes``, ``ImportMeetingForm`` / ``PreSyncReportForm`` /
  ``PreImportReportForm`` button handlers, the ``sync_meeting``
  orchestrator, ``MeetingAddForm.updateFields``,
  ``MeetingEditForm.handleApply`` / ``handleCancel``, the
  ``validate_no_already_superseded`` schema validator and
  ``SupersedeAdapter.supersedes_items`` / ``has_supersedes_items``, plus
  ``get_api_url_for_presync_meeting_items``. Suite goes 182 → 204 tests;
  application-code coverage 87% → 94%.
  [aduchene]

### plonetheme.deliberations (1.7 → 1.8)

#### Version 1.8 (2026-06-15)

- Style the ``website-url`` navigation item (return link to the
  institution's own website): pushed to the far right on desktop and
  flagged with an outbound-link icon. [DELIBE-112]
  [aduchene]
- Brand the edit toolbar: iMio header with the institution logo (linking
  to the site root) and the navigation-root title (linking to the
  navigation root).
  [aduchene]
- On mobile and tablet (<992px), replace the cramped collapsed toolbar
  with a floating action button that slides the toolbar in as an
  off-canvas left icon-rail.
  [aduchene]
- Host the toolbar template override
  (``plone.app.layout.viewlets.toolbar``) in the theme instead of
  plonemeeting.portal.core.
  [aduchene]
- Give the ``#portal-globalnav`` a top gradient border matching the
  footer.
  [aduchene]
- Style the "Flux RSS" document action as a centered pill button using
  the institution colour.
  [aduchene]
- On mobile and tablet (<992px), replace the offcanvas hamburger menu
  with a fixed bottom tab bar (a Preact component built from the global
  navigation): up to three primary section tabs plus a "Plus" overflow
  popover, the active tab using the per-institution accent colour.
  [aduchene]
- Compact the mobile/tablet header: cap the institution logo height and
  trim the surrounding padding so page content is no longer pushed
  below the fold.
  [aduchene]
- Align the Plausible statistics dashboard (``@@statistics`` /
  ``@@plausible-statistics``) with the site's content container: oversize
  the embed iframe by the dashboard's internal side padding (the
  dashboard's own max-width is lifted through Plausible's embed styles
  injection, see plonemeeting.portal.core). [DELIBE-307]
  [aduchene]

## Release 2.4.1

**Date:** 2026-04-03


### plonemeeting.portal.core (2.4.0 → 2.4.1)

#### Version 2.4.1 (2026-04-03)

- Enable AI assistant on ``Item`` (Decision) content type in addition to ``Publication``.
  [aduchene]

## Release 2.4.0

**Date:** 2026-04-03


### plonemeeting.portal.core (2.3.2 → 2.4.0)

#### Version 2.4.0 (2026-04-03)

- Integrate ``imio.omnia.core``, ``imio.omnia.assistant`` and ``imio.omnia.tinymce`` as dependencies.
  [aduchene]
- Add ``enable_ai_assistant`` and ``ai_assistant_system_prompt`` fields to ``Institution`` (new AI fieldset).
  [aduchene]
- Implement ``AssistantAdapter``: assistant only available on ``Publication`` content type
  when ``enable_ai_assistant`` is enabled on the institution.
  [aduchene]
- Implement ``OrganizationIDProvider``: resolves the organization ID from the institution
  containing the current publication.
  [aduchene]
- Grant ``Anonymous`` role access to ``@@omnia-assistant-api`` so the assistant works
  on public publication pages.
  [aduchene]
- Add upgrade step to 2400: installs the three omnia add-ons and re-imports ``typeinfo``
  and ``rolemap``.
  [aduchene]

## Release 2.3.3

**Date:** 2026-01-28


### plonemeeting.portal.core (2.3.1 → 2.3.2)

#### Version 2.3.2 (2026-01-28)

- DELIBE-152: Improve i18n translations.
  [aduchene]

### plonetheme.deliberations (1.6 → 1.7)

#### Version 1.7 (2026-01-28)

- Minor changes regarding some z-index issues.
  [aduchene]

## Release 2.3.2

**Date:** 2026-01-19


### imio.webspellchecker (1.0b7 → 1.2)

#### Version 1.2 (2026-01-19)

- Use defer `<script>`'s attribute so it doesn't block the whole page in case the service isn't responding.
  [aduchene]

#### Version 1.1 (2025-07-11)

- Fixed installation by renaming the `base` profile to `install-base` so it is
  no more alphabetically before `default`.
  Removed `metadata.xml` from the `install-base` profile.
  [gbastien, aduchene]

## Release 2.3.1

**Date:** 2025-12-10


### plonemeeting.portal.core (2.3.0 → 2.3.1)

#### Version 2.3.1 (2025-12-10)

- Fix `publication_workflow` perms and guards.
  [aduchene]
- Fix upgrade step to 2300.
  [aduchene]

### plonetheme.deliberations (1.5 → 1.6)

#### Version 1.6 (2025-12-10)

- Minor tweaks.
  [aduchene]

## Release 2.3.0

**Date:** 2025-12-09


### plonemeeting.portal.core (2.2.6 → 2.3.0)

#### Version 2.3.0 (2025-12-09)

- DELIBE-256: Patch `Products.CMFPlone.resources.utils.get_resource` to disable useless verbose logger
  when getting a resource.
  [aduchene]
- DELIBE-152: Add new state `archived` to `publication_workflow` and allow institution manager to archive publications.
  [aduchene]
- DELIBE-152: Add 2 new groups `*-publications-creators` and `*-publications-reviewer`
  for each institution to manage publication creation and review.
  [aduchene]
- DELIBE-152: Add new state `proposed` to `publication_workflow` and allow creators to propose publications for review.
  [aduchene]
- DELIBE-152: Add new `Supersede` behavior to `Publication` content type to manage publication versions.
  [aduchene]
- Reorder fiels and fieldsets on `Institution`.
  [aduchene]
- New overridable translations to keep them when updating the translations to ease navigation on the page.
  [aduchene]
- Begin implementation of a generic table of contents for publications.
  [aduchene]
- Refactor how review_state is displayed and translated across the package.
  [aduchene]
- Refactor forms to use the same `BaseAddForm` and `BaseEditForm` for content types.
  Allowing to sort fieldsets and to hide some fieldsets to non plone site administrators.
  [aduchene]
- Add 2 configurable default texts on `Institution` to be used on when a new publication is created:
  `default_publication_consultation_text`, `default_publication_text`.
  [aduchene]
- Add new field `archived_publication_warning_text` on `Institution` to display
  a warning message on archived publications.
  [aduchene]
- Add a configurable default text on `Institution` to be used on when a new meeting is imported:
  `default_meeting_custom_info`.
  [aduchene]
- DELIBE-58: Order global categories on faceted views too.
  [aduchene]
- Add a base `PlonemeetingMigrator` class to ease future migrations.
  [aduchene]
- Improve login page.
  [aduchene]

### plonetheme.deliberations (1.4 → 1.5)

#### Version 1.5 (2025-12-09)

- Theming for login page, publication timeline, publication related items.
  [aduchene]

## Release 2.2.7

**Date:** 2026-01-19


### imio.webspellchecker (1.0b7 → 1.2)

#### Version 1.2 (2026-01-19)

- Use defer `<script>`'s attribute so it doesn't block the whole page in case the service isn't responding.
  [aduchene]

#### Version 1.1 (2025-07-11)

- Fixed installation by renaming the `base` profile to `install-base` so it is
  no more alphabetically before `default`.
  Removed `metadata.xml` from the `install-base` profile.
  [gbastien, aduchene]

## Release 2.2.6

**Date:** 2025-12-11


### plonemeeting.portal.core (2.2.5 → 2.2.6)

#### Version 2.2.6 (2025-12-11)

- Sort publications on effective date and sortable_title on faceted view.
  [aduchene]

## Release 2.2.5

**Date:** 2025-10-24


### plonemeeting.portal.core (2.2.4 → 2.2.5)

#### Version 2.2.5 (2025-10-24)

- Remove `x-twitter` in `site_socials` actions.
  [aduchene]
- SUP-48246: Human sort `global_categories` and `document_types` vocabularies.
  [aduchene]
- Add a new values for `document_types` vocabulary.
  [aduchene]

## Release 2.2.4

**Date:** 2025-10-21


### plonemeeting.portal.core (2.2.3 → 2.2.4)

#### Version 2.2.4 (2025-10-21)

- Inherit of `DXDocumentGenerationHelperView` instead of `DocumentGenerationHelperView`
  in `docgen.PMDocumentGenerationHelperView`.
  [aduchene]

## Release 2.2.3

**Date:** 2025-09-12


### plonemeeting.portal.core (2.2.2 → 2.2.3)

#### Version 2.2.3 (2025-09-12)

- Fix an issue with `get_contentbrowser_options`.
  [aduchene]

## Release 2.2.2

**Date:** 2025-09-12


### plonemeeting.portal.core (2.2.1 → 2.2.2)

#### Version 2.2.2 (2025-09-12)

- Fix an issue in `InstitutionTemplatesVocabularyFactory`.
  [aduchene]
- Fix an issue in `event.check_publication_timestamp`.
  [aduchene]

## Release 2.2.1

**Date:** 2025-09-10


### plonemeeting.portal.core (2.1.12 → 2.2.1)

#### Version 2.2.1 (2025-09-10)

- Integrate collective.documentgenerator to generate a documents from content types.
  [aduchene]
- Add default templates for `Publication` to be used by collective.documentgenerator.
  [aduchene]
- Add missing plone.icons to content types.
  [aduchene]

#### Version 2.2.0 (2025-09-08)

- DELIBE-251: New timestamping format (ASiC) for publications, combining the archive and the timestamp in a single file.
  [aduchene]
- DELIBE-228: Add a new JS form to validate the new publication timestamping format.
  [aduchene]
- Adapt `publication.pt` to include new timestamping format.
  [aduchene]

### plonetheme.deliberations (1.3 → 1.4)

#### Version 1.4 (2025-09-08)

- Re-release.
  [aduchene]

### collective.timestamp (1.3 → 1.5)

#### Version 1.5 (2025-09-10)

- Properly translate labels in `TimestampInfo`.
  [aduchene]

#### Version 1.4 (2025-08-26)

- Add a new view `TimestampInfo` to have more info about the timestamp that can also be used as an util view.
  [aduchene]

## Release 2.1.13

**Date:** 2025-07-01


### plonemeeting.portal.core (2.1.11 → 2.1.12)

#### Version 2.1.12 (2025-07-01)

- DELIBE-245: timestamp invalidation overhaul.
  [aduchene]
- Change the map center offset to be more centered on the institution.
  [aduchene]
- Make the PDF Viewer displaying pages in full width by default.
  [aduchene]
- Remove the the `get_resource` patch.
  [aduchene]
- DELIBE-249: Allow to directly publish a publication in private state with an effective date.
  [aduchene]

## Release 2.1.12

**Date:** 2025-06-23


### collective.timestamp (1.2 → 1.3)

#### Version 1.3 (2025-06-23)

- Avoid modifying list passed as argument in `utils.timestamp`.
  [aduchene]

## Release 2.1.10

**Date:** 2025-06-19


### plonemeeting.portal.core (2.1.10 → 2.1.11)

#### Version 2.1.11 (2025-06-19)

- Fix an issue with `publication.EditForm`.
  [aduchene]

## Release 2.1.9

**Date:** 2025-06-19


### plonemeeting.portal.core (2.1.9 → 2.1.10)

#### Version 2.1.10 (2025-06-19)

- Prevent Editor to edit a publication in planned state.
  [aduchene]
- Move table_of_contents field to the general fieldset.
  [aduchene]
- Prevent and show an error message when a publication effective date is removed in planned state.
  [aduchene]
- Add missing translations.
  [aduchene]

### collective.timestamp (1.0a2 → 1.2)

#### Version 1.2 (2025-06-19)

- Fixed a bug with `utils.timestamp` stuck in an infinite loop when use_failover was False.
  [aduchene]
- Changed default values of `ITimestampingSettings` and set required fields.
  [aduchene]

#### Version 1.1 (2025-06-19)

- Fix a bug with TimeStamper.timestamp not returning the correct value.
  [aduchene]

## Release 2.1.8

**Date:** 2025-06-12


### plonemeeting.portal.core (2.1.7 → 2.1.9)

#### Version 2.1.9 (2025-06-12)

- Fix bad release.
  [aduchene]

#### Version 2.1.8 (2025-06-12)

- Fix wrong permission in `preview_meeting.pt`.
  [aduchene]
- DELIBE-111: Add a warning message to the publication manager if the publication date is in the past.
  [aduchene]
- DELIBE-206: Add `webstats_js` field on Institution and override AnalyticsViewlet to use it.
  [aduchene]
- DELIBE-237: Fix no effective date when timestamping was disabled.
  [aduchene]

## Release 2.1.7

**Date:** 2025-05-19


### plonemeeting.portal.core (2.1.6 → 2.1.7)

#### Version 2.1.7 (2025-05-19)

- DELIBE-224: Fix file upload issue in the rich text editot's content browser.
  [aduchene]

## Release 2.1.6

**Date:** 2025-05-14


### plonemeeting.portal.core (2.1.5 → 2.1.6)

#### Version 2.1.6 (2025-05-14)

- DELIBE-221: Fix an permission issue with the "Add meeting" button in the faceted view.
  [aduchene]
- DELIBE-223: Fix bleeding groups from other institutions in manage-edit-user view.
  [aduchene]
- Add a back button to the File view.
  [aduchene]
- Refactor and extract annexes into macros.
  [aduchene]

### plonetheme.deliberations (1.2 → 1.3)

#### Version 1.3 (2025-09-08)

- Floating buttons in forms.
  [aduchene]
- Theming about timestamping form.
  [aduchene]

## Release 2.1.5

**Date:** 2025-05-12


### plonemeeting.portal.core (2.1.4 → 2.1.5)

#### Version 2.1.5 (2025-05-12)

- DELIBE-222: Fix an issue regarding the last Contentbrowser changes.
  [aduchene]

## Release 2.1.4

**Date:** 2025-05-06


### plonemeeting.portal.core (2.1.2 → 2.1.4)

#### Version 2.1.4 (2025-05-06)

- Change default timestamping service in default profile.
  [aduchene]
- Make sure Contentbrowser is using the navigation root as rootPath.
  [aduchene]

## Release 2.1.3

**Date:** 2025-04-30


### plonemeeting.portal.core (2.1.1 → 2.1.2)

#### Version 2.1.2 (2025-04-30)

- DELIBE-199: Users are now manageable by institution.
  [aduchene]
- DELIBE-199: Add new member and manager groups for each institution.
  [aduchene]
- DELIBE-199: New institution settings navigation tab and view.
  [aduchene]

### plonetheme.deliberations (1.1 → 1.2)

#### Version 1.2 (2025-04-30)

- Manage institution theming.
  [aduchene]

## Release 2.1.1

**Date:** 2025-03-21


### plonemeeting.portal.core (2.1.0 → 2.1.1)

#### Version 2.1.1 (2025-03-21)

- DELIBE-23/DELIBE-206: Complete the upgrade step 2100.
  [aduchene]
- DELIBE-24: Fix an issue where a decisions manager could not remove items from a meeting.
  [aduchene]
- Handle multiple possible cron paths in the Prometheus export view.
  [aduchene]

### plonetheme.deliberations (1.0 → 1.1)

#### Version 1.1 (2025-03-04)

- Misc. fixes and tweaks.
  [aduchene]

## Release 2.1.0

**Date:** 2025-02-28


### plonemeeting.portal.core (2.0.5 → 2.1.0)

#### Version 2.1.0 (2025-02-28)

- DELIBE-196: Plone 6.1 compatibility.
  [aduchene]
- DELIBE-23/DELIBE-206: Uninstall collective.cookiecuttr.
  [aduchene]

#### Version 2.0.6 (unreleased)

- DELIBE-186: Add a new Prometheus export view `prometheus-export` to monitor cron.
  [aduchene]
- Complete tests about `MeetingAgendaAPIView`.
  [aduchene]
- Rename `institution_locations` view name to `institution-locations`.
  [aduchene]

## Release 2.0.6

**Date:** 2024-12-19


### plonemeeting.portal.core (2.0.4 → 2.0.5)

#### Version 2.0.5 (2024-12-19)

- DELIBE-12: Avoid a "@@confirm-action" on `Institution` creation.
  [aduchene]
- DELIBE-29: Add ZoomControl back on institutions map
  [aduchene]
- DELIBE-180: Fix some issues when an `Institution.representatives_mappings` could be None.
  [aduchene]

## Release 2.0.5

**Date:** 2024-10-23


### plonemeeting.portal.core (2.0.3 → 2.0.4)

#### Version 2.0.4 (2024-10-23)

- DELIB-11: Fixed an issue with next/prev navigation on `ItemView` when items are not in correct order
  in the meeting folder.
  [aduchene]
- DELIBE-3: Add meeting date in the title of `PreSyncForm` and `PreImportForm`.
  [aduchene]

## Release 2.0.4

**Date:** 2024-10-11


### collective.timestamp (1.0a1 → 1.0a2)

*No changelog entries found.*

## Release 2.0.3

**Date:** 2024-10-10


### plonemeeting.portal.core (2.0.2 → 2.0.3)

#### Version 2.0.3 (2024-10-10)

- Removed ipdb.
  [aduchene]

## Release 2.0.2

**Date:** 2024-10-08


### plonemeeting.portal.core (2.0.1 → 2.0.2)

#### Version 2.0.2 (2024-10-08)

- Fixed call to `@@update_meeting` and `@@force_reimport_meeting` that was broken
  because we were passing the `decisions` folder instead the `Institution`.
  [gbastien]
- Fixed issue in pre-sync form when an item is removed and classifier field is used.
  [aduchene]
- Fixed issue with anonymous that could not download the timestamp field on `Publication`.
  [aduchene]

## Release 2.0.1

**Date:** 2024-10-02


### plonemeeting.portal.core (2.0.0 → 2.0.1)

#### Version 2.0.1 (2024-10-02)

- Fixed wrong link on `preview_meeting.pt`.
  [aduchene]
- Adapted `meeting_workflow` so `Editor` may change a meeting `review_state`
  and not only the `Owner`.  `Owner` is not more managed by `meeting_workflow`.
  Fix meeting `review_state` could not be changed by another user than the `Owner`.
  [gbastien]
- Fixed publication effective date not reindexed after publish.
- Splitted `avis` `document_type` in 3 `document_types`
  (`avis`, `avis-enquete-publique` and `avis-reunion-information`),
  `avis` `id` kept for backward compatibility for publications already created.

#### Version 2.0.0b1 (2024-09-17)

- Plone 6 compatibility.
  [aduchene]
- Theme extracted to `plonetheme.deliberations` package.
  [aduchene]
- Use latest Python 3.12 and Plone 6.0.13.
  [aduchene]
- "Publications" feature :

  - Rename "meetings" folder to "decisions".
  - Use `collective.autopublishing` to manage automatic publishing of publications.
  - Use `collective.timestamp` to manage publication timestamping.
  - Use `imio.webspellchecker` to have better webspellchecking.
  - Add `Publication` content type.
  - Add `Publication` views and faceted navigation.
  - Add custom workflows to manage publications and folders.
  - Add new groups `*-publications-manager` for each institution to manage publications.
  - Add some unit tests about the feature.
  - Add an upgrade step to migrate meetings and items in decisions folder.
  - Miscellaneous fixes and tweaks to make it work nicely.

  [gbastien, laulaz, aduchene]

### plonetheme.deliberations (1.0b1 → 1.0)
  - Plone 6 ready.
    [aduchene]
  - publications theming.
    [aduchene]
