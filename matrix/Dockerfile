FROM scratch

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Matrix screen saver in console"

ADD alpine-minirootfs-3.12.0-x86_64.tar.gz / 

RUN apk add cmatrix

CMD [ "cmatrix" ]
