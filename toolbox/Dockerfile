FROM alpine

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL description="Set of Linux Tools for container management and testing."
LABEL dockerhub="https://hub.docker.com/r/bletvaska/toolbox"
LABEL github="https://github.com/bletvaska/docker-images/tree/master/toolbox"

# todo: do we need git? 
RUN apk update \
    && apk add --no-cache \
        bash \
        curl \
        docker-cli \
        httpie \
        iputils \
        jq \
        mtr \
        ncurses \
        nmap \
        py3-setuptools \
        py3-jsonschema \
        shellcheck \
        sqlite \
        stress-ng \
        tmux \
        vim \
        wget \
        yq \
    && apk add --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
        bats \
        sqlmap

# install dgoss
RUN curl -fsSL https://goss.rocks/install | sh

# create home environment
ENV HOME="/home"
RUN mkdir /home/work
WORKDIR /home/work

ADD vimrc /home/.vimrc
ADD bashrc /home/.bashrc

# add bats libs into /tools folder
# download and unzip bats libraries
RUN mkdir -p /tools/libs/ \
    && cd /tools/libs \
    && wget https://github.com/ztombol/bats-support/archive/refs/heads/master.zip \
    && unzip master.zip \
    && rm master.zip \
    && mv bats-support-master bats-support \
    && wget https://github.com/ztombol/bats-assert/archive/refs/heads/master.zip \
    && unzip master.zip \
    && rm master.zip \
    && mv bats-assert-master bats-assert
#ADD libs/ /tools/

CMD [ "/bin/bash" ]

