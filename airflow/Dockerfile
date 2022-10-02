# FROM bletvaska/python
FROM python:3.10-slim

LABEL maintainer="mirek <mirek@cnl.sk>"

# create user
RUN useradd \
    --user-group \
    --password pythonista \
    --uid 1000 \
    -m \
    pythonista

# install main packages
RUN apt update \
    && apt -y install curl \
    && python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir apache-airflow \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSO https://starship.rs/install.sh \
    && sh ./install.sh -y \
    && rm install.sh

# prepare entrypoint
COPY entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

VOLUME /airflow
WORKDIR /airflow
USER pythonista
EXPOSE 8080

# environment variables
ENV AIRFLOW_HOME=/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=False

# configuration
COPY --chown=pythonista starship.toml /home/pythonista/.config/starship.toml
RUN echo 'eval "$(starship init bash)"' >> /home/pythonista/.bashrc \
    && echo 'PATH=/home/pythonista/.local/bin:$PATH' >> /home/pythonista/.bashrc

CMD [ "airflow", "standalone" ]

