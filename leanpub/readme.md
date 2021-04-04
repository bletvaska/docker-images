# Lean Publishing Toolbox for My Courses at KPI

Image for building my courses, which are written with [Jekyll](https://jekyllrb.com) - static site generator.

For generating is used `pandoc` instead of built in `kramdown` and won theme `nucky` is also builtin in the image.


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


## Building the ePub


## Building the PDF

