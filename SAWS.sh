#!/bin/bash

SUCCESS=false
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
for i in {1..5}; do
    if [[] ! $SUCCESS ]]; then
        sudo python3 SAWS.py &
        sleep 1
        if [[ $(ps aux | grep -q '[s]udo python3 SAWS.py') ]]; then
            $SUCCESS=true
            break
        else
            sleep 2
        fi
    fi
done

if [[ ! $SUCCESS ]] ; then
    zenity --error --text="Tried to start SAWS.py 5 times\!" --title="Warning\!"
fi