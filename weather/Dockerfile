FROM python:3.10-slim-bullseye AS builder

RUN apt update \
    && apt upgrade \
    && /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir /wheels/ \
    && cd /wheels/

COPY dist/*whl /wheels/

RUN pip wheel --wheel-dir=/wheels/ \
        weather-1.0.0-py3-none-any.whl


FROM python:3.10-slim-bullseye AS base
LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Simple weather checker as simple app example for Docker 101 course."

COPY --from=builder /wheels/*whl /tmp/

RUN adduser --no-create-home --disabled-password --gecos "" mrilko \
    && cd /tmp/ \
    && apt update \
    && apt upgrade \
    && apt install -y procps \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip install *whl \
    && pip cache purge \
    && rm -rf *whl

USER mrilko

CMD [ "weather" ]