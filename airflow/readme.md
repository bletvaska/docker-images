# Apacha Airflow Mini

This is my mini *Docker* image for my [Apache Airflow](https://airflow.apache.org/) course. It is created only from basic installation and configuration and by default it is running as `standalone`.


## Tags

* [latest](https://github.com/bletvaska/docker-images/blob/master/airflow/Dockerfile)


## Running the Airflow

Recommended way of running the image:

```bash
$ docker container run --rm \
  --name airflow \
  --publish 8080:8080 \
  --volume /path/to/your/airflow/home/folder:/airflow \
  airflow
```


## If you need additional packages

Create the file `requirements.txt` in your `airflow` directory. When you will be running the container, the packages from this file will be installed automatically.


## Environment Variables

This image uses several environment variables:

* `AIRFLOW_USER_ID` - The ID of the user the Airflow will run. This is useful to set the ID of your local user just to avoid the issues with the files, which will Airflow create. Default value is set to `1000`.
* `AIRFLOW_USER` - The username to access the Web UI.
* `AIRFLOW_PASSWORD` - The password to access the WEB UI.
