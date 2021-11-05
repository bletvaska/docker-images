FROM alpine

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Set of Linux Tools for container management and testing."
LABEL dockerhub="https://hub.docker.com/r/bletvaska/toolbox"
LABEL github="https://github.com/bletvaska/docker-images/tree/master/toolbox"

RUN apk update \
    && apk add \
        bash \
        bats \
        curl \
        git \
        httpie \
        iputils \
        jq \
        mtr \
        nmap \
        shellcheck \
        sqlite \
        stress-ng \
        vim \
        wget \
        ncurses \
        py3-setuptools \
        py3-jsonschema \
        yq 

# create home environment
ENV HOME="/home"
RUN mkdir /home/work
WORKDIR /home/work

ADD vimrc /home/.vimrc
ADD bashrc /home/.bashrc

# add bats libs into /tools forlder
RUN mkdir /tools
ADD libs/ /tools/

CMD [ "/bin/bash" ]
