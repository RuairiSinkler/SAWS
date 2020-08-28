#!/bin/bash

SUCCESS=false
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
for i in {1..5}; do
    if ! $success; then
        sudo python3 SAWS.py &
        sleep 1
        if pgrep "sudo python3 SAWS.py"; then
            $success=true
            break
        else
            sleep 2
        fi
    fi
done

if ! $success; then
    zenity --error --text="Tried to start SAWS.py 5 times\!" --title="Warning\!"
fi