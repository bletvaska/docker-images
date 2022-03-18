FROM python:3.9-slim-bullseye AS builder

RUN apt update && apt install -y gcc

RUN pip wheel --wheel-dir /wheels \
    flask-login==0.4.1 \
    python-nvd3==0.15.0 \
    python-slugify==4.0.1 \
    termcolor==1.1.0 \
    unicodecsv==0.14.1 \
    blinker==1.4 \
    Flask-JWT-Extended==3.25.1

FROM python:3.9-slim-bullseye AS main

COPY --from=builder /wheels/ /wheels/

RUN pip install /wheels/* \
    && rm -rf /wheels/ \
    && pip install apache-airflow

ENV AIRFLOW_HOME=/airflow

COPY entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]

VOLUME /airflow
WORKDIR /airflow

CMD [ "airflow", "standalone" ]
