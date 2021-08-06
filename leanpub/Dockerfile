FROM alpine
#FROM ruby:2.7-alpine

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL title="LeanPub Powered"
LABEL description="LeanPub heavy powered docker image Courses at Department of Computers and Informatics at Technical University of Košice"

# set timezone
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Europe/Bratislava /etc/localtime \
    && echo "Europe/Bratislava" > /etc/timezone \
    && apk del tzdata

# install pandoc and jekyll
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk update \
    && apk add --no-cache pandoc jekyll

# install packages for jekyll
RUN apk add --no-cache make gcc libc-dev g++
RUN gem install jekyll-pandoc paru minima
RUN apk del make gcc libc-dev g++

# install theme
COPY jekyll-theme-nucky/ /tmp/jekyll-theme-nucky/
RUN ls /tmp \
    && cd /tmp/jekyll-theme-nucky \
    && gem build jekyll-theme-nucky.gemspec \
    && gem install --local jekyll-theme-nucky-2021.2.gem \
    && rm -rf /tmp/jekyll-theme-nucky

#! TODO python, later replacement for pandoc filters in ruby
# gettext zip
RUN apk add --no-cache python3 py3-pip py3-dotenv py3-requests py3-rich py3-jinja2 \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && pip install --no-cache-dir panflute invoke pydantic python-frontmatter

# experimental - texlive support
RUN apk add --no-cache texlive
ENV TEXMFHOME=/texmf
COPY texmf/ /texmf/

# invoke needs bash
# curl
RUN apk add --no-cache bash vim

# environment variables
ENV JEKYLL_ENV=development
ENV DATADIR=/pandoc
# to avoid saving user specific files to project files
ENV HOME=/tmp

WORKDIR /courseware
EXPOSE 4000

ADD pandoc /pandoc
ADD entrypoint.sh /
ADD tasks.py /

ENTRYPOINT [ "/entrypoint.sh" ]

