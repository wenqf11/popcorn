# -*- coding: utf-8 -*-
__author__ = 'LY'


import settings
import time
from models import k_device, k_class, k_devicetype
import os


#用户上传文件
def handle_uploaded_file(username, f):
    #path = settings.IMG_DIR+'/'+username+'.'+f.name.split('.')[-1]
    filename = username+'.'+f.name.split('.')[-1]
    #path = os.getcwd() + settings.MEDIA_URL + '/user_avatar/' + filename
    path = settings.WEBSET_ROOT_PATH+settings.MEDIA_URL + '/user_avatar/' + filename
    with open(path, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return filename


# 获取系统当前时间
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


# 获取系统当前日期
def get_current_date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))


# 获取设备的节点树
def get_device_node(devicetypes, type_parent, class_parent):
    datas = list()
    for type in devicetypes:
        if type.parentid == type_parent:
            cur_data = dict()
            cur_data['text'] = type.name.decode('utf-8')
            device_list = list()
            devices = k_device.objects.filter(typeid_id = type.id, classid_id__in=class_parent)
            for d in devices:
                device_list.append({"text":(d.name+"(简称:"+d.brief+")").decode('utf-8'), "href":"/device?id=" + str(d.id)})
            sub_nodes = get_device_node(devicetypes, type.id, class_parent)
            if len(sub_nodes) > 0 and len(device_list) > 0:
                cur_data['nodes'] = device_list
                for sub_node in sub_nodes:
                    cur_data['nodes'].append(sub_node)
            elif len(sub_nodes) == 0 and len(device_list) > 0:
                cur_data['nodes'] = device_list
            elif len(sub_nodes) > 0 and len(device_list) == 0:
                cur_data['nodes'] = sub_nodes

            cur_data['number'] = len(device_list)
            if cur_data.has_key('nodes'):
                for sub_data in cur_data['nodes']:
                    if sub_data.has_key('nodes'): # not decive list, but a subclass
                        cur_data['number'] += sub_data['number']

            cur_data['text'] += '(设备数:' + str(cur_data['number']) + ')'
            datas.append(cur_data)

    return datas

# 获取设备类型的节点树
def get_type_node(devicetypes, parent):
    datas = list()
    for type in devicetypes:
        if type.parentid == parent:
            cur_data = dict()
            cur_data['text'] = type.name.decode('utf-8')
            cur_data['href'] = "/device_type?id=" + str(type.id)
            tmp = get_type_node(devicetypes, type.id)
            if len(tmp) > 0:
                cur_data['nodes'] = tmp
            datas.append(cur_data)

    return datas

def get_dept_type_node(devicetypes, parent):
    datas = list()
    for type in devicetypes:
        if type.parentid == parent:
            cur_data = dict()
            cur_data['text'] = type.name.decode('utf-8')
            cur_data['href'] = "/department?id=" + str(type.id)
            tmp = get_dept_type_node(devicetypes, type.id)
            if len(tmp) > 0:
                cur_data['nodes'] = tmp
            datas.append(cur_data)

    return datas


def get_device_class_node(classes, parent):
    datas = list()
    for c in classes:
        if c.parentid == parent:
            cur_data = dict()
            cur_data['text'] = c.name.decode('utf-8')
            cur_data['href'] = "/device?classid=" + str(c.id)
            tmp = get_device_class_node(classes, c.id)
            if tmp and len(tmp) > 0:
                cur_data['nodes'] = tmp
            datas.append(cur_data)
    return datas

def get_device_by_class(classes, parent):
    datas = list()
    for cls in classes:
        if cls.parentid == parent:
            cur_data = dict()
            cur_data['text'] = cls.name.decode('utf-8')
            cur_data['href'] = "/device?classid=" + str(cls.id)
            tmp = get_device_class_node(classes, cls.id)
            if tmp and len(tmp) > 0:
                cur_data['nodes'] = tmp
            datas.append(cur_data)

    return datas


def get_sub_classes_list(classes, sub_classes_list, class_parent):
    for cls in classes:
        if cls.parentid == class_parent:
            sub_classes_list.append(cls.id)
            get_sub_classes_list(classes,sub_classes_list,cls.id)


def get_decivetype_by_class(classid):
        tmp_class = k_class.objects.filter(id = classid)
        while True:
            if len(tmp_class)== 1:
                if tmp_class[0].depth <= 1:
                    tmp_id = tmp_class[0].id
                    return k_devicetype.objects.filter(status=tmp_id)
                tmp_class = k_class.objects.filter(id=tmp_class[0].parentid)
            else:
                return k_devicetype.objects.all()


def get_parent_classid(classid):
        tmp_class = k_class.objects.filter(id = classid)
        while True:
            if len(tmp_class)== 1:
                if tmp_class[0].depth <= 1:
                    return tmp_class[0].id
                tmp_class = k_class.objects.filter(id=tmp_class[0].parentid)
            else:
                return classid
