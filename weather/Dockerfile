FROM python:3.11-slim-bullseye AS builder

RUN apt update \
    && apt upgrade \
    && /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir /wheels/ \
    && cd /wheels/

COPY dist/*whl /wheels/

RUN pip wheel --wheel-dir=/wheels/ \
    weather-2023.1-py3-none-any.whl


FROM python:3.11-slim-bullseye AS base
LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Simple weather checker as simple app example for Docker 101 course."

COPY --from=builder /wheels/*whl /tmp/

RUN adduser --no-create-home --disabled-password --gecos "" mrilko \
    && mkdir /app && chown mrilko.mrilko /app \
    && cd /tmp/ \
    && apt update \
    && apt upgrade \
    && apt install -y --no-install-recommends procps \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip install *whl \
    && pip cache purge \
    && rm -rf *whl

HEALTHCHECK --interval=15s --timeout=3s --retries=3 --start-period=5s \
  CMD http --check-status get http://localhost:8000/healthz || exit 1


USER mrilko

EXPOSE 8000

WORKDIR /app

VOLUME [ "/app/templates" ]  # , "./config", "./measurements", "cache" ]

CMD [ "weather" ]
