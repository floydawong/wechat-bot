# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import config

import time

_msg_cache = {}

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

        if _is_msg_overtime(msg):
            msg.reply('[机器人]\n我可能在忙, 有急事请打我电话!\n{}\n'.format(config.telephone_number))
            _msg_cache[sender] = None
            continue

        for history_msg in msg.bot.messages:
            if _is_msg_overtime(history_msg):
                continue
            if history_msg.sender == history_msg.bot.self:
                _msg_cache[sender] = None
                break

def start():
    while True:
        time.sleep(1)
        _tick()
