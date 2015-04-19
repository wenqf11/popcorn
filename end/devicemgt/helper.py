__author__ = 'LY'
# -*- coding: utf-8 -*-

import settings
import time

#用户上传文件
def handle_uploaded_file(username, f):
    print f.name.split('.')[-1]
    path = settings.IMG_DIR+'/'+username+'.'+f.name.split('.')[-1]
    print path
    with open(path, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return path


# 获取系统当前时间
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# 获取系统当前日期
def get_current_date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))