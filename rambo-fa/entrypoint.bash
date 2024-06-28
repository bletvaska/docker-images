#!/usr/bin/env bash

if [[ "${RAMBO_PART}" == 3 ]]; then
  timeout 20 $@
else
  exec "$@"
fi
