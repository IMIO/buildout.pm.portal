py:=2.7
plone:=5.1
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
	if [ -f /usr/bin/virtualenv-2.7 ] ; then virtualenv-2.7 .;else virtualenv -p python$(py) .;fi
	bin/pip install -r requirements.txt

.PHONY: plone-5.1
plone-5.1:
	make cleanall
	make bootstrap plone=5.1
	./bin/buildout -t 30 -c plone-5.1.x.cfg

.PHONY: plone-5.2
plone-5.2:
	make cleanall
	make bootstrap plone=5.2
	./bin/buildout -t 30 -c plone-5.2.x.cfg

.PHONY: docker-image
docker-image: eggs
	docker build --pull -t iadelib/citizenportal:latest .

eggs:  ## Copy eggs from docker image to speed up docker build
	-docker run --entrypoint='' $(IMAGE_NAME) tar -c -C /plone eggs | tar x
	mkdir -p eggs
