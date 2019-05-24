#!/bin/bash

LOG_FILE='out.log'

rm *.pyc > /dev/null 2>&1
rm $LOG_FILE > /dev/null 2>&1
pgrep python | xargs -r kill -s 9 
