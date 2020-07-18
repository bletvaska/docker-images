#!/bin/sh

# get the data
TIME=$(date "+%H:%M:%S")
IP=$(hostname -i)
HOSTNAME=$(hostname)

# render template
template=$(sed /opt/template.tpl -r \
    -e "s/%TIME%/${TIME}/g" \
    -e "s/%IP%/${IP}/g" \
    -e "s/%HOSTNAME%/${HOSTNAME}/g" \
    )
echo -e "${template}"

# run additional command
exec "$@"
