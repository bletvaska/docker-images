# Jekyll: Static Site Generator

Docker image for building and serving Jekyll static sites.

## Usage

All commands are run from your project directory, mounted into the container as `/web`.

```sh
$ docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    jekyll make <target>
```

To see all the available targets, type:

```sh
$ docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    jekyll make help
```




### Start a new project

Creates a new Jekyll site scaffold in the current directory:

```sh
$ docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    jekyll make new
```


### Install dependencies

Installs all gems defined in `Gemfile` into `vendor/bundle/`:

```sh
$ docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    jekyll make install
```


### Build the site

Generates the static site into `_site/`:

```sh
$ docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    jekyll make build
```


### Serve the site

Builds and serves the site locally at <http://localhost:5000> with live reload:

```sh
$ docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    --publish 5000:5000 \
    jekyll make serve
```


## Alias for your Linux system

To make things easier, you can create following alias:

```sh
$ alias jekyll="docker container run --rm -it \
    --user $(id --user):$(id --group) \
    --volume .:/web \
    --publish 5000:5000 \
    jekyll make"
```

Then you can simply run on your system command `jekyll <target>`. To see all the available targets, simply type:

```sh
$ jekyll help
```
