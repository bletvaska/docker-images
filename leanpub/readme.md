# Lean Publishing Toolbox for My Courses at KPI

Image for building my courses, which are written with [Jekyll](https://jekyllrb.com) - static site generator.

For generating is used `pandoc` instead of built in `kramdown` and won theme `nucky` is also builtin in the image.

External projects:

* [Pandoc Crossref](https://github.com/lierdakil/pandoc-crossref) - Pandoc filter for cross-references


## Generating the Web with Jekyll


### Usage

Create an alias, which will make things easies:

```bash
alias leanpub='docker container run --rm -it \
    --volume $(pwd):/courseware \
    --publish 4000:4000 \
    --user $(id -u ${USER}):$(id -g ${USER}) \
    bletvaska/leanpub'
```

So then usage is simple:

```bash
$ leanpub usage
```


### Building the Courseware

To build and auto-rebuild the changed content, you just need to run following code from inside of your courseware directory:

```bash
$ leanpub build
```


### Cleaning the Results

```bash
$ leanpub clean
```


### Serving Course Webpage Locally

```bash
$ leanpub serve
```


### Building the ePub

```bash
$ leanpub epub
```


### Building the PDF

install following packages:

```bash
dnf install latexmk \
    texlive-xetex \
    texlive-pdfpages \
    texlive-pageslts \
    texlive-tex-gyre \
    texlive-tcolorbox \
    texlive-framed \
    texlive-mdwtools
```

```bash
$ leanpub pdf
$ latexmk -pdfxe -bibtex -pvc -shell-escape lectures.tex
```


## Development

### Structure of the Project

```
leanpub/
├── Dockerfile
├── justfile               building and releasing the image (not copied into the image)
├── requirements.txt       Python dependencies, installed while building the image
├── jekyll-theme-nucky/    sources of the Jekyll theme, installed as a gem
├── changelog.md
└── app/                   exact copy of /app in the image
    ├── justfile           commands run in the container (build, serve, epub, ...)
    ├── entrypoint.sh
    ├── tasks.py
    ├── liquid_render.rb
    ├── _config_defaults.yml
    ├── pandoc/
    └── texmf/
```


### Building and Releasing the Image

Every change is recorded in `changelog.md` under `## [Unreleased]`. The image
is versioned as `YYYY.M.PATCH` (e.g. `2026.9.10`).

```bash
$ just build                 # development image bletvaska/leanpub:dev
$ just release 2026.9.10     # tags 2026.9.10, 2026.9, 2026 and latest
$ just push 2026.9.10        # pushes these tags to Docker Hub
```

Before `just release`, rename `## [Unreleased]` in `changelog.md` to
`## [2026.9.10] - YYYY-MM-DD` and add a new empty `## [Unreleased]` above it.
`just release` refuses a version without a section in the changelog or
a version which is already on Docker Hub, `just push` refuses to push if
the four tags do not point to the same image.


### Modifying Templates without Rebuilding the Image

The templates and styles of artefacts are part of the Docker image. To modify them freely without rebuilding the image all the time, create the `leanpub` alisa following way:

```bash
$ alias leanpub='docker container run --rm -it \
    --volume $(pwd):/courseware \
    --volume /path/to/docker/image/leanpub/app/pandoc/:/app/pandoc \
    --publish 4000:4000 \
    --user $(id -u ${USER}):$(id -g ${USER}) \
    leanpub'
```

For modifying the _LaTeX_ template it is necessary to export `$TEXMFHOME` environment variable:

```bash
$ export TEXMFHOME=/path/to/docker/image/leanpub/app/texmf/
```

Then you can run locally command:

```bash
$ latexmk -pdfxe -bibtex -pvc -shell-escape lectures.tex
```
