#!/bin/bash

SUCCESS=false
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
for i in {1..5}; do
    if sudo python3 $DIR/SAWS.py; then
        $success=true
        break
    else
        sleep 2
    fi
done

if ! $success: then
    zenity --error --text="Tried to start SAWS.py 5 times\!" --title="Warning\!"
fi