#!/bin/bash

for i in {1..5};
do 
    sudo python3 SAWS.py && break || sleep 2;
done