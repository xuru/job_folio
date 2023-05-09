# define an alias for the specfic python version used in this file.
FROM python:3.10.11-slim-bullseye as python


# Python build stage
FROM python as python-build-stage

ENV PYTHONDONTWRITEBYTECODE=1
ARG ARG_POETRY_VERSION=1.4.2

# poetry
# https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=${ARG_POETRY_VERSION}
ENV POETRY_VENV="/opt/poetry/venv"
ENV POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# new venv for just poetry, and install poetry with pip; see official doc link
RUN python3 -m venv $POETRY_VENV \
    && ${POETRY_VENV}/bin/pip install --upgrade pip \
    && ${POETRY_VENV}/bin/pip install poetry==${POETRY_VERSION}


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # wait script
    WAIT_VERSION=2.9.0 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VENV="/opt/poetry/venv" \
    POETRY_VIRTUALENVS_PATH="/opt/poetry/virtualenvs" \
    POETRY_NO_INTERACTION=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

ENV PATH=$POETRY_VENV/bin:$PATH
ENV PYTHONPATH=$POETRY_VENV/lib

RUN apt-get update && apt-get install --no-install-recommends -y \
  # To run the Makefile
  make \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # Uncomment below lines to enable Sphinx output to latex and pdf
  # texlive-latex-recommended \
  # texlive-fonts-recommended \
  # texlive-latex-extra \
  # latexmk \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage $POETRY_VENV $POETRY_VENV

# use wheels to install python dependencies
COPY ./poetry.lock* ./pyproject.toml ./
RUN poetry config virtualenvs.path $POETRY_VIRTUALENVS_PATH \
    && poetry install --with docs --no-root --no-cache

COPY ./compose/local/docs/start /start-docs
RUN sed -i 's/\r$//g' /start-docs
RUN chmod +x /start-docs

COPY ./docs /docs
WORKDIR /docs
