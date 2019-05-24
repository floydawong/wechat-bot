#!/bin/bash

LOG_FILE='out.log'

show_log(){
    echo 3..
    sleep 1
    echo 2..
    sleep 1
    echo 1..
    sleep 1
    cat $LOG_FILE
}

zzz='python'

sh ./stop.sh
nohup $zzz wechat_robot.py > $LOG_FILE &

sleep 1
show_log

