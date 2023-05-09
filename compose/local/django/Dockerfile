ARG PYTHON_VERSION=3.10.10-slim-bullseye
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ARG ARG_POETRY_VERSION=1.4.2

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Set configuration
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # wait script
    WAIT_VERSION=2.9.0 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=${ARG_POETRY_VERSION} \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    SETUP_PATH="/opt/setup"

ENV PATH=$POETRY_HOME/bin:$PATH

##############################################################################
# This stage is used to install dependencies and build the environment
##############################################################################
FROM python as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  zsh \
  curl \
  build-essential \
  libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR ${SETUP_PATH}

COPY ./poetry.lock* ./pyproject.toml ./
RUN pip install --upgrade pip setuptools \
    && curl -sSL https://install.python-poetry.org | python - \
    && ${POETRY_HOME}/bin/poetry export --with dev,test,lint -o requirements.txt --without-hashes \
    && pip wheel --wheel-dir ${SETUP_PATH}/wheels -r requirements.txt

# see: https://github.com/ufoscout/docker-compose-wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# see: https://github.com/ufoscout/docker-compose-wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=wedge:wedge --from=python-build-stage ${SETUP_PATH}/wheels  /wheels/
COPY --chown=wedge:wedge --from=python-build-stage ${POETRY_HOME} ${POETRY_HOME}/
COPY --chown=wedge:wedge --from=python-build-stage /wait /wait

# use wheels to install python dependencies
COPY ./poetry.lock* ./pyproject.toml ./
RUN poetry config virtualenvs.path $POETRY_VIRTUALENVS_PATH \
    && poetry install --with dev,test,lint --no-root --no-cache

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && pip install superfsmon \
    && rm -rf /wheels

# copy application code to WORKDIR
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
