FROM harbor.imio.be/common/plone-base:6.1.2 AS builder

ENV ZC_BUILDOUT=4.1.4 \
    PLONE_MAJOR=6.1 \
    PLONE_VERSION=6.1.2

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  gcc \
  git \
  libbz2-dev \
  libc6-dev \
  libffi-dev \
  libjpeg62-dev \
  libopenjp2-7-dev \
  libmemcached-dev \
  libpcre3-dev \
  libpq-dev \
  libreadline-dev \
  libssl-dev \
  libxml2-dev \
  libxslt1-dev \
  python3-dev \
  python3.12-venv \
  python3-pip \
  wget \
  zlib1g-dev \
  && pip3 install --no-cache-dir --break-system-packages zc.buildout==$ZC_BUILDOUT py-spy

USER imio
WORKDIR /plone

RUN python3 -m venv /plone
COPY --chown=imio requirements.txt /plone
RUN /plone/bin/pip install -r requirements.txt \
    && /plone/bin/pip install py-spy

COPY --chown=imio *.cfg /plone/
COPY --chown=imio scripts /plone/scripts

RUN /plone/bin/buildout -c docker.cfg -t 30 -N

#
#FROM ubuntu:24.04 AS uno_src
#RUN apt-get update && apt-get install -y --no-install-recommends \
#      python3.12 python3-uno libreoffice-core \
#  && rm -rf /var/lib/apt/lists/*


FROM harbor.imio.be/common/plone-base:6.1.2
ARG build_number
ENV ZC_BUILDOUT=4.1.4 \
  PLONE_VERSION=6.1.0 \
  HOSTNAME_HOST=local \
  PROJECT_ID=delib \
  PLONE_EXTENSION_IDS=plone.app.caching:default,plonetheme.barceloneta:default,plonemeeting.portal.core:default \
  DEFAULT_LANGUAGE=fr

VOLUME /data/blobstorage
WORKDIR /plone

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
  cron \
  libjpeg62 \
  libmemcached11 \
  libopenjp2-7 \
  libpq5 \
  libtiff6 \
  libxml2 \
  libxslt1.1 \
  lynx \
  netcat-openbsd \
  python3-uno \
  poppler-utils \
  rsync \
  wget \
  wv \
  zint \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN curl -L https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_amd64.deb > /tmp/dumb-init.deb \
 && dpkg -i /tmp/dumb-init.deb && rm /tmp/dumb-init.deb
COPY --chown=imio --from=builder /plone /plone
COPY --from=builder /usr/local/bin/py-spy /usr/local/bin/py-spy
COPY --chown=imio docker/docker-initialize.py docker/docker-entrypoint.sh docker/cron.sh docker/tick.sh /

#COPY --from=uno_src /usr/lib/python3/dist-packages/uno.py /usr/lib/python3/dist-packages/uno.py
#COPY --from=uno_src /usr/lib/python3/dist-packages/unohelper.py /usr/lib/python3/dist-packages/unohelper.py
#COPY --from=uno_src /usr/lib/libreoffice/program /usr/lib/libreoffice/program

# Ensure UNO_PATH is set to where libreoffice is installed
ENV UNO_PATH=/usr/lib/libreoffice/program

# Allow imio to create a cron job
RUN touch /etc/cron.d/plone-tick \
    && crontab -u imio /etc/cron.d/plone-tick \
    && chmod u+s /usr/sbin/cron

RUN echo $build_number > .build_number

# Make the venv first on PATH at runtime
ENV PATH="/plone/bin:${PATH}"

USER imio
EXPOSE 8081
HEALTHCHECK --interval=15s --timeout=10s --start-period=20s --retries=5 \
  CMD wget -q http://127.0.0.1:8081/ok -O - | grep OK || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["console"]
