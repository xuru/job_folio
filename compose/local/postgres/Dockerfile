FROM postgres:12-alpine
MAINTAINER job_folio <ops@job_folio.us>

COPY --chown=postgres init-user-db.sh /docker-entrypoint-initdb.d/
RUN chown -R postgres. /docker-entrypoint-initdb.d/*
