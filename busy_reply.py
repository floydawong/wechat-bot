# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import config

import time
import threading

_msg_cache = {}

def check_exclude(msg):
    split_names = config.busy_reply_friend_exclude.split('|')
    for name in split_names:
        if name in msg.sender.name:
            return True
        if name in msg.sender.nick_name:
            return True
        if name in msg.sender.remark_name:
            return True
    return False

def busy_auto_reply(msg):
    _msg_cache[msg.sender] = msg


def _is_msg_overtime(msg):
    create_time = str(msg.create_time)

    # Fix: create_time有一定几率出现小数点, 比如: 2019-05-23 09:39:02.577000
    if create_time.find('.') > 0:
        create_time = create_time[:create_time.find('.')]

    timestamp = time.mktime(time.strptime(create_time, "%Y-%m-%d %H:%M:%S"))
    nowstamp = time.time()
    if nowstamp - timestamp > config.auto_busy_reply_time:
        return True
    return False


def _tick():
    for sender in _msg_cache:
        msg = _msg_cache[sender]
        if not msg:
            continue

        # 如果超时, 由机器人自动回复信息.
        if _is_msg_overtime(msg):
            msg.reply(config.auto_busy_reply_msg)
            _msg_cache[sender] = None
            continue

        # 如果历史消息中, 有自己的回复, 则在缓存中清楚该记录.
        for history_msg in msg.bot.messages:
            if _is_msg_overtime(history_msg):
                continue
            if history_msg.sender == history_msg.bot.self:
                _msg_cache[sender] = None
                break

class Tick(threading.Thread):
    def run(self):
        while True:
            time.sleep(1)
            _tick()

def start():
    main_thread = Tick()
    main_thread.start()
