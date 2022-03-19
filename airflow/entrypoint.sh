#!/usr/bin/env bash


# runtime Python package installations
if [[ -f /airflow/requirements.txt ]]; then
    echo "Installing additional packages based on requirements.txt file:"
    cat /airflow/requirements.txt
    echo 
    pip install -r /airflow/requirements.txt
fi


# init environment
if [[ "$1" = 'airflow' ]]; then
    # check if db is initialized
    airflow db check-migrations 2> /dev/null || {
        airflow db init
        airflow users create \
            --username "${AIRFLOW_USER:-admin}" \
            --password "${AIRFLOW_PASSWORD:-admin}" \
            --firstname John \
            --lastname Doe \
            --role Admin \
            --email john.doe@gmail.com
    }

    # check if airflow folders exists
    [[ -d /airflow/dags ]] || mkdir /airflow/dags
    [[ -d /airflow/plugins ]] || mkdir /airflow/plugins
fi


# exec
exec "$@"
