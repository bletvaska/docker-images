FROM debian:11-slim
#FROM ruby:2.7-alpine

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL title="LeanPub Powered"
LABEL description="LeanPub heavy powered docker image Courses at Department of Computers and Informatics at Technical University of Košice"
LABEL version="2022.10"

# set timezone
RUN cp /usr/share/zoneinfo/Europe/Bratislava /etc/localtime \
    && echo "Europe/Bratislava" > /etc/timezone

# install pandoc and jekyll
RUN apt update
    #&& apt install pandoc jekyll

# install packages for jekyll
#RUN apk add --no-cache make gcc libc-dev g++ ruby-dev
#RUN gem install jekyll-pandoc paru minima webrick
#RUN apk del make gcc libc-dev g++ ruby-dev

##! TODO python, later replacement for pandoc filters in ruby
## gettext zip
#RUN apk add --no-cache python3 py3-pip py3-dotenv py3-requests py3-rich py3-jinja2 \
    #&& pip install --no-cache-dir panflute invoke pydantic python-frontmatter
    ## && ln -s /usr/bin/python3 /usr/bin/python \

## invoke needs bash
## zip and curl for deployment
#RUN apk add --no-cache bash # vim zip curl

## install theme
#COPY jekyll-theme-nucky/ /tmp/jekyll-theme-nucky/
#RUN cd /tmp/jekyll-theme-nucky \
    #&& gem build jekyll-theme-nucky.gemspec \
    #&& gem install --local jekyll-theme-nucky-2022.10.gem \
    #&& rm -rf /tmp/jekyll-theme-nucky

## experimental - texlive support
## RUN apk add --no-cache texlive
#ENV TEXMFHOME=/texmf
#COPY texmf/ /texmf/

## environment variables
#ENV JEKYLL_ENV=development
#ENV DATADIR=/pandoc
## to avoid saving user specific files to project files
#ENV HOME=/tmp

#WORKDIR /courseware
#EXPOSE 4000

#ADD pandoc /pandoc
#ADD entrypoint.sh /
#ADD tasks.py /

#ENTRYPOINT [ "/entrypoint.sh" ]

