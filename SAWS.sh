#!/bin/bash

SUCCESS=false
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
RETRIES=3
cd $DIR
for i in {1..$RETRIES} ; do
    if [ "$SUCCESS" = false ] ; then
        sudo python3 SAWS.py &
        sleep 1
        if [[ $(ps aux | grep '[s]udo python3 SAWS.py') ]]; then
            SUCCESS=true
            break
        else
            sleep 2
        fi
    fi
done

if [ "$SUCCESS" = false ] ; then
    zenity --error --text="Tried to start SAWS.py $RETRIES times\!" --title="Warning\!"
fi
