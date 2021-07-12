#!/usr/bin/env sh

set -o errexit  # stop when error occurs
set -o pipefail # if not, expressions like `error here | true` will always succeed
set -o nounset  # detects uninitialised variables
#set -x


main(){
    # remove Gemfile.lock to avoid issue based on versions
    [ -e Gemfile.lock ] && rm Gemfile.lock

    # show usage
    if [ "$#" -eq 0 ] || [ "${1}" == "usage" ]; then
        inv --list

        echo
        echo "created by mirek (c) 2021"

        exit 0
    fi

    # check what to do based on jekyll commands
    if $(echo "${1}" | grep -Eq "(build|clean|serve|update|install|deploy|epub|preprocess)"); then
        invoke "${@}"

        exit 0
    fi

    echo "Running CMD..."
    exec "${@}"
}

main "${@}"

