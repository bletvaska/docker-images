#!/usr/bin/env bash


if [ "$1" = 'airflow' ]; then
    # check if db is initialized
    airflow db check-migrations || {
        airflow db init
        airflow users create \
            --username admin \
            --password admin \
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
