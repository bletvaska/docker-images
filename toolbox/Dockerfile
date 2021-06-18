FROM scratch
ADD alpine-minirootfs-3.14.0-x86_64.tar.gz /
CMD [ "/bin/sh" ]

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Set of Linux Tools for container management and testing."

RUN apk update \
    && apk add curl iputils nmap wget mtr stress-ng
