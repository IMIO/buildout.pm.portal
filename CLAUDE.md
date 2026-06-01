# CLAUDE.md - Deliberations.be

## Project overview

**Deliberations.be** (Plonemeeting Portal) - a Plone 6.1 web application for citizens to consult official deliberations and publications from Walloon local authorities (Belgium). Built and maintained by [iMio](https://imio.be).

This repository is the **buildout** (deployment/development harness). The actual application code lives in `src/` as mr.developer checkouts, primarily in `plonemeeting.portal.core`.

## Tech stack

- **Plone 6.1** on **Python 3.12**
- **zc.buildout** for dependency management and instance configuration
- **mr.developer** for source checkouts in `src/`
- ZODB (Data.fs + blobstorage) or optional RelStorage (PostgreSQL)
- Docker deployment via `docker/`

## Repository layout

```
buildout.cfg          # Entry point - extends dev.cfg (or prod.cfg / docker.cfg)
dev.cfg               # Development profile (extends plone-6.1.x.cfg + base.cfg)
prod.cfg              # Production profile (extends Plone release pinnings)
base.cfg              # Shared: eggs, zcml, instance recipe
sources.cfg           # mr.developer source repos (GitHub IMIO / collective)
versions.cfg          # Pinned package versions
port.cfg              # Network ports and DB credentials
docker.cfg            # Docker-specific buildout profile
bldr.toml             # bldr release tool config (changelog, versioning)
Makefile              # bootstrap, buildout, test, run, docker-image
src/                  # mr.developer source checkouts (gitignored except content)
  plonemeeting.portal.core/   # Main application package
  plonetheme.deliberations/   # Plone theme
  collective.documentgenerator/
  collective.timestamp/
  collective.autopublishing/
  imio.ai.core/         # Local develop egg
  imio.helpers/
  imio.pyutils/
  imio.webspellchecker/
var/                  # Runtime data (Data.fs, blobstorage, logs)
```

## Common commands

```bash
# Bootstrap from scratch
make bootstrap          # creates venv + installs buildout
bin/buildout            # runs buildout (or: make buildout for full clean rebuild)

# Run
bin/instance fg         # start Plone in foreground (http://localhost:8080)
make run                # same thing

# Tests
bin/test                # run tests (defaults to plonemeeting.portal.core)
make test               # same (runs buildout first if needed)

# Code analysis
bin/code-analysis       # run all static checks
bin/code-analysis-flake8

# Coverage
bin/coverage            # run tests with coverage
bin/report              # generate HTML coverage report
```

## Buildout configuration

The `buildout.cfg` entry point selects which profile to extend:
- **dev.cfg** (default) - development with auto-checkout, iw.debug, QA tools
- **prod.cfg** - production with Plone release pinnings, prometheus monitoring
- **docker.cfg** - Docker deployment extending prod + zeo

Key settings in `dev.cfg`:
- `auto-checkout` lists packages that are checked out as source in `src/`
- `always-checkout = true` keeps source checkouts up to date
- `allow-picked-versions = true` for development flexibility

## Git workflow — IMPORTANT

Each `src/<package>` is its **own** git repo (and `src/` is gitignored by
the buildout). Commit application-code changes from inside the package
repo — `git -C src/<package> ...` — on its own branch. **Never `git add
-A` from the buildout root for package work**: it stages unrelated
buildout files and misses the gitignored package changes. The buildout
repo only owns harness files (`*.cfg`, `Makefile`, `docker/`, `CLAUDE.md`…).

## Code style

- **flake8**: max-line-length 120, ignore E501/W503/E203 (see `.flake8`)
- Follow Plone coding standards
- Python packages use `setup.cfg` / `setup.py` conventions

## Key packages

| Package | Role |
|---|---|
| `plonemeeting.portal.core` | Main application logic, views, content types |
| `plonetheme.deliberations` | Diazo theme for the citizen portal |
| `collective.documentgenerator` | Document generation (appy/LibreOffice) |
| `collective.timestamp` | eIDAS qualified timestamps for publications |
| `collective.autopublishing` | Automated content publishing workflows |
| `imio.webspellchecker` | Spell-checking integration |
| `imio.helpers` / `imio.pyutils` | Shared iMio utility libraries |
| `imio.ai.core` | AI integration (local develop egg) |

## Release workflow

Releases are managed with **bldr** (see `bldr.toml`):
- Bumps versions in `versions.cfg` and `publiccode.yml`
- Generates consolidated `CHANGELOG.md` from sub-package changelogs
- Creates GitHub releases with tag

## Notes

- Default admin credentials for dev: `admin:admin` (see `port.cfg`)
- Dev instance runs on port **8080** (base.cfg), prod on **8081** (port.cfg), debug on **8089**
- The `src/` directory is gitignored; packages are cloned by mr.developer on `bin/buildout`
- `imio.ai.core` in `src/` is a local `develop =` egg, not an mr.developer checkout
