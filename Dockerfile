FROM python:3.9.13

ARG ENVIRONMENT=default

ENV PYTHONUNBUFFERED 1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=1


WORKDIR /app

COPY requirements/*.txt /tmp/requirements/

RUN set -x \
  && buildDeps=" \
  build-essential \
  " \
  && runDeps=" \
  git \
  " \
  && localDeps=" \
  telnet \
  " \
  && apt-get update \
  && apt-get install -y --no-install-recommends $buildDeps \
  && apt-get install -y --no-install-recommends $runDeps \
  && if [ $ENVIRONMENT = local ] || [ $ENVIRONMENT = development ]; then \
  apt-get install -y --no-install-recommends $localDeps \
  # Install python dev dependencies
  && pip install -r /tmp/requirements/local.txt; \
  else \
  # Install python production dependencies
  pip install -r /tmp/requirements/production.txt; \
  # other environment to local remove the build dependencies
  apt-get remove -y $buildDeps; \
  fi \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  # clean tmp dir
  && rm -rf /tmp/*

COPY . .

CMD [ "python","manage.py","runserver","0.0.0.0:8000" ]
