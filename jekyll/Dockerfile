FROM alpine:3.23

LABEL authors="mirek <mirek@cnl.sk>"
LABEL description="Docker image for building and serving Jekyll static sites"
LABEL source="https://github.com/bletvaska/docker-images"

RUN addgroup publisher \
    && adduser --disabled-password --ingroup publisher publisher

RUN apk --no-cache add ruby ruby-dev ruby-bundler build-base make

ENV BUNDLE_PATH="/web/vendor/bundle"

WORKDIR "/web"

COPY app /app

EXPOSE 5000

USER publisher

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD [ "make", "help" ]

