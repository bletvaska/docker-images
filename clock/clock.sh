#!/usr/bin/env sh

function on_exit(){
    echo "on_exit"
    signal="ON EXIT"
}


function on_sigint(){
    echo "on_sigint"
    signal="INTERRUPT"
}


function on_sigterm(){
    echo "on_sigterm"
    signal="TERMINATE"
}

trap on_exit EXIT
trap on_sigint SIGINT
trap on_sigint SIGTERM

while true; do 
    clear
    date "+%H:%M:%S" | figlet -ctk
    if [[ ${signal} ]]; then
        echo "${signal}"
    fi
    sleep 1
done
