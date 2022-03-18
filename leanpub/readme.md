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

The templates and styles of artefacts are part of the Docker image. To modify them freely without rebuilding the image all the time, create the `leanpub` alisa following way:

```bash
$ alias leanpub='docker container run --rm -it \
    --volume $(pwd):/courseware \
    --volume /path/to/docker/image/leanpub/pandoc/:/pandoc \
    --publish 4000:4000 \
    --user $(id -u ${USER}):$(id -g ${USER}) \
    leanpub'
```

For modifying the _LaTeX_ template it is necessary to export `$TEXMFHOME` environment variable:

```bash
$ export TEXMFHOME=/path/to/docker/image/leanpub/texmf/
```

Then you can run locally command:

```bash
$ latexmk -pdfxe -bibtex -pvc -shell-escape lectures.tex
```
