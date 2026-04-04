#!/usr/bin/env sh

set -o errexit

readonly MAKEFILE_PATH=/app/Makefile

# running make?
if [ "${1}" = "make" ]; then
  shift
  make --makefile="${MAKEFILE_PATH}" "${@}"
  exit 0
fi

# exec
exec "$@"

