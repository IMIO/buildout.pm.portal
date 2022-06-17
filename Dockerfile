FROM imiobe/plone-base:5.2.8-alpine as builder

COPY --chown=imio scripts /plone/scripts/
COPY --chown=imio *.cfg requirements.txt /plone/

WORKDIR /plone

RUN apk add --update --no-cache --virtual .build-deps \
  build-base \
  gcc \
  git \
  libc-dev \
  libffi-dev \
  libjpeg-turbo-dev \
  libpng-dev \
  libwebp-dev \
  libxml2-dev \
  libxslt-dev \
  openssl-dev \
  pcre-dev \
  wget \
  zlib-dev \
  && pip install -r requirements.txt \
  && su -c "buildout -vvv -c prod.cfg" -s /bin/sh imio

FROM imiobe/plone-base:5.2.8-alpine

ENV PLONE_MAJOR=5.2 \
  PLONE_VERSION=5.2.8 \
  TZ=Europe/Brussel \
  ZEO_HOST=db \
  ZEO_PORT=8100 \
  HOSTNAME_HOST=local \
  PROJECT_ID=imio \
  SMTP_QUEUE_DIRECTORY=/data/queue

LABEL plone=$PLONE_VERSION \
  os="alpine" \
  name="Plone $PLONE_VERSION" \
  description="Plone image for PM Citizen Portal" \
  maintainer="Imio"

COPY --chown=imio --from=builder /plone /plone
COPY --chown=imio docker-initialize.py docker-entrypoint.sh /

RUN pip install -r requirements.txt

USER imio
VOLUME /data/blobstorage
VOLUME /data/filestorage
WORKDIR /plone
EXPOSE 8081
HEALTHCHECK --interval=1m --timeout=5s --start-period=45s \
  CMD nc -z -w5 127.0.0.1 8081 || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["start"]