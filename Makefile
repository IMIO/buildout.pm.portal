py:=3.7
IMAGE_NAME="docker-staging.imio.be/iadelib/citizenportal:latest"

all: dev

.PHONY: dev
dev:
	ln -fs dev.cfg buildout.cfg
	if ! test -f bin/buildout;then make bootstrap;fi
	bin/buildout -t 30

.PHONY: test
test:dev
	bin/test

.PHONY: run
run:
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg pip-selfcheck.json local

.PHONY: bootstrap
bootstrap:
	virtualenv -p python$(py) .
	bin/pip install -r requirements.txt

.PHONY: docker-image
docker-image:
	make eggs
	docker build --no-cache --pull -t iadelib/citizenportal:latest .

.PHONY: eggs
eggs:  ## Copy eggs from docker image to speed up docker build
	rm -Rf eggs
	mkdir -p eggs
	# docker run --entrypoint='' $(IMAGE_NAME) tar -c -C /plone eggs | tar x

