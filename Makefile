IMAGE_NAME="docker-staging.imio.be/iadelib/citizenportal:latest"
BUILD_NUMBER ?= local

# plonemeeting.portal.core owns its linting/formatting via plone.meta (ruff).
CORE_DIR = src/plonemeeting.portal.core

all: dev

.PHONY: buildout
buildout:
	make cleanall
	make bootstrap
	bin/pip install -U pip
	bin/pip install -r requirements.txt
	bin/buildout

.PHONY: test
test:dev
	bin/test

.PHONY: run
run:
	bin/instance fg

# Lint/format the core package without leaving the buildout root.
# Delegates to the package's make targets, which run ruff & zpretty directly
# (requires `ruff` & `zpretty` on PATH: `pipx install ruff zpretty`).
.PHONY: lint
lint:
	$(MAKE) -C $(CORE_DIR) lint

.PHONY: format
format:
	$(MAKE) -C $(CORE_DIR) format

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg pip-selfcheck.json local .git/hooks/pre-commit

.PHONY: bootstrap
bootstrap:
	python3.12 -m venv .
	bin/pip install -r requirements.txt

.PHONY: docker-image
docker-image:
	docker build --no-cache --pull -f docker/Dockerfile --build-arg build_number=$(BUILD_NUMBER) -t iadelib/citizenportal:latest .
