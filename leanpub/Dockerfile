#FROM ruby:alpine
FROM ruby:2.7-alpine

#ARG part=1

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL title="LeanPub Powered"
LABEL description="LeanPub heavy powered docker image Courses at Department of Computers and Informatics at Technical University of Košice"

# install pandoc
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk update \
    && apk add pandoc

# install jekyll
RUN apk add make gcc libc-dev g++
RUN gem install jekyll minima webrick jekyll-pandoc paru liquid-cli i18n
#RUN apk del make gcc libc-dev g++

# install theme
COPY jekyll-theme-nucky-2021.1.gem /tmp
RUN gem install --local /tmp/jekyll-theme-nucky-2021.1.gem \
    && rm /tmp/jekyll-theme-nucky-2021.1.gem

#! TODO python, later replacement for pandoc filters in ruby
RUN apk add python3 py3-pip py3-invoke py3-dotenv py3-requests py3-rich gettext zip \
    && pip install panflute==1.12.5 \
    && ln -s /usr/bin/python3 /usr/bin/python

# set timezone
RUN apk add tzdata \
    && cp /usr/share/zoneinfo/Europe/Bratislava /etc/localtime \
    && echo "Europe/Bratislava" > /etc/timezone \
    && apk del tzdata

# to remove
RUN apk add bash curl

# environment variables
ENV JEKYLL_ENV=development
ENV DATADIR=/pandoc
ENV HOME=/courseware

WORKDIR /courseware
EXPOSE 4000

ADD pandoc /pandoc
ADD entrypoint.sh /
ADD tasks.py /

ENTRYPOINT [ "/entrypoint.sh" ]

