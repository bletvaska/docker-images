FROM alpine:latest

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Clock rendered with figlet package"

COPY clock.sh /

RUN apk add figlet

CMD [ "/clock.sh" ]
