# build: docker buildx build --build-arg RAMBO_PART=3  --tag bletvaska/rambo:3 .
# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
FROM python:3.11-slim as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root


FROM gcr.io/distroless/python3-debian12 as runtime

ENV VIRTUAL_ENV=/app/.venv
ENV PYTHONPATH="${VIRTUAL_ENV}/lib/python3.11/site-packages"
ARG RAMBO_PART=1
ENV RAMBO_PART=${RAMBO_PART}

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY rambo /app/rambo

WORKDIR /app

EXPOSE 8000

CMD ["-m", "uvicorn", "rambo.app:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["-m", "rambo"]
