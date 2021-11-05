# Toolbox 

Set of Linux tools for (not only) container testing.

Tools:

* `bash`
* `bats`
* `curl`
* `git`
* `httpie`
* `iputils`
* `jq`
* `jsonschema`
* `mtr`
* `nmap`
* `ping`
* `shellcheck`
* `sqlite`
* `stress-ng`
* `vim`
* `wget`
* `yq`


## Running

There are many tools preinstalled and also some configuration is provided too. Recommended way of using the _Toolbox_ is by creating an alias for your system:

```bash
alias toolbox='docker container run -it --rm \
    --volume $(pwd):/home/work \
    --user $(id -u ${USER}):$(id -g ${USER}) \
    bletvaska/toolbox'
```

Because of that:

* the `home` folder for the user is set to `/home`
* there is configuration for `bash` and `vim` already in the `/home` folder
* user's workdir is set to `/home/work/`

Then you can also use the _Toolbox_ locally:

```bash
$ toolbox http -b http://worldtimeapi.org/api/timezone/Europe/Bratislava
```


