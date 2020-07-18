FROM scratch

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL version="2020.1"

ADD alpine-minirootfs-3.12.0-x86_64.tar.gz /

COPY template.tpl /opt/
COPY entrypoint.sh /

ENV PS1="\[\e[38;5;5m\]\w\[\e[00m\] $ "

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/sh"]

