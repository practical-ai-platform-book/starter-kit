FROM python:3.9.10

SHELL ["/bin/bash", "-o", "pipefail", "-o", "xtrace", "-c"]

RUN : Set timezone to JST \
        && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && : Install poetry \
        && curl -sfL 'https://install.python-poetry.org' | python

ENV PATH $PATH:/root/.local/bin

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN : Install dependencies \
        && poetry config virtualenvs.create false \
        && poetry install --no-dev

COPY . .
