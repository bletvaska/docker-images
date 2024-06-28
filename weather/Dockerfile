FROM python:3.12-slim-bullseye AS builder

ARG PACKAGE=weather-2024.4-py3-none-any.whl
ARG USER=mrilko

COPY dist/${PACKAGE} /build/

RUN python3 -m venv /venv \
    && /venv/bin/pip3 install --no-cache-dir --upgrade pip /build/${PACKAGE} \
    && pip cache purge

# RUN apt update \
#     && apt upgrade \
#     && apt install -y gcc \
#     && /usr/local/bin/python -m pip install --upgrade pip
#
# RUN mkdir /wheels/ \
#     && cd /wheels/
#
# COPY dist/*whl /wheels/
#
# RUN pip wheel --wheel-dir=/wheels/ \
#     weather-2023.12-py3-none-any.whl
#
#
FROM python:3.12-slim-bullseye AS base
LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Simple weather checker as simple app example for Docker 101 course."
#
COPY --from=builder /venv/ /venv/
ENV PYTHONPATH=/venv/lib/python3.12/site-packages

RUN addgroup ${USER} \
    && adduser --no-create-home --disabled-password --gecos "" --ingroup ${USER} ${USER}
#
# RUN adduser --no-create-home --disabled-password --gecos "" mrilko \
#     && mkdir /app && chown mrilko:mrilko /app \
#     && cd /tmp/ \
#     && apt update \
#     && apt upgrade \
#     && apt install -y --no-install-recommends procps \
#     && /usr/local/bin/python -m pip install --upgrade pip \
#     && pip install *whl \
#     && pip cache purge \
#     && rm -rf *whl
#
#HEALTHCHECK --interval=15s --timeout=3s --retries=3 --start-period=5s \
#  CMD http --check-status get http://localhost:8000/healthz || exit 1
#
USER ${USER}
#
EXPOSE 8000
#
WORKDIR /app
#
# # , "themes", "./config", "./measurements", "cache" ]
VOLUME [ "/app" ]
#
#CMD [ "uvicorn", "weather.app:app", "--log-level", "error", "--host", "0.0.0.0" ]
CMD [ "python", "-m", "weather" ]

