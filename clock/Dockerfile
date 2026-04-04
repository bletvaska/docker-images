FROM alpine:3.21

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Clock rendered with figlet package"

COPY clock.sh /

RUN apk add --no-cache \
    figlet=~2.2 \
    ncurses=~6.5

CMD [ "/clock.sh" ]
