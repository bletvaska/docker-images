FROM bletvaska/python

LABEL maintainer="mirek <mirek@cnl.sk>"

# RUN usermod -l airflow pythonista

RUN python -m pip install --upgrade pip \
    && pip install apache-airflow

ENV AIRFLOW_HOME=/airflow

COPY entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

VOLUME /airflow
WORKDIR /airflow
# USER airflow
EXPOSE 8080

CMD [ "airflow", "standalone" ]
