# -*- coding: utf-8 -*-
__author__ = 'LY'


import settings
import time
from models import k_device


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


# 获取设备的节点树
def get_device_node(devicetypes, parent):
    datas = list()
    for type in devicetypes:
        if type.parentid == parent:
            cur_data = dict()
            cur_data['text'] = type.name
            device_list = list()
            devices = k_device.objects.filter(typeid_id = type.id)
            for d in devices:
                device_list.append({"text":d.name, "href":"/device?id=" + str(d.id)})
            sub_nodes = get_device_node(devicetypes, type.id)
            if len(sub_nodes) > 0 and len(device_list) > 0:
                cur_data['nodes'] = device_list
                for sub_node in sub_nodes:
                    cur_data['nodes'].append(sub_node)
            elif len(sub_nodes) == 0 and len(device_list) > 0:
                cur_data['nodes'] = device_list
            elif len(sub_nodes) > 0 and len(device_list) == 0:
                cur_data['nodes'] = sub_nodes
            datas.append(cur_data)

    return datas

# 获取设备类型的节点树
def get_type_node(devicetypes, parent):
    datas = list()
    for type in devicetypes:
        if type.parentid == parent:
            cur_data = dict()
            cur_data['text'] = type.name
            tmp = get_type_node(devicetypes, type.id)
            if len(tmp) > 0:
                cur_data['nodes'] = tmp
            datas.append(cur_data)

    return datas