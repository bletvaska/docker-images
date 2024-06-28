# RAMBO Images

Simple web application written in awesome FastAPI for my Docker and Kubernetes courses.

Metadata about movies are stolen from http://www.omdbapi.com.

## Building Images

```bash
# build python package first
poetry build

# build them all
for part in {1..5}; do
  docker buildx build --build-arg RAMBO_PART="${part}"  --tag bletvaska/rambo:"${part}" --file Dockerfile.slim .
done

# tag them one by one
docker image tag bletvaska/rambo:1 bletvaska/rambo:1982
docker image tag bletvaska/rambo:2 bletvaska/rambo:1985
docker image tag bletvaska/rambo:3 bletvaska/rambo:1988
docker image tag bletvaska/rambo:4 bletvaska/rambo:2008
docker image tag bletvaska/rambo:5 bletvaska/rambo:2019

# publish to hub.docker.com
docker image push bletvaska/rambo --all-tags
```

## Environment Variables

* `TZ` - sets the container timezone
