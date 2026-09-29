#!/usr/bin/env sh

set -o errexit  # stop when error occurs
set -o pipefail # if not, expressions like `error here | true` will always succeed
set -o nounset  # detects uninitialised variables
#set -x


main(){
    # remove Gemfile.lock to avoid issue based on versions
    [ -e Gemfile.lock ] && rm Gemfile.lock

    # justfile lives under /app, alongside courseware mounted at
    # /courseware, so just needs both an explicit justfile location and an
    # explicit working directory (--justfile alone would switch the working
    # directory to /app instead of the courseware being built)
    just_cmd="just --justfile=/app/justfile --working-directory=$(pwd)"

    # show usage; with a recipe name (e.g. `usage build`), show that
    # recipe's own options instead of the full list
    if [ "$#" -eq 0 ] || [ "${1}" = "usage" ] || [ "${1}" = "help" ]; then
        if [ "$#" -gt 1 ]; then
            exec ${just_cmd} --usage "${2}"
        fi

        ${just_cmd} --list

        echo
        echo "created by mirek (c) 2021, 2026"

        exit 0
    fi

    # recipes working with the site need a jekyll root (at least _config.yml);
    # without it jekyll (or tasks.py) dies with an ugly stack trace, so stop
    # early with a readable message instead
    case "${1}" in
        build|clean|serve|deploy|epub|pdf)
            if [ ! -f _config.yml ]; then
                echo "Error: the current folder is not a jekyll site root (no _config.yml found)." >&2
                echo "Run it from the course folder containing _config.yml." >&2
                exit 1
            fi
            ;;
    esac

    # check what to do based on jekyll commands
    # exec replaces this shell with just, so it becomes PID 1 and receives
    # signals (e.g. from `docker stop`) directly instead of relying on a
    # shell in between to forward them
    if $(echo "${1}" | grep -Eq "(build|clean|serve|update|install|deploy|epub|pdf|shell|versions)"); then
        exec ${just_cmd} "${@}"
    fi

    echo "Running CMD..."
    exec "${@}"
}

main "${@}"

