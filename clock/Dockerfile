FROM alpine:latest

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Clock rendered with figlet package"

#ADD alpine-minirootfs-3.12.0-x86_64.tar.gz / 
COPY clock.sh /

RUN apk add figlet

CMD [ "/clock.sh" ]
