FROM debian:trixie-slim

LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL title="LeanPub Powered"
LABEL description="LeanPub heavy powered docker image Courses at Department of Computers and Informatics at Technical University of Košice"

# pandoc-crossref releases are only published in lockstep with a specific
# pandoc version, so both are pinned together and installed from upstream
# instead of apt (Debian trixie's packaged pandoc, 3.1.11, predates every
# available pandoc-crossref release).
ARG PANDOC_VERSION=3.10.1
ARG PANDOC_CROSSREF_VERSION=0.3.25

# Debian trixie ships just 1.40.0; the [arg(...)] attribute used for
# long-form recipe flags needs 1.46.0+, so just is pinned from upstream too.
ARG JUST_VERSION=1.58.0

# set timezone
RUN cp /usr/share/zoneinfo/Europe/Bratislava /etc/localtime \
    && echo "Europe/Bratislava" > /etc/timezone

# without a locale, Ruby's default external encoding is US-ASCII, which
# crashes on any UTF-8 content (Slovak diacritics included); C.UTF-8 is
# built into glibc, no locale-gen/locales package needed
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# jekyll (and ruby) come straight from Debian; the plugin gems below are
# pure-ruby, so no compiler toolchain is needed
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        jekyll \
        ca-certificates \
        curl \
        xz-utils \
        zip \
        python3 \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN gem install --no-document jekyll-pandoc paru minima webrick

# pandoc, pandoc-crossref and just, pinned upstream binaries
# (bounded per-attempt timeout + retries so a stalled connection fails
# instead of hanging forever; -C - resumes each retry instead of
# restarting the download from zero on a slow connection)
RUN curl_fetch="curl -fsSL -C - --connect-timeout 10 --max-time 300 --retry 5 --retry-delay 5" \
    && ${curl_fetch} -o /tmp/pandoc.tar.gz \
        "https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-linux-amd64.tar.gz" \
    && tar -xzf /tmp/pandoc.tar.gz -C /usr/local --strip-components=1 \
    && rm /tmp/pandoc.tar.gz \
    && ${curl_fetch} -o /tmp/pandoc-crossref.tar.xz \
        "https://github.com/lierdakil/pandoc-crossref/releases/download/v${PANDOC_CROSSREF_VERSION}/pandoc-crossref-Linux-X64.tar.xz" \
    && tar -xJf /tmp/pandoc-crossref.tar.xz -C /usr/local/bin pandoc-crossref \
    && rm /tmp/pandoc-crossref.tar.xz \
    && ${curl_fetch} -o /tmp/just.tar.gz \
        "https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-x86_64-unknown-linux-musl.tar.gz" \
    && tar -xzf /tmp/just.tar.gz -C /usr/local/bin just \
    && rm /tmp/just.tar.gz

# install theme
COPY jekyll-theme-nucky/ /tmp/jekyll-theme-nucky/
RUN cd /tmp/jekyll-theme-nucky \
    && gem build jekyll-theme-nucky.gemspec \
    && gem install --local jekyll-theme-nucky-2026.09.gem \
    && rm -rf /tmp/jekyll-theme-nucky

# python toolchain used by tasks.py (invoke)
# Debian marks the system python as externally managed (PEP 668), so
# dependencies live in a dedicated venv instead of a plain `pip install`
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
ENV PATH="/opt/venv/bin:${PATH}"

# experimental - texlive support (texmf is part of app/, copied below)
ENV TEXMFHOME=/app/texmf

# environment variables
ENV JEKYLL_ENV=development
# lets pandoc resolve --defaults/--csl/--template by bare name from
# /app/pandoc/{defaults,csl,templates}/, no full path needed
ENV XDG_DATA_HOME=/app
# to avoid saving user specific files to project files
ENV HOME=/tmp

WORKDIR /courseware
EXPOSE 4000

# everything the image itself contributes (as opposed to the courseware
# mounted at /courseware) lives together under /app; the app/ folder of
# this repository is its exact copy
COPY app/ /app/

# version of the image, shown by `just versions`; a release build passes it
# explicitly (docker build --build-arg VERSION=2026.9.4 -t ...:2026.9.4 .),
# a plain `docker build` is marked as "dev". It is declared last so changing
# it does not invalidate the cached layers above.
ARG VERSION=dev
ENV LEANPUB_VERSION=${VERSION}
LABEL version="${VERSION}"

ENTRYPOINT [ "/app/entrypoint.sh" ]
