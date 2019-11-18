all: dev

.PHONY: dev
dev:
	ln -fs dev.cfg buildout.cfg
	if [ -f /usr/bin/virtualenv-2.7 ] ; then virtualenv-2.7 .;else virtualenv -p python2.7 .;fi
	./bin/pip install -r requirements.txt
	./bin/buildout -t 30

run: bin/instance
	bin/instance fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg pip-selfcheck.json
