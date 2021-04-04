#!/usr/bin/env sh

set -o errexit  # stop when error occurs
set -o pipefail # if not, expressions like `error here | true`
                # will always succeed
set -o nounset  # detects uninitialised variables
#set -x

_usage(){
    echo "Usage: COMMAND

Commands:
 usage      - shows this usage
 build      - build your site
 clean      - clean the site (removes site output and metadata file) without building
 serve      - serve your site locally
 update     - update dependencies to their latest versions
 install    - install the gems specified by the Gemfile or Gemfile.lock"

    echo
    echo "created by mirek (c) 2021"
}


# runs jekyll clean command
_jekyll_clean(){
    echo "Cleaning..."

    bundler exec jekyll clean
}


# runs jekyll build command
_jekyll_build(){
    echo "Building..."

    # check lecturer mode
    if [ -n "${LP_LECTURER+set}" ] && [ "${LP_LECTURER}" -eq 1 ]; then
        export _lecturer_config=",_config_lecturer.yml"
    fi

    # prepare command to run and execute
    cmd=$(echo 'bundler exec jekyll build 
        --config=_config.yml${_lecturer_config}
        --drafts' | envsubst)

    ${cmd}
}


# runs jekyll serve command with all the params
_jekyll_serve(){
    echo "Serving jekyll..."
    
    # check lecturer mode
    if [ -n "${LP_LECTURER+set}" ] && [ "${LP_LECTURER}" -eq 1 ]; then
        export _lecturer_config=",_config_lecturer.yml"
    fi

    # prepare command to run and execute
    cmd=$(echo 'bundler exec jekyll serve
        --config=_config.yml${_lecturer_config}
        --host 0.0.0.0
        --incremental
        --drafts' | envsubst)
    # !TODO prerobit na exec?
    ${cmd}
    #exec "${CMD}"
}


# updates the packages
_bundler_update(){
    echo "Updating..."

    exec bundler update
}


# install the packages
_bundler_install(){
    echo "Installing..."

    exec bundler install
}


main(){
    # show usage
    if [ "$#" -eq 0 ]; then
        _usage
        exit 0
    fi

    # check what to do based on jekyll commands
    if $(echo "${1}" | grep -Eq "(build|clean|serve|update|install|usage|deploy)"); then
        invoke "${@}"
        #if [ "${1}" == "build" ]; then
            #_jekyll_build $@
        #elif [ "${1}" == "clean" ]; then
            #_jekyll_clean $@
        #elif [ "${1}" == "serve" ]; then
            #_jekyll_serve $@
        #elif [ "${1}" == "update" ]; then
            #_bundler_update $@
        #elif [ "${1}" == "install" ]; then
            #_bundler_install $@
        #elif [ "${1}" == "usage" ]; then
            #_usage
        #fi

        exit 0
    fi

    echo "Running CMD..."
    exec "${@}"
}

main "${@}"

