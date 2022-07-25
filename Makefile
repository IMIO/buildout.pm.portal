IMAGE_NAME="docker-staging.imio.be/iadelib/citizenportal:latest"

all: dev

.PHONY: dev
dev:
	make cleanall
	ln -fs dev.cfg buildout.cfg
	make bootstrap
	bin/pip install -U pip
	bin/pip install -r requirements.txt
	bin/buildout

.PHONY: prod
prod:
	make cleanall
	ln -fs prod.cfg buildout.cfg
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

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg pip-selfcheck.json local .git/hooks/pre-commit

.PHONY: bootstrap
bootstrap:
	python3.8 -m venv .
	bin/pip install -r requirements.txt

.PHONY: docker-image
docker-image:
	docker build --no-cache --pull -t iadelib/citizenportal:latest .
