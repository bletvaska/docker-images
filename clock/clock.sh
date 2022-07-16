#!/usr/bin/env sh


function on_sigint(){
    signal="INTERRUPT"
    timer=5
}


function on_sigterm(){
    signal="TERMINATE"
    timer=5
}


trap on_sigint  SIGINT   # 2
trap on_sigterm SIGTERM  # 15


function center(){
    text=$1
    cols=$(tput cols)
    printf "%"$(( (cols + ${#text})/2))"s" "${text}"
}

while true; do
    # render
    clear
    date "+%H:%M:%S" | figlet -ctk

    # if signal was received, then timer is running
    if [ "${timer}" ]; then
        center "Signal ${signal} Received."
        timer=$(( ${timer} - 1 ))

        # remove timer when on 0
        if [ "${timer}" -eq 0 ]; then
            unset timer
        fi
    fi

    # sleep
    sleep 1
done
