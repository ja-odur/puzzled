## base image
FROM python:3.7-slim-buster AS python-node-base

## For archived debian images
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/deb.debian.org/s|buster-updates|buster|g' /etc/apt/sources.list

## Install node 20
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
    apt install -y nodejs && apt-get clean

## install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq5 \
    build-essential \
    zlib1g-dev curl  && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


## dependency image
FROM python-node-base AS build-requirements

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
ARG NODE_ROOT=/root/node_dependencies
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


## add and install python requirements
RUN pip install --upgrade pip && pip install pipenv

ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv sync


## add and install node requirements
RUN mkdir $NODE_ROOT
ADD package.json $NODE_ROOT
WORKDIR $NODE_ROOT

RUN npm install

RUN apt-get -y purge gcc && apt-get clean

## build-image
FROM python-node-base

# MAINTAINER Odur Joseph <odurjoseph8@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG VIRTUAL_ENV=/opt/venv
ARG NODE_ROOT=/root/node_dependencies
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ARG HOME='/app'

## Copy Python and Node dependencies from dependency image
COPY --from=build-requirements $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=build-requirements $NODE_ROOT/node_modules $HOME/node_modules

WORKDIR $HOME
ADD . $HOME/

COPY --from=build-requirements ./Pipfile.lock $HOME/

ENV DJANGO_SETTINGS_MODULE backend.settings

ENV PATH="${PATH}:${HOME}/node_modules/.bin"

ENV NODE_OPTIONS=--openssl-legacy-provider

EXPOSE 3000 8000
