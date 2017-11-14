# -*- encoding=UTF-8 -*-
__author__ = 'LY'


from django.shortcuts import render_to_response
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout,login as auth_login
from django.contrib.auth.decorators import login_required
from models import *
from forms import *
from index import *
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from helper import handle_uploaded_file, get_current_time, get_current_date, get_type_node, get_device_node, get_device_by_class, get_dept_type_node, get_sub_classes_list, get_decivetype_by_class, get_parent_classid, have_right_to_devicemgt
import json
import xlwt
import re


purviewhash = {
    1: ["用户管理","部门设置"],#ok
    2: ["用户管理","部门设置","添加部门","编辑部门"],#ok
    3: ["用户管理","部门设置","删除部门"],#审核？
    4: ["用户管理","角色管理"],#ok
    5: ["用户管理","角色管理","添加角色","编辑角色"],#ok
    6: ["用户管理","角色管理","删除角色"],#审核？
    7: ["用户管理","所有用户"],#ok
    8: ["用户管理","所有用户","添加用户","编辑用户"],#ok
    9: ["用户管理","所有用户","删除用户"],#审核？
    10: ["设备管理","设备类型"],#ok
    11: ["设备管理","设备类型","添加设备类型"],#编辑？
    12: ["设备管理","设备类型","编辑设备类型", "删除设备类型"],#删除/审核？
    13: ["设备管理","生产厂家"],#ok
    14: ["设备管理","生产厂家","添加生产厂家","编辑生产厂家"],#ok
    15: ["设备管理","生产厂家","删除生产厂家"],#审核？
    16: ["设备管理","供应商"],#ok
    17: ["设备管理","供应商","添加供应商","编辑供应商"],#ok
    18: ["设备管理","供应商","删除供应商"],#审核？
    19: ["设备管理","所有设备"],#ok
    20: ["设备管理","所有设备","添加设备","编辑设备"],#ok
    21: ["设备管理","所有设备","删除设备"],#审核？
    22: ["库存","所有备件信息"],#ok
    23: ["库存","所有备件信息","添加备件信息","编辑备件信息"],#ok
    24: ["库存","所有备件信息","删除备件信息","审核备件信息"],#ok
    25: ["库存","所有工具信息"],#ok
    26: ["库存","所有工具信息","添加工具信息","编辑工具信息"],#ok
    27: ["库存","所有工具信息","删除工具信息","审核工具信息"],#ok
    28: ["保养","维修保养","尚未保养","保养记录","设备管理","所有设备","保养计划"],#ok
    29: ["保养","设备管理","所有设备","保养计划","添加保养","编辑保养","添加保养计划"],#ok
    30: ["保养","维修保养","保养记录","设备管理","所有设备","保养计划","删除保养","审核保养"],#ok
    31: ["维修","维修保养","尚未维修","维修记录"],#ok
    32: ["维修","维修保养","尚未维修","指派维修"],#ok
    33: ["维修","维修保养","尚未维修","添加维修任务","编辑维修"],#ok
    34: ["维修","维修保养","尚未维修","维修记录","删除维修","审核维修"],#ok
    35: ["任务","未完成任务","任务记录"],#ok
    36: ["任务","未完成任务","任务记录","添加任务","编辑任务"],#ok
    37: ["任务","未完成任务","任务记录","删除任务","审核任务"],#ok
    38: ["库存","备件使用","备件出入库"],#ok
    39: ["库存","备件使用","备件出入库","添加备件库存记录","编辑备件库存记录"],#ok
    40: ["库存","备件使用","备件出入库","删除备件库存记录","审核备件库存记录"],#ok
    41: ["库存","工具使用","工具出入库"],#ok
    42: ["库存","工具使用","工具出入库","添加工具库存记录","编辑工具库存记录"],#ok
    43: ["库存","工具使用","工具出入库","删除工具库存记录","审核工具库存记录"],#ok
    44: ["抄表数据"],#ok
    45: ["积分与抽奖","积分设置"],#ok
    46: ["积分与抽奖","积分设置","编辑积分"],#ok
    47: ["积分与抽奖","积分记录"],#ok
    48: ["积分与抽奖","抽奖设置"],#ok
    49: ["积分与抽奖","抽奖设置","编辑抽奖"],#ok
    50: ["积分与抽奖","抽奖记录"],#ok
    51: ["路线设置","查看路线"],#ok
    52: ["路线设置","查看路线","添加路线","编辑路线"],#ok
    53: ["路线设置","查看路线","删除路线"],#审核？
    54: ["排班设置"],#ok
    55: ["排班设置","编辑排班"],
    56: ["考勤记录"],#ok
}


# 查找权限集合并返回
def get_purviews_and_render_to_response(username, page, variables={}):
    _user = k_user.objects.get(username=username)
    _roles = _user.roles.all()
    _userpurviews = []
    for _role in _roles:
        _purviews = _role.purviews.all()
        for _purview in _purviews:
            if _purview.id not in _userpurviews:
                _userpurviews.append(_purview.id)
    _modelsshow = []
    for _userpurview in _userpurviews:
        _modelsshow.extend(purviewhash[_userpurview])
    _modelsshow = list(set(_modelsshow))
    variables["modelsshow"] = _modelsshow
    return render_to_response(page, variables)


# 查找分类集合
def get_class_set(result, current_class):
    children_class = k_class.objects.filter(parentid=current_class)
    for child_class in children_class:
        result.append(child_class.id)
        get_class_set(result, child_class.id)


# 权限判断
def check_purview(username, pid):
    _user = k_user.objects.get(username=username)
    _roles = _user.roles.all()
    _userpurviews = []
    for _role in _roles:
        _purviews = _role.purviews.all()
        for _purview in _purviews:
            if _purview.id not in _userpurviews:
                _userpurviews.append(_purview.id)
    if int(pid) in _userpurviews:
        return 0
    else:
        _purview = k_purview.objects.get(id=pid)
        return _purview.memo


# 首页
@login_required
def index(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    data = dict()
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
       purview_msg = ''
    #, 'purview_msg': purview_msg
    data["name"] = user.name
    data["usernum"] = get_user_num(user.classid_id)
    data["devicenum"] = get_device_num(user.classid_id)
    data["userscore"] = get_user_score(user.id)
    data["userrank"] = get_user_rank(user.id, user.classid_id)
    data["unmaintenance1"] = get_user_unmaintenance(user.id, 1)
    data["unmaintenance2"] = get_user_unmaintenance(user.id, 2)
    data["unfinishedtask"] = get_user_unfinishedtask(user.id)
    data["spareusing"] = get_using_spare(user.classid_id)
    data["toolusing"] = get_using_tool(user.classid_id)
    data["attendence"] = get_attendence_stat(user.classid_id)
    data["tasks"] = get_task_stat(user.classid_id)
    data["maintenance1"] = get_maintenace_stat(user.classid_id, 1)
    data["maintenance2"] = get_maintenace_stat(user.classid_id, 2)
    # 读取权限，显示内容
    variables = RequestContext(request, {
        'username': user.username,
        'purview_msg': purview_msg,
        'useravatar': user.avatar,
        'data': data
    })
    return get_purviews_and_render_to_response(request.user.username, 'index.html', variables)


'''
用户管理开始
'''


def get_leaf(leaf_list):
    result = list()
    for leaf in leaf_list:
        userdata = dict()
        userdata["text"] = leaf.name.decode('utf-8')
        userdata["href"] = "/user?id=" + str(leaf.id)
        result.append(userdata)
    return result


def get_node(child_leaf_list, child_node_list):
    result = list()
    for leaf in child_leaf_list:
        userdata = dict()
        userdata["text"] = leaf.name.decode('utf-8')
        userdata["href"] = "/user?id=" + str(leaf.id)
        userdata["number"] = 0
        result.append(userdata)
    for c in child_node_list:
        userdata = dict()
        userdata["text"] = c.name.decode('utf-8')
        userdata["nodes"] = list()
        sub_child_list = k_class.objects.filter(parentid = c.id)
        sub_leaf_list = k_user.objects.filter(classid_id=c.id)
        if sub_child_list:
            userdata["nodes"] = get_node(sub_leaf_list, sub_child_list)
        elif sub_leaf_list:
            userdata["nodes"] = get_leaf(sub_leaf_list)
        result.append(userdata)

        userdata["number"] = len(sub_leaf_list)
        for sub_node in userdata["nodes"]:
            if sub_node.has_key("nodes"):
                userdata["number"] += sub_node["number"]
        userdata["text"] +=  '(人数:' + str(userdata['number']) + ')'
    return result


@login_required
def usermgt(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    current_class_id = user.classid_id
    current_class = k_class.objects.get(id=current_class_id)
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''

    if current_class:
        userdatas = list()
        class_set = k_class.objects.filter(parentid=current_class_id)
        leaf_set = k_user.objects.filter(classid_id=current_class_id)
        for leaf in leaf_set:
            userdata = dict()
            userdata["text"] = leaf.name.decode('utf-8')
            userdata["href"] = "/user?id=" + str(leaf.id)
            userdatas.append(userdata)
        for c in class_set:
            userdata = dict()
            userdata["text"] = c.name.decode('utf-8')
            child_list = k_class.objects.filter(parentid = c.id)
            leaf_list = k_user.objects.filter(classid_id=c.id)
            userdata["nodes"] = get_node(leaf_list, child_list)

            userdata["number"] = len(leaf_list)
            for sub_node in userdata["nodes"]:
                if sub_node.has_key("nodes"):
                    userdata["number"] += sub_node["number"]
            userdata["text"] +=  '(人数:' + str(userdata['number']) + ')'

            userdatas.append(userdata)

        cur_datas = dict()
        datas = list()
        cur_datas["text"] = current_class.name.decode('utf-8')
        cur_datas['nodes'] = userdatas

        cur_datas["number"] = len(leaf_set)
        for sub_node in cur_datas["nodes"]:
            if sub_node.has_key("nodes"):
                cur_datas["number"] += sub_node["number"]
        cur_datas["text"] +=  '(人数:' + str(cur_datas['number']) + ')'

        datas.append(cur_datas)

    _id = request.GET.get('id')
    # 如果访问某个用户的信息
    if _id:
        # 根据用户id取出用户
        user_info = k_user.objects.get(id=_id)
        # 根据用户id取出用户角色
        user_role = k_role.objects.filter(k_user=_id)
        # 根据用户的classid取出层级关系
        user_class_list = []
        tmp_class = k_class.objects.filter(id=user_info.classid_id)
        while tmp_class:
            if len(tmp_class) == 1:
                user_class_list.append(tmp_class[0].name)
                tmp_class = k_class.objects.filter(id=tmp_class[0].parentid)
            else:
                print "error!"
        user_class = ""
        user_class_len = len(user_class_list)
        for i in xrange(0,user_class_len):
            user_class += user_class_list[user_class_len - i - 1] + "-"
        user_class = user_class[0:len(user_class) - 1]
        temp = serializers.serialize('json', [user_info,])
        struct = json.loads(temp)
        res_user_info = struct[0]

        res_user_role = list()
        for role in user_role:
            res_user_role.append(role.name)

        return HttpResponse(json.dumps({
            "info": res_user_info,
            "role": res_user_role,
            "class": user_class}
        ), content_type="application/json")
    else:
        variables = RequestContext(request, {
            'username': user.username,
            'useravatar': user.avatar,
            'clicked_item': 'user',
            'data': datas,
            'server_msg': server_msg
        })
        return get_purviews_and_render_to_response(request.user.username, 'user.html', variables)


@login_required
def operate_user(request):
    """
        update user information
    """
    if request.method == 'GET':
        user = k_user.objects.get(username=request.user.username)
        # 读取权限，显示内容
        _id = request.GET.get('id')
        userdata = dict()

        #分类筛选
        user = k_user.objects.get(username=request.user.username)
        result = [user.classid.id]
        get_class_set(result, user.classid.id)
        class_list = list()
        classes = k_class.objects.filter(id__in=result)
        for c in classes:
            class_list.append(c.name)
        role_list = list()
        roles = k_role.objects.filter(classid__in=result)
        for role in roles:
            role_list.append(role.name)

        userdata['class_list'] = class_list
        userdata['role_list'] = role_list
        if _id:
            theuser = k_user.objects.filter(id=_id)[0]
            key_list = ['state', 'username', 'name', 'avatar', 'mobile', 'email', 'address', 'zipcode', 'birthday',
                        'idcard', 'idcardtype', 'contact','contactmobile', 'content', 'memo', 'birthday']
            for key in key_list:
                userdata[key] = eval('theuser.' + key)

            userdata['class_name'] = theuser.classid.name

            k_chosed_roles = k_role.objects.filter(k_user=_id)
            chosed_roles = []
            for k_chosed_role in k_chosed_roles:
                chosed_roles.append(k_chosed_role.name)
            userdata['chosen_roles'] = chosed_roles
            userdata['disabled_chosen_roles'] = list(set(chosed_roles).difference(set(role_list)))
        else:
            userdata['isNew'] = True

        server_msg = request.GET.get('msg')
        if server_msg:
            variables = RequestContext(request, {'username': user.username, 'data': userdata, 'server_msg': server_msg, 'useravatar': user.avatar})
        else:
            variables = RequestContext(request, {'username': user.username, 'data': userdata, 'useravatar': user.avatar,})
        return get_purviews_and_render_to_response(request.user.username, 'useroperate.html', variables)
    else:
        user = k_user.objects.filter(username=request.POST['username'])
        if len(user) == 1:
            user = user[0]
            cur_user_id = user.id
            _d_username = user.username

            _c = k_class.objects.get(name=request.POST['classname'])
            if _c:
                user.classid = _c

            raw_password = request.POST['password']
            user.email = request.POST['email']
            user.name = request.POST['name']
            user.mobile = request.POST['mobile']
            user.gender = request.POST['gender']
            user.zipcode = request.POST['zipcode']
            user.address = request.POST['address']
            user.birthday = datetime.strptime(request.POST['birthday'], '%Y-%m-%d').date()
            user.idcard = request.POST['idcard']
            user.idcardtype = request.POST['idcardtype']
            user.content = request.POST['content']
            user.memo = request.POST['memo']
            user.contact = request.POST['contact']
            user.contactmobile = request.POST['contactmobile']
            tmp_urs = user.roles.filter(k_user=user.id)
            for ur in tmp_urs:
                user.roles.remove(ur)
            # 建立user和role的关系
            roles_name = request.POST.getlist('role')
            for r_name in roles_name:
                roles = k_role.objects.filter(name=r_name)
                for role in roles:
                    user.roles.add(role.id)
            user.editorid = request.user.id
            user.editdatetime=get_current_date()

            if raw_password != "":
                user.set_password(raw_password)
                _d_user = User.objects.get(username=_d_username)
                _d_user.set_password(raw_password)
                _d_user.save()
            user.save()

            server_msg = '修改用户资料成功！'
            return HttpResponseRedirect('/user_operate/?id=' + str(cur_user_id) + '&msg=' + server_msg)
        else:
            server_msg = "用户名不存在！"
            return HttpResponseRedirect('/user_operate/?msg=' + server_msg)


@login_required
def useradd(request):
    """ add new user
    """
    login_user = k_user.objects.get(username=request.user.username)
    server_msg = ''
    cur_user_id = 0
    if request.method == 'POST':
        avatar = "default-user.png"
        # 如果用户名相同，修改已有的用户
        user = k_user.objects.filter(username=request.POST['username'])
        if not user:
            # 总共要有26项信息
            classid = k_class.objects.filter(name=request.POST['classname'])[0]
            user = k_user.objects.create_user(username=request.POST['username'],
                classid=classid,
                state=1,
                password=request.POST['password'],
                name=request.POST['name'],
                face=avatar,
                avatar=avatar,
                mobile=request.POST['mobile'],
                email=request.POST['email'],
                address=request.POST['address'],
                zipcode=request.POST['zipcode'],
                gender=request.POST['gender'],
                birthday=datetime.strptime(request.POST['birthday'], '%Y-%m-%d').date(),
                idcard=request.POST['idcard'],
                idcardtype=0,
                content=request.POST['content'],
                memo=request.POST['memo'],
                contact=request.POST['contact'],
                contactmobile=request.POST['contactmobile'],
                creatorid=login_user.id,
                createdatetime=get_current_date(),
                editorid=login_user.id,
                editdatetime=get_current_date(),
                auditorid=login_user.id,
                auditdatetime=get_current_date(),
                status=0,
            )
            # 给roles和user也增加一条记录
            olduser = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=user.password
            )

            # 保存
            user.save()
            olduser.save()

            cur_user_id = user.id

            # 建立user和role的关系
            roles = k_role.objects.filter(name=request.POST['role'])
            for role in roles:
                user.roles.add(role.id)
            server_msg = '添加用户成功！'
        else:
            server_msg = "用户名已存在！"
        return HttpResponseRedirect('/useradd/?msg=' + server_msg)
    else:
        user = User.objects.get(username=request.user.username)
        # 读取权限，显示内容
        _id = request.GET.get('id')
        userdata = dict()

        #分类筛选
        user = k_user.objects.get(username=request.user.username)
        result = [user.classid.id]
        get_class_set(result, user.classid.id)
        class_list = list()
        classes = k_class.objects.filter(id__in=result)
        for c in classes:
            class_list.append(c.name)
        role_list = list()
        roles = k_role.objects.filter(classid__in=result)
        for role in roles:
            role_list.append(role.name)

        userdata['class_list'] = class_list
        userdata['role_list'] = role_list
        if _id:
            theuser = k_user.objects.filter(id=_id)[0]
            key_list = ['username', 'name', 'avatar', 'mobile', 'email', 'address', 'zipcode', 'birthday',
                        'idcard', 'idcardtype', 'contact','contactmobile', 'content', 'memo', 'birthday']
            for key in key_list:
                userdata[key] = eval('theuser.' + key)

            k_chosed_roles = k_role.objects.filter(k_user=_id)
            chosed_roles = []
            for k_chosed_role in k_chosed_roles:
                chosed_roles.append(k_chosed_role.name)
            userdata['chosen_roles'] = chosed_roles
        else:
            userdata['isNew'] = True
        server_msg = request.GET.get('msg')
        if server_msg:
            variables = RequestContext(request, {'username': user.username, 'data': userdata, 'useravatar': user.avatar, 'server_msg': server_msg})
        else:
            variables = RequestContext(request, {'username': user.username, 'useravatar': user.avatar, 'data': userdata})
        return get_purviews_and_render_to_response(request.user.username, 'useradd.html',variables)


@login_required
def update_user(request):
    '''修改用户信息
    '''
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    server_msg = ''
    cur_user_id = 0
    if request.method == 'POST':
        user = k_user.objects.filter(username=request.POST['username'])
        if len(user) == 1:
            user = user[0]
            cur_user_id = user.id
            _d_username = user.username

            _c = k_class.objects.get(name=request.POST['classname'])
            if _c:
                user.classid = _c

            raw_password = request.POST['password']
            user.email = request.POST['email']
            user.name = request.POST['name']
            user.mobile = request.POST['mobile']
            user.gender = request.POST['gender']
            user.zipcode = request.POST['zipcode']
            user.address = request.POST['address']
            user.birthday = datetime.strptime(request.POST['birthday'], '%Y-%m-%d').date()
            user.idcard = request.POST['idcard']
            user.idcardtype = request.POST['idcardtype']
            user.content = request.POST['content']
            user.memo = request.POST['memo']
            user.contact = request.POST['contact']
            user.contactmobile = request.POST['contactmobile']
            user.editorid = request.user.id
            user.editdatetime = get_current_date()
            tmp_urs = user.roles.filter(k_user=user.id)
            for ur in tmp_urs:
                user.roles.remove(ur)
            # 建立user和role的关系
            roles_name = request.POST.getlist('role')
            for r_name in roles_name:
                roles = k_role.objects.filter(name=r_name)
                for role in roles:
                    user.roles.add(role.id)
            user.editorid = request.user.id
            user.editdatetime=get_current_date()

            user.set_password(raw_password)
            user.save()

            # 修改django数据库中的密码
            _d_user = User.objects.get(username=_d_username)
            _d_user.set_password(raw_password)
            _d_user.save()

            server_msg = '修改用户资料成功！'
            return HttpResponseRedirect('/user_operate/?id=' + str(cur_user_id) + '&msg=' + server_msg)
        else:
            server_msg = "用户名不存在！"
            return HttpResponseRedirect('/user_operate/?msg=' + server_msg)
    else:
        return HttpResponseRedirect('/user_operate/')


def userdel(request):
    if request.user.is_authenticated():
        _id = request.GET.get('id')
        if int(_id) == request.user.id:
            return HttpResponseRedirect('/user/?msg="不能删除用户本身"')
        if _id:
            users = k_user.objects.get(id=_id)
            str = "成功删除用户" + users.username
            users.delete()
        return HttpResponseRedirect('/user/?msg='+str)
    else:
        return HttpResponseRedirect('/login/')


@login_required
def userset(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'userset.html', variables)

@login_required
def userbatch_add(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'userbatchadd.html', variables)


@login_required
def userbatch_submit(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    if request.method == "POST":
        raw_post_data = request.body
        json_data = json.loads(raw_post_data)
        success_num = 0
        try:
            for json_key in json_data:
                obj_datas = json_data[json_key]
                for obj_data in obj_datas:
                    _username = obj_data['username']
                    _name = obj_data['name']
                    _classname = obj_data['classname']
                    _classid = k_class.objects.get(name=_classname)
                    _users = k_user.objects.filter(username=_username)
                    if len(_users) > 0:
                        _dev = _users[0]
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += _classname+'中'+_dev.name+'('+_dev.username+')的用户已存在！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")

                    _gender = 1
                    if obj_data['gender'] == '女':
                        _state = 0
                    elif obj_data['gender'] == '男':
                        _state = 1
                    else:
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += '用户性别有误！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")

                    _state = 0
                    if obj_data['state'] == '锁定':
                        _state = 0
                    elif obj_data['state'] == '在岗':
                        _state = 1
                    elif obj_data['state'] == '长假':
                        _state = 2
                    elif obj_data['state'] == '离职':
                        _state = 3
                    else:
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += '用户状态有误！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")

                    if obj_data['idcardtype'] != '身份证':
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += '该用户没有身份证！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")

                    _avatar='default.png'

                    _user = k_user.objects.create(
                        classid=_classid,
                        username=_username,
                        name=_name,
                        gender=_gender,
                        state=_state,
                        mobile=obj_data['mobile'],
                        email=obj_data['email'],
                        address=obj_data['address'],
                        zipcode=obj_data['zipcode'],
                        birthday=obj_data['birthday'],
                        idcard=obj_data['idcard'],
                        idcardtype=0,
                        memo=obj_data['memo'],
                        contact=obj_data['contact'],
                        contactmobile=obj_data['contactmobile'],
                        status=_state,
                        avatar=_avatar,
                        creatorid=request.user.id,
                        createdatetime=get_current_date(),
                        editorid=request.user.id,
                        editdatetime=get_current_date(),
                        auditorid=request.user.id,
                        auditdatetime=get_current_date()
                    )

                    roles = k_role.objects.filter(name=obj_data['roles'])
                    for role in roles:
                        _user.roles.add(role.id)

                    raw_password = _username
                    _user.set_password(raw_password)

                    _olduser = User.objects.create_user(
                        username=_user.username,
                        email=_user.email,
                        password=_user.password
                    )
                    _user.save()
                    _olduser.save()
                    success_num += 1
            server_msg = '成功添加'+str(success_num)+'条用户信息！'
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
        except Exception as e:
            server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查所属部门、设备类别和责任人用户名是否正确！'
            print e
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
    # 读取权限，显示内容
    server_msg = "导入失败，请检查数据格式是否符合模板要求！"
    return HttpResponse(json.dumps({
        "username": user.username,
        "server_msg":server_msg
        }), content_type="application/json")

'''
用户管理结束
设备管理开始
'''

@login_required
def device_view_all(request):
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''
    devicetypes = get_decivetype_by_class(user.classid_id)
    dev_type_id_list = list()
    for dtype in devicetypes:
        dev_type_id_list.append(dtype.id)

    device = k_device.objects.all()

    data = []
    for d in device:
        if not d.typeid_id in dev_type_id_list:
            continue
        dataitem = {}
        
        if d.classid:
            dataitem['classname'] = d.classid.name
        else:
            dataitem['classname'] = "未指定部门"
        dataitem['brief'] = d.brief
        dataitem['name'] = d.name
        dataitem['position'] = d.position
        dataitem['brand'] = d.brand
        dataitem['model'] = d.model
        dataitem['serial'] = d.serial
        dataitem['content'] = d.content
        dataitem['buytime'] = d.buytime
        dataitem['notice'] = d.notice
        dataitem['memo'] = d.memo

        # device type
        devicetype = k_devicetype.objects.filter(id=d.typeid_id)
        if len(devicetype) == 1:
            dataitem['devicetype'] = devicetype[0].name
        else:
            dataitem['devicetype'] = "未指定设备分类"

        # producer/supplier
        if d.producerid:
            dataitem['producer'] = d.producerid.name
        else:
            dataitem['producer'] = '无'
        if d.supplierid:
            dataitem['supplier'] = d.supplierid.name
        else:
            dataitem['supplier'] = '无'

        # owner
        owner = k_user.objects.filter(id=d.ownerid)
        if len(owner) == 1:
            dataitem['owner'] = owner[0].name
        else:
            dataitem['owner'] = "未指定负责人或该用户已被删除"

        # spare
        str_spares = ''
        spares = k_spare.objects.filter(k_device=d.id)
        for s in spares:
            str_spares += '%s (编号:%s, 型号:%s)'%(s.name, s.brief, s.model) + ','
        if str_spares != '':
            dataitem['spares'] = str_spares[0:len(str_spares)-1]
        else:
            dataitem['spares'] = '无'

        data.append(dataitem)

    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'device_view_all.html', {"data": data, 'purview_msg': purview_msg,
                                                                                     'username':user.username, 'useravatar': user.avatar})


@login_required
def devicebyclass(request):
    user = k_user.objects.get(username=request.user.username)
    _parent_classid = get_parent_classid(user.classid_id)
    '''
    parents = user.classid
    if parents.depth == 0:  
        classes = k_class.objects.all()
        datas = list()
        data = dict()
        data['text'] = parents.name
        data['href'] = "/device?classid=" + str(parents.id)
        data['nodes'] = get_device_by_class(classes, parents.id)
        if data['nodes']:
            datas.append(data)
            variables=RequestContext(request,{'username':user.username,  'useravatar': user.avatar, 'data':datas})
            return get_purviews_and_render_to_response(request.user.username, 'devicebyclass.html',variables)
    '''
    if have_right_to_devicemgt(_parent_classid):
        return HttpResponseRedirect('/device?classid=%d'%_parent_classid)
    else:
        return HttpResponseRedirect('/device/')

@login_required
def devicemgt(request):
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''
    #devicetypes = k_devicetype.objects.all()
    
    type_parents = 0
    class_parents = 0
    filter_classidx = request.GET.get('classid')
    if filter_classidx:
        class_parents = int(filter_classidx)

    classes = k_class.objects.all()

    _id = request.GET.get('id')
    if (_id):
            tmp_device = k_device.objects.filter(id=_id)
            if len(tmp_device) == 1:
                tmp_device = tmp_device[0]
                class_parents = int(tmp_device.classid_id)


    datas = list()
    tmp_parents = user.classid
    if tmp_parents.depth == 0:  # handle the topest right
        sub_datas = list()
        for c in classes:
            if c.parentid == tmp_parents.id:
                sub_data = dict()
                sub_data['text'] = c.name
                sub_data['href'] = "#"
                class_parents = c.id
                sub_classes_list = list()
                devicetypes = get_decivetype_by_class(class_parents)
                sub_classes_list.append(class_parents)
                get_sub_classes_list(classes, sub_classes_list, class_parents)
                class_parents = sub_classes_list
                sub_data['nodes'] = get_device_node(devicetypes, type_parents, class_parents) #获取节点树
                sub_datas.append(sub_data)

        datas = sub_datas
    else:
        if class_parents > 0:
            sub_classes_list = list()
            sub_classes_list.append(class_parents)
            get_sub_classes_list(classes, sub_classes_list, class_parents)
            class_parents = sub_classes_list
        else:
            class_parents = classes
        devicetypes = get_decivetype_by_class(user.classid_id)
        datas = get_device_node(devicetypes, type_parents, class_parents) #获取节点树

    deviceinfo = dict()
    if (_id):
        device = k_device.objects.filter(id=_id)
        if len(device) == 1:
            device = device[0]
            deviceinfo['id'] = _id
            deviceinfo['brief'] = device.brief
            deviceinfo['name']  = device.name
            deviceinfo['position'] = device.position
            deviceinfo['content'] = device.content
            devicetype = k_devicetype.objects.filter(id=device.typeid_id)
            if len(devicetype) == 1:
                deviceinfo['devicetype'] = devicetype[0].name
            else:
                deviceinfo['devicetype'] = "未指定设备分类"
            owner = k_user.objects.filter(id=device.ownerid)
            if len(owner) == 1:
                deviceinfo['owner'] = owner[0].name
            else:
                deviceinfo['owner'] = "未指定负责人"
            str_spares = ''
            spares = k_spare.objects.filter(k_device=_id)
            for s in spares:
                str_spares += '%s (编号:%s, 型号:%s)'%(s.name, s.brief, s.model) + ','
            if str_spares != '':
                deviceinfo['spares'] = str_spares[0:len(str_spares)-1]
            else:
                deviceinfo['spares'] = '无'
            _m_record = k_maintenance.objects.filter(deviceid_id=_id, mtype=2).order_by('createdatetime')
            if len(_m_record) >= 1:
                deviceinfo['m_record_size'] = len(_m_record)
                _m_record = _m_record[len(_m_record)-1]
                deviceinfo['m_record_title'] = _m_record.title
                deviceinfo['m_record_content'] = _m_record.createcontent
                deviceinfo['m_createtime'] = _m_record.createdatetime
                deviceinfo['m_status'] = dict(k_maintenance.MAINTENANCE_STATUS)[_m_record.state]
                deviceinfo['m_priority'] = dict(k_maintenance.MAINTENANCE_PRIORITY)[_m_record.priority]
                if _m_record.state != '1':
                    _m_assignor = k_user.objects.filter(id = _m_record.assignorid)
                    if len(_m_assignor) == 1:
                        deviceinfo['m_assignor'] = _m_assignor[0].name
                        deviceinfo['m_assigntime'] = _m_record.assigndatetime
                        deviceinfo['has_m_assignor'] = 1
                _m_creator = k_user.objects.filter(id = _m_record.creatorid)
                if len(_m_creator) == 1:
                    deviceinfo['m_creator'] = _m_creator[0].name
                else:
                    deviceinfo['m_creator'] = "(创建者不存在!)"
                deviceinfo['has_m_record'] = 1
            else:
                deviceinfo['m_record_title'] = "暂无"
                deviceinfo['m_record_content'] = "暂无"
                deviceinfo['has_m_record'] = 0
                deviceinfo['m_record_size'] = 0
            _k_record = k_maintenance.objects.filter(deviceid_id=_id, mtype=1).order_by('createdatetime')
            if len(_k_record) >= 1:
                deviceinfo['k_record_size'] = len(_k_record)
                _k_record = _k_record[len(_k_record)-1]
                deviceinfo['k_record_title'] = _k_record.title
                deviceinfo['k_record_content'] = _k_record.createcontent
                deviceinfo['k_createtime'] = _k_record.createdatetime
                deviceinfo['k_status'] = dict(k_maintenance.MAINTENANCE_STATUS)[_k_record.state]
                deviceinfo['k_priority'] = dict(k_maintenance.MAINTENANCE_PRIORITY)[_k_record.priority]
                if _k_record.state != '1':
                    _k_assignor = k_user.objects.filter(id = _k_record.assignorid)
                    if len(_k_assignor) == 1:
                        deviceinfo['k_assignor'] = _k_assignor[0].name
                        deviceinfo['k_assigntime'] = _k_record.assigndatetime
                        deviceinfo['has_k_assignor'] = 1
                _k_creator = k_user.objects.filter(id = _k_record.creatorid)
                if len(_k_creator) == 1:
                    deviceinfo['k_creator'] = _k_creator[0].name
                else:
                    deviceinfo['k_creator'] = "(创建者不存在!)"
                deviceinfo['has_k_record'] = 1
            else:
                deviceinfo['k_record_title'] = "暂无"
                deviceinfo['k_record_content'] = "暂无"
                deviceinfo['has_k_record'] = 0
                deviceinfo['k_record_size'] = 0
            _t_record = k_meter.objects.filter(brief=device.brief).order_by('metertime')
            if len(_t_record) >= 1:
                deviceinfo['t_record_size'] = len(_t_record)
                _t_record = _t_record[len(_t_record)-1]
                _t_user = k_user.objects.filter(id=_t_record.userid_id)
                if len(_t_user) == 1:
                    deviceinfo['t_user'] = _t_user[0].name
                else:
                    deviceinfo['t_user'] = "(抄表者不存在!)"
                _t_route = k_route.objects.filter(id=_t_record.routeid_id)
                if len(_t_route) == 1:
                    deviceinfo['t_route'] = _t_route[0].name
                else:
                    deviceinfo['t_route'] = "(线路不存在!)"   
                deviceinfo['t_record_content'] = _t_record.json
                deviceinfo['t_metertime'] = _t_record.metertime
                deviceinfo['has_t_record'] = 1
            else:
                deviceinfo['has_t_record'] = 0
                deviceinfo['t_record_size'] = 0
            _c = k_class.objects.filter(id=device.classid_id)
            if len(_c) == 1:
                _c_list = list()
                _c_list.append(_c[0].name)
                _parentid = _c[0].parentid
                while True:
                    _cur = k_class.objects.filter(id=_parentid)
                    if len(_cur) != 1:
                        break
                    else:
                        _parentid = _cur[0].parentid
                        _c_list.append(_cur[0].name)
                _c_num = len(_c_list)
                deviceinfo['class'] = ''
                for i in xrange(0,_c_num):
                    deviceinfo['class'] += _c_list[_c_num-i-1] + "-"

                deviceinfo['class'] = deviceinfo['class'][0:len(deviceinfo['class'])-1]
            else:
                deviceinfo['class'] = '未指定该设备所属部门'
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''

    if len(deviceinfo) > 0:
        variables=RequestContext(request,{'username':user.username,  'useravatar': user.avatar, 'data':datas, 'server_msg':server_msg, 'deviceinfo':deviceinfo, 'purview_msg':purview_msg})
    else:
        variables=RequestContext(request,{'username':user.username,  'useravatar': user.avatar, 'data':datas, 'server_msg':server_msg, 'purview_msg':purview_msg})
    return get_purviews_and_render_to_response(request.user.username, 'device.html',variables)


@login_required
def operate_device(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''
    _id = request.GET.get('id')

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    userdata = dict()
    class_list = list()
    type_list = list()
    supplier_list = list()
    producer_list = list()
    people_list = list()
    spare_list = list()
    spare_detail_list = list()
    classes = k_class.objects.filter(id__in=result)
    for c in classes:
        class_list.append(c.name)
    #types = k_devicetype.objects.all()
    types = get_decivetype_by_class(user.classid_id)
    for t in types:
        type_list.append(t.name)
    suppliers = k_supplier.objects.all()
    for s in suppliers:
        supplier_list.append(s.name)
    producers = k_producer.objects.all()
    for p in producers:
        producer_list.append(p.name)
    spares = k_spare.objects.all()
    for s in spares:
        spare_list.append(s.name)
        tmp_dict = dict()
        tmp_dict['name'] = s.name
        tmp_dict['brief'] = s.brief
        tmp_dict['model'] = s.model
        spare_detail_list.append(tmp_dict)
        #spare_detail_list.append( {'name': s.name, 'brief': s.brief, 'model:': s.model} )
    people = k_user.objects.filter(classid__in=result)
    for p in people:
        person = dict()
        person["name"] = p.name
        _c = k_class.objects.get(id=p.classid_id)
        person["position"] = _c.name
        people_list.append(person)
    userdata['class_list'] = class_list
    userdata['dtype_list'] = type_list
    userdata['supplier_list'] = supplier_list
    userdata['producer_list'] = producer_list
    userdata['people'] = people_list
    userdata['spare_list'] = spare_list
    userdata['spare_detail_list'] = spare_detail_list
    if _id:
        thedevice = k_device.objects.filter(id = _id)[0]
        key_list = ['name', 'brand', 'brief', 'serial', 'model', 'buytime', 'content', 'qrcode', 'position', 'memo',
                    'lastmaintenance', 'nextmaintenance','maintenanceperiod', 'lastrepaire', 'spare','lastmeter', 'notice']
        for key in key_list:
            userdata[key] = eval('thedevice.'+key)
        if thedevice.producerid:
            userdata['chosen_producer'] = thedevice.producerid.name
        else:
            userdata['chosen_producer'] = '无'
        if thedevice.supplierid:
            userdata['chosen_supplier'] = thedevice.supplierid.name
        else:
            userdata['chosen_supplier'] = '无'
        userdata['chosen_class'] = thedevice.classid.name
        userdata['chosen_type'] = thedevice.typeid.name

        k_chosed_spares = k_spare.objects.filter(k_device=_id)
        chosed_spares = []
        for k_chosed_spare in k_chosed_spares:
            #chosed_spares.append( '%s(%s,%s)'%(k_chosed_spare.name, k_chosed_spare.model, k_chosed_spare.brief) )
            chosed_spares.append(k_chosed_spare.brief)
        userdata['chosen_spares'] = chosed_spares

        _owner = k_user.objects.filter(id=thedevice.ownerid)
        if len(_owner) == 1:
            _owner = _owner[0]
            userdata['chosen_owner'] = _owner.name
            _choseneditable = False
            for person in people_list:
                if userdata['chosen_owner'] == person['name']:
                    _choseneditable = True
            userdata['choseneditable'] = _choseneditable
            if _choseneditable == False:
                p = k_user.objects.filter(name=userdata['chosen_owner'])[0]
                person = dict()
                person["name"] = p.name
                _c = k_class.objects.get(id=p.classid_id)
                person["position"] = _c.name
                people_list.append(person)
    else:
        if request.GET.get('supplier_name'):
            userdata['chosen_supplier'] = request.GET.get('supplier_name')
        if request.GET.get('producer_name'):
            userdata['chosen_producer'] = request.GET.get('producer_name')
        userdata['isNew'] = True
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar, 'data': userdata, 'server_msg': server_msg})
    return get_purviews_and_render_to_response(request.user.username, 'deviceadd.html', variables)


@login_required
def deviceadd(request):
    user = User.objects.get(username=request.user.username)
    server_msg = ''
    if request.method == 'POST':
        _brief = request.POST['brief']
        _name = request.POST['name']
        _classname = request.POST['classname']
        _classid = k_class.objects.get(name=_classname)
        _typeid = k_devicetype.objects.get(name=request.POST['typename'])
        if request.POST['producer'] != "":
            _producerid = k_producer.objects.get(name=request.POST['producer'])
        else:
            _producerid = ''
        if request.POST['supplier'] != "":
            _supplierid = k_supplier.objects.get(name=request.POST['supplier'])
        else:
            _supplierid = ''
        _ownerid = ''
        tmp_name_dept = request.POST['owner'].split('#')
        if len(tmp_name_dept) == 2:
            tmp_name_classid = k_class.objects.get(name = tmp_name_dept[1])
            _ownerid_list = k_user.objects.filter(name=tmp_name_dept[0], classid=tmp_name_classid)
            if len(_ownerid_list) == 1:
                _ownerid = _ownerid_list[0]
        if _ownerid == '':
            server_msg = '责任人信息填写有误！'
            return HttpResponseRedirect('/operate_device/?msg='+server_msg)
        _devs = k_device.objects.filter(brief=_brief)
        _devs = _devs.filter(name=_name)
        if request.POST['phase'] == 'NEW':
            if len(_devs) > 0:
                _dev = _devs[0]
                server_msg = _classname+'中'+_dev.name+'('+_dev.brief+')的设备已存在！'
                return HttpResponseRedirect('/operate_device/?msg='+server_msg)

            _tmp_devs = k_device.objects.filter(brief=_brief)
            if len(_tmp_devs) > 0:
                _dev = _tmp_devs[0]
                server_msg = _classname+'中简称为:'+_dev.brief+'的设备已存在！'
                return HttpResponseRedirect('/operate_device/?msg='+server_msg)
                
            _tmp_devs = k_device.objects.filter(name=_name)
            if len(_tmp_devs) > 0:
                _dev = _tmp_devs[0]
                server_msg = _classname+'中名字为:'+_dev.name+'的设备已存在！'
                return HttpResponseRedirect('/operate_device/?msg='+server_msg)

            _device = k_device.objects.create(
                classid=_classid,
                typeid=_typeid,
                #producerid=_producerid,
                #supplierid=_supplierid,
                ownerid=_ownerid.id,
                name=request.POST['name'],
                brief=request.POST['brief'],
                brand=request.POST['brand'],
                state=request.POST['state'],
                serial=request.POST['serial'],
                model=request.POST['model'],
                buytime=request.POST['buytime'],
                content=request.POST['content'],
                position=request.POST['position'],
                memo=request.POST['memo'],
                notice=request.POST['notice'],
                maintenanceperiod = 1,
                #status=2,
                creatorid=request.user.id,
                createdatetime=get_current_date(),
                editorid=request.user.id,
                editdatetime=get_current_date()
            )
            if _supplierid != '':
                _device.supplierid = _supplierid
            if _producerid != '':
                _device.producerid = _producerid
            
            # 建立device和spare的关系
            spares_brief = request.POST.getlist('spare')
            for s_brief in spares_brief:
                spares = k_spare.objects.filter(brief=s_brief)
                for spare in spares:
                    _device.spare.add(spare.id)

            _device.save()
            server_msg = '添加设备成功！'
            return HttpResponseRedirect('/operate_device/?msg='+server_msg)
        if request.POST['phase'] == 'EDIT':
            _dev = _devs[0]
            _dev.brand = request.POST['brand']
            _dev.state = request.POST['state']
            _dev.serial = request.POST['serial']
            _dev.model = request.POST['model']
            _dev.buytime = request.POST['buytime']
            _dev.content = request.POST['content']
            _dev.position = request.POST['position']
            _dev.memo = request.POST['memo']
            _dev.notice = request.POST['notice']
            _dev.editorid = request.user.id
            _dev.editdatetime = get_current_date()
            _dev.classid = _classid
            if _producerid != '':
                _dev.producerid = _producerid
            if _supplierid != '':
                _dev.supplierid = _supplierid
            _dev.typeid = _typeid
            _dev.ownerid = _ownerid.id
            tmp_devs = _dev.spare.filter(k_device=_dev.id)
            for t_dev in tmp_devs:
                _dev.spare.remove(t_dev)
            # 建立user和role的关系
            spares_brief = request.POST.getlist('spare')
            for s_brief in spares_brief:
                spares = k_spare.objects.filter(brief=s_brief)
                for spare in spares:
                    _device.spare.add(spare.id)
            _dev.save()
            server_msg = _classname + '中' + _dev.name + '(' + _dev.brief + ')的设备信息已成功更新！'
            return HttpResponseRedirect('/operate_device/?id=' + str(_dev.id) + '&msg=' + server_msg)
    else:
        server_msg = '禁止用非法方式访问！'
        return HttpResponseRedirect('/operate_device/?msg=' + server_msg)


@login_required
def devicedel(request):
    _id = request.GET.get('id')
    if _id:
        devices = k_device.objects.filter(id=_id)
        if len(devices) == 1:
            device = devices[0]
            device.delete()
        else:
            return HttpResponseRedirect('/device/?msg="删除设备失败"')
    return HttpResponseRedirect('/device/')


@login_required
def devicebatch_add(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar,'server_msg': server_msg})
    return get_purviews_and_render_to_response(request.user.username, 'devicebatchadd.html', variables)

@login_required
def devicebatch_submit(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    if request.method == "POST":
        raw_post_data = request.body
        json_data = json.loads(raw_post_data)
        success_num = 0
        try:
            for json_key in json_data:
                obj_datas = json_data[json_key]
                for obj_data in obj_datas:
                    _brief = obj_data['brief']
                    _name = obj_data['name']
                    _classname = obj_data['classname']
                    _classid = k_class.objects.get(name=_classname)
                    _typeid = k_devicetype.objects.get(name=obj_data['typename'])
                    if obj_data['producer'] == "无":
                        _producerid = ''
                    else:
                        _producer = k_producer.objects.filter(name=obj_data['producer'])
                        if len(_producer) == 0:
                            _producerid = k_producer.objects.create(
                                name=obj_data['producer'], creatorid = request.user.id, createdatetime=get_current_date(),
                                editorid=request.user.id, editdatetime=get_current_date()
                            )
                        elif len(_producer) == 1:
                            _producerid = _producer[0]
                        else:
                            server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加生产厂家出错：'
                            return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    if obj_data['supplier'] == "无":
                        _supplierid = ''
                    else:
                        _supplier = k_supplier.objects.filter(name=obj_data['supplier'])
                        if len(_supplier) == 0:
                            _supplierid = k_supplier.objects.create(
                                name=obj_data['supplier'], creatorid = request.user.id, createdatetime=get_current_date(),
                                editorid=request.user.id, editdatetime=get_current_date()
                            )
                        elif len(_supplier) == 1:
                            _supplierid = _supplier[0]
                        else:
                            server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加供应商出错：'
                            return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    _ownerid = k_user.objects.get(username=obj_data['owner'])
                    _devs = k_device.objects.filter(brief=_brief)
                    _devs = _devs.filter(name=_name)
                    if len(_devs) > 0:
                        _dev = _devs[0]
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += _classname+'中'+_dev.name+'('+_dev.brief+')的设备已存在！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")

                    _state = 0
                    if obj_data['state'] == '运行':
                        _state = 0
                    elif obj_data['state'] == '停用':
                        _state = 1
                    elif obj_data['state'] == '故障':
                        _state = 2
                    elif obj_data['state'] == '维修':
                        _state = 3
                    else:
                        _state = 4 # error

                    _device = k_device.objects.create(
                        classid=_classid,
                        typeid=_typeid,
                        #producerid=_producerid,
                        #supplierid=_supplierid,
                        ownerid=_ownerid.id,
                        name=obj_data['name'],
                        brief=obj_data['brief'],
                        brand=obj_data['brand'],
                        state=_state,
                        serial=obj_data['serial'],
                        model=obj_data['model'],
                        buytime=obj_data['buytime'],
                        content=obj_data['content'],
                        position=obj_data['position'],
                        memo=obj_data['memo'],
                        #spare=obj_data['spare'],
                        notice=obj_data['notice'],
                        maintenanceperiod = 1,
                        #status=2,
                        creatorid=request.user.id,
                        createdatetime=get_current_date(),
                        editorid=request.user.id,
                        editdatetime=get_current_date()
                    )
                    if _supplierid != '':
                        _device.supplierid = _supplierid
                    if _producerid != '':
                        _device.producerid = _producerid
                                # 建立device和spare的关系
                    _device.save()
                    success_num += 1
            server_msg = '成功添加'+str(success_num)+'条设备信息！'
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
        except Exception as e:
            server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查所属部门、设备类别和责任人用户名是否正确！' + str(e)
            tmp_decivetype = k_devicetype.objects.filter(name=obj_data['typename'])
            if len(tmp_decivetype) <= 0:
                server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查设备类别是否正确！' + str(e)
            tmp_class = k_class.objects.filter(name=_classname)
            if len(tmp_class) <= 0:
                server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查所属部门是否正确！' + str(e)
            tmp_ownerid = k_user.objects.filter(username=obj_data['owner'])
            if len(tmp_ownerid) <= 0:
                server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查责任人用户名是否正确！' + str(e)
            #print e
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
    server_msg = "导入失败，请检查数据格式是否符合模板要求！"
    return HttpResponse(json.dumps({
        "username": user.username,
        "server_msg":server_msg
        }), content_type="application/json")

@login_required
def device_type(request):
    user = k_user.objects.get(username=request.user.username)
    #devicetypes = k_devicetype.objects.all()
    devicetypes = get_decivetype_by_class(user.classid_id)
    parents = 0
    datas = get_type_node(devicetypes, parents) #获取节点树
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
    _id = request.GET.get('id')
    if _id:
        device_info = {}
        _departs = k_devicetype.objects.filter(id=_id)
        if len(_departs) == 1:
            device_info["id"] = _id
            device_info["parent"] = "（该类型为最上级类型）"
            _parent = k_devicetype.objects.filter(id=_departs[0].parentid)
            if len(_parent) == 1:
                device_info["parent"] = _parent[0].name
            device_info["name"] = _departs[0].name
            device_info["memo"] = _departs[0].memo
            device_info["creatorid"] = _departs[0].creatorid
            _tmp_creator = k_user.objects.filter(id=_departs[0].creatorid)
            if len(_tmp_creator) == 1:
                device_info["creatorname"] = _tmp_creator[0].name
            device_info["createtime"] = _departs[0].createdatetime
            variables=RequestContext(request,{'username':user.username, 'useravatar': user.avatar, 'data':datas, 'server_msg':server_msg,
                                          'device_info':device_info})
    else:
        variables = RequestContext(request,{'username': user.username,  'useravatar': user.avatar, 'data': datas, 'server_msg': server_msg})
    return get_purviews_and_render_to_response(request.user.username, 'devicetype.html', variables)


@login_required
def device_type_add(request):
    user = k_user.objects.get(username=request.user.username)
    #k_devicetypes = k_devicetype.objects.all()
    k_devicetypes = get_decivetype_by_class(user.classid_id)
    devicetypes = list()
    for k_type in k_devicetypes:
        devicetypes.append(k_type.name)
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar, 'devicetypes': devicetypes})
    return get_purviews_and_render_to_response(request.user.username, 'devicetypeadd.html', variables)


@login_required
def device_type_submit(request):
    if not k_devicetype.objects.filter(name=request.GET.get('name')):
        _parentname = request.GET.get('parentname')
        _name = request.GET.get('name')
        _memo = request.GET.get('memo')
        _user = k_user.objects.get(username=request.user.username)
        _parent_classid = get_parent_classid(_user.classid_id)
        _id = 0
        _depth = 0
        if not have_right_to_devicemgt(_parent_classid):
            return HttpResponseRedirect('/device_type/?msg="无权限添加新的设备类型！"')
        if len(_parentname) == 0:
            _id = 0
            _depth = 0
        else:
            _parent = k_devicetype.objects.filter(name=_parentname)
            if len(_parent) == 1:
                _id = _parent[0].id
                _depth = _parent[0].depth+1
            else:
                return HttpResponseRedirect('/device_type/?msg="父级类别有误！"')
        _old_name = request.GET.get('old_name')
        cur_devicetype = k_devicetype.objects.filter(name=_old_name)
        if len(cur_devicetype) == 0:
            _type = k_devicetype.objects.create(
                name=_name,
                parentid=_id,
                depth=_depth,
                memo=_memo,
                status=_parent_classid,
                creatorid=request.user.id,
                createdatetime=get_current_date(),
                editorid=request.user.id,
                editdatetime=get_current_date()
            )
            _type.save()
            return HttpResponseRedirect('/device_type/?msg="设备类型添加成功！"')
        else:
            _type = cur_devicetype[0]
            _type.name = _name
            _type.parentid = _id
            _type.depth = _depth
            _type.memo = _memo
            _type.status = _parent_classid
            _type.editorid = request.user.id
            _type.editdatetime = get_current_date()
            _type.save()
            return HttpResponseRedirect('/device_type/?msg="设备类型名称修改成功！"')
    else:
        return HttpResponseRedirect('/device_type/?msg="该设备类型名称已存在！"')


@login_required
def device_type_revise(request):
    _id = request.GET.get('id')
    if _id:
        user = k_user.objects.get(username=request.user.username)
        k_devicetypes = k_devicetype.objects.all()
        devicetypes = list()
        for k_type in k_devicetypes:
            devicetypes.append(k_type.name)
        _dtype = k_devicetype.objects.filter(id=_id)
        if len(_dtype) == 1:
            name = _dtype[0].name
            parentid = _dtype[0].parentid
            _parenttype = k_devicetype.objects.filter(id=parentid)
            chosentype=''
            if len(_parenttype) == 1:
                chosentype = _parenttype[0].name
            else:
                chosentype = "" #顶层，无父级设备类型
            variables = RequestContext(request, {
                'username': user.username,
                'useravatar': user.avatar,
                'devicetypes': devicetypes,
                'isExisted': False,
                'name':name,
                'chosentype':chosentype
            })
        elif len(_dtype) == 0:
            HttpResponseRedirect('/device_type/?msg="该设备类型不存在！"')
        else:
            HttpResponseRedirect('/device_type/?msg="该设备类型在数据库中存储错误！"')
        return get_purviews_and_render_to_response(request.user.username, 'devicetypeadd.html', variables)
    else:
        HttpResponseRedirect('/device_type/?msg="非法访问！"')


@login_required
def device_type_del(request):
    _id = request.GET.get('id')
    if _id:
        _devicetype = k_devicetype.objects.filter(id=_id)
        if len(_devicetype) == 1:
            _device = k_device.objects.filter(typeid_id=_id)
            if len(_device) > 0:
                msg = "有"+str(len(_device))+"个设备属于该设备类型，无法删除设备类型："+_devicetype[0].name
            else:
                msg = "成功删除设备类型："+_devicetype[0].name
                _devicetype[0].delete()
        else:
            msg = "该部门不存在！"
        return HttpResponseRedirect('/device_type/?msg='+msg)
    else:
        return HttpResponseRedirect('/device_type/')


def supplier(request):
    user = k_user.objects.get(username=request.user.username)
    _suppliers = k_supplier.objects.all()
    data = []
    for _supplier in _suppliers:
        data.append({
            'name': _supplier.name,
            'contact': _supplier.contact,
            'address': _supplier.addr,
            'linkman':_supplier.linkman,
            'mobile': _supplier.mobile,
            'memo': _supplier.memo,
        })
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''
    return get_purviews_and_render_to_response(request.user.username, 'supplier.html', {'data': data, 'username': user.username,
                                                                                        'useravatar': user.avatar, 'server_msg':server_msg})


@login_required
def add_supplier(request):
    user = k_user.objects.get(username=request.user.username)
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'supplieradd.html', variables)

@login_required
def del_supplier(request):
    _name = request.GET.get('name')
    if _name:
        _supplier = k_supplier.objects.get(name=_name)
        _supplier.delete()
    return HttpResponseRedirect('/supplier/')

@login_required
def submit_supplier(request):
    if request.method == 'POST':
        #修改供应商
        _supplier = k_supplier.objects.filter(name = request.POST.get('name'))
        if _supplier:
            _supplier = _supplier[0]
            _supplier.contact = request.POST.get('contact')
            _supplier.addr = request.POST.get('address')
            _supplier.linkman = request.POST.get('linkman')
            _supplier.mobile = request.POST.get('mobile')
            _supplier.memo = request.POST.get('memo')
            _supplier.editorid = request.user.id
            _supplier.editdatetime = get_current_date()
            _supplier.save()
            return HttpResponseRedirect('/supplier/')
    else:
        #添加供应商
        if not (k_supplier.objects.filter(name = request.GET.get('name')) or k_supplier.objects.filter(name = request.GET.get('supplier_name'))):
            if request.GET.get('name'):
                _name = request.GET.get('name')
                _contact = request.GET.get('contact')
                _address = request.GET.get('address')
                _linkman = request.GET.get('linkman')
                _mobile = request.GET.get('mobile')
                _memo = request.GET.get('memo')
                _supplier = k_supplier.objects.create(name=_name, contact=_contact,addr=_address,memo=_memo,linkman=_linkman,mobile=_mobile,
                                                      creatorid = request.user.id, createdatetime=get_current_date(),
                                                      editorid=request.user.id, editdatetime=get_current_date())
                _supplier.save()
                return HttpResponseRedirect('/supplier/')
            elif request.GET.get('supplier_name'):
                _name = request.GET.get('supplier_name')
                _contact = request.GET.get('supplier_contact')
                _address = request.GET.get('supplier_address')
                _linkman = request.GET.get('supplier_linkman')
                _mobile = request.GET.get('supplier_mobile')
                _memo = request.GET.get('supplier_memo')
                _supplier = k_supplier.objects.create(name=_name, contact=_contact,addr=_address,memo=_memo,linkman=_linkman,mobile=_mobile,
                                                      creatorid = request.user.id, createdatetime=get_current_date(),
                                                      editorid=request.user.id, editdatetime=get_current_date())
                _supplier.save()
                return HttpResponseRedirect('/operate_device/?supplier_name='+_name)
            else:
                return HttpResponseRedirect('/supplier/?msg="非法请求！"')
        else:
            return HttpResponseRedirect('/supplier/?msg="该供应商已存在！"')
    return HttpResponseRedirect('/supplier/')


@login_required
def producer(request):
    user = k_user.objects.get(username=request.user.username)
    _producers = k_producer.objects.all()
    data = []
    for _producer in _producers:
        data.append({
            'name': _producer.name,
            'contact': _producer.contact,
            'address': _producer.addr,
            'linkman':_producer.linkman,
            'mobile': _producer.mobile,
            'memo': _producer.memo,
        })
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''
    return get_purviews_and_render_to_response(request.user.username, 'producer.html', {'data': data, 'username': user.username,
                                                                                        'useravatar': user.avatar, 'server_msg':server_msg})


@login_required
def add_producer(request):
    user = k_user.objects.get(username=request.user.username)
    variables = RequestContext(request, {'username': user.username,  'useravatar': user.avatar, 'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'produceradd.html', variables)


@login_required
def del_producer(request):
    _name = request.GET.get('name')
    if _name:
        _producer = k_producer.objects.get(name=_name)
        _producer.delete()
    return HttpResponseRedirect('/producer/')


@login_required
def submit_producer(request):
    if request.method == 'POST':
        # 修改供应商
        _producer = k_producer.objects.filter(name=request.POST.get('name'))
        if _producer:
            _producer = _producer[0]
            _producer.contact = request.POST.get('contact')
            _producer.addr = request.POST.get('address')
            _producer.linkman = request.POST.get('linkman')
            _producer.mobile = request.POST.get('mobile')
            _producer.memo = request.POST.get('memo')
            _producer.editorid = request.user.id
            _producer.editdatetime = get_current_date()
            _producer.save()
            return HttpResponseRedirect('/producer/')
    else:
        #添加供应商
        if not (k_producer.objects.filter(name = request.GET.get('name')) or k_producer.objects.filter(name = request.GET.get('producer_name'))):
            # 本页面还是从设备添加页面
            if request.GET.get('name'):
                _name = request.GET.get('name')
                _contact = request.GET.get('contact')
                _address = request.GET.get('address')
                _linkman = request.GET.get('linkman')
                _mobile = request.GET.get('mobile')
                _memo = request.GET.get('memo')
                _producer = k_producer.objects.create(name=_name, contact=_contact,addr=_address,memo=_memo,linkman = _linkman,mobile=_mobile,
                                                      creatorid = request.user.id, createdatetime=get_current_date(),
                                                      editorid=request.user.id, editdatetime=get_current_date())
                _producer.save()
                return HttpResponseRedirect('/producer/')
            elif request.GET.get('producer_name'):
                _name = request.GET.get('producer_name')
                _contact = request.GET.get('producer_contact')
                _address = request.GET.get('producer_address')
                _linkman = request.GET.get('producer_linkman')
                _mobile = request.GET.get('producer_mobile')
                _memo = request.GET.get('producer_memo')
                _producer = k_producer.objects.create(name=_name, contact=_contact,addr=_address,memo=_memo,linkman = _linkman,mobile=_mobile,
                                                      creatorid = request.user.id, createdatetime=get_current_date(),
                                                      editorid=request.user.id, editdatetime=get_current_date())
                _producer.save()
                return HttpResponseRedirect('/operate_device/?producer_name='+_name)
            else:
                return HttpResponseRedirect('/producer/?msg="非法请求！"')
        else:
            return HttpResponseRedirect('/producer/?msg="该生产厂家已存在！"')


# 个人信息
@login_required
def profile(request):
    if request.method == "GET":
        user = k_user.objects.get(username=request.user.username)
        variables = RequestContext(request, {'userinfo': user, 'username': user.username, 'useravatar': user.avatar})
        return get_purviews_and_render_to_response(request.user.username, 'profile.html', variables)
    else:
        user = k_user.objects.filter(username=request.POST['username'])
        if len(user) == 1:
            user = user[0]
            user.name = request.POST['name']
            user.email = request.POST['email']
            user.mobile = request.POST['mobile']
            user.gender = request.POST['gender']
            user.address = request.POST['address']
            user.birthday = datetime.strptime(request.POST['birthday'], '%Y-%m-%d').date()
            user.editorid = request.user.id
            user.editdatetime = get_current_date()
            user.save()
            msg = "修改用户信息成功！"
        else:
            msg = "用户名不存在，修改用户信息失败！"

        user = k_user.objects.get(username=request.user.username)
        variables = RequestContext(request, {'userinfo': user, 'msg': msg, 'username': user.username, 'useravatar': user.avatar})
        return get_purviews_and_render_to_response(request.user.username, 'profile.html', variables)


def change_password(request):
    if request.method == "POST":
        old_password = request.POST['old-password']
        new_password = request.POST['new-password']
        user = authenticate(username=request.user.username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            msg = "修改密码成功！"
        else:
            msg = "旧密码错误，修改密码失败！"

        user = k_user.objects.get(username=request.user.username)
        return render_to_response('profile.html', {
            'user': user,
            'useravatar': user.avatar,
            "msg": msg
        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/profile/")


def change_avatar(request):
    filename = handle_uploaded_file(request.user.username, request.FILES['avatar'])
    user = k_user.objects.get(username=request.user.username)
    user.avatar = filename
    user.save()
    return HttpResponse(json.dumps({
            "username": request.user.username,
            "useravatar":filename,
            "status":"OK"
            }
        ), content_type="application/json")

@login_required
def setting(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username, 'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'setting.html', variables)


# 注册, 创建一个新用户
def register(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            user = k_user.objects.create(username=username, password=password, classid_id=1, roles=1)
            olduser = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=user.password
            )
            user.save()
            olduser.save()
            return HttpResponse('register success!!')
    else:
        uf = UserForm()
    return render_to_response('register.html', {'uf': uf}, context_instance=RequestContext(req))


# 处理登录请求
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            # user = k_user.objects.filter(username = username,password = password)
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                kuser = k_user.objects.filter(username = username)
                if len(kuser) == 1:
                    return HttpResponseRedirect('/')
                else:
                    variables = RequestContext(request, {'msg': "数据库中存在重名用户！请联系管理员！"})
                    return render_to_response('login.html', variables)
            else:
                variables = RequestContext(request, {'msg': "用户名不存在或密码错误！"})
                return render_to_response('login.html', variables)
        else:
                variables = RequestContext(request, {'msg': "用户名不存在或密码错误！"})
                return render_to_response('login.html', variables)
    else:
        return render_to_response('login.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')


def deviceall(request):
    if request.method == 'POST':
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        brief = request.POST.get("brief")
        if brief:
            thedevice = k_device.objects.filter(brief = brief)[0]
            newbrief = request.POST.get("newbrief")
            if newbrief:
                thedevice.brief = newbrief
                thedevice.save()
            else:
                fieldname = request.POST.get("fieldname")
                fielddata = request.POST.get("fielddata")
                exec("thedevice."+fieldname+"="+fielddata)
                thedevice.save()
    alldevice = k_device.objects.all()
    devicedata = []
    for d in alldevice:
        onedevice = dict()
        theclass = k_class.objects.filter(id = d.classid_id)
        onedevice["classid"] = theclass[0].id
        onedevice["name"] = d.name
        onedevice["brief"] = d.brief
        onedevice["brand"] = d.brand
        theproducer = k_producer.objects.filter(id = d.producerid_id)
        onedevice["producer"] = theproducer[0].name
        thesupplier = k_supplier.objects.filter(id = d.supplierid_id)
        onedevice["supplier"] = thesupplier[0].name
        thedevicetype = k_devicetype.objects.filter(id = d.typeid_id)
        onedevice["typeid"] = thedevicetype[0].id
        onedevice["state"] = d.state
        onedevice["serial"] = d.serial
        onedevice["model"] = d.model
        ### here
        onedevice["buytime"] = '2015/3/19'
        onedevice["content"] = d.content
        onedevice["memo"] = d.memo
        devicedata.append(onedevice)
    response = {}
    response["data"] = devicedata
    response["options"] = []
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(json.dumps(response))


@login_required
def purview(request):
    allpurview = k_purview.objects.all()
    purviewdata = []
    for p in allpurview:
        onepurview = dict()
        theclass = k_class.objects.filter(id=p.classid_id)
        onepurview["class"] = theclass[0].name
        onepurview["name"] = p.name
        onepurview["item"] = p.item
        onepurview["memo"] = p.memo
        thecreator = k_user.objects.filter(id=p.creatorid)
        onepurview["creator"] = thecreator[0].username
        onepurview["createdatetime"] = '2015/4/12'
        theeditor = k_user.objects.filter(id=p.editorid)
        onepurview["editor"] = theeditor[0].username
        onepurview["editdatetime"] = get_current_time()
        purviewdata.append(onepurview)
    response = {}
    response["aaData"] = purviewdata
    #response["sInfo"] = ""
    #response["iTotalRecords"] = 11
    #response["iTotalDisplayRecords"] = 11
    response["options"] = []
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(json.dumps(response))


@login_required
def add_schedule(request):
    current_user = k_user.objects.get(username=request.user.username)
    _class = current_user.classid

    route_id = int(request.POST.get('route_id'))
    route = k_route.objects.get(id=route_id)

    user_ids = request.POST.getlist('users')
    users = [k_user.objects.get(id=int(user_id)) for user_id in user_ids]

    _date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()

    schedules = k_schedule.objects.filter(route=route, date=_date)
    for s in schedules:
        s.delete()

    for user in users:
        k_schedule.objects.create(classid=_class, route=route, user=user, date=_date)

    return HttpResponse(json.dumps({
        'success': True,
        'info': 'Add Schedule Success!'
    }))


@login_required
def delete_schedule(request):
    route_id = int(request.POST.get('route_id'))
    route = k_route.objects.get(id=route_id)

    _date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()

    schedules = k_schedule.objects.filter(route=route, date=_date)

    for s in schedules:
        s.delete()

    return HttpResponse(json.dumps({
        'success': True,
        'info': 'Delete Schedule Success!'
    }))


@login_required
def view_schedule(request):
    kuser = k_user.objects.get(username=request.user.username)
    result = [kuser.classid.id]
    get_class_set(result, kuser.classid.id)
    if request.method == 'GET':
        users = k_user.objects.filter(classid__in=result)
        user_data = [{'id': user.id, 'name': user.name, 'department': user.classid.name} for user in users]

        routes = k_route.objects.filter(classid__in=result)
        route_data = [{'id': r.id, 'name': r.name, 'startTime': r.starttime, 'period': r.period} for r in routes]

        return get_purviews_and_render_to_response(request.user.username, 'schedule.html', {'routes': route_data,
                                                                                            'users': user_data,
                                                                                            'username': kuser.username,
                                                                                            'useravatar': kuser.avatar})
    else:
        routes = k_route.objects.filter(classid__in=result)
        route_data = [{'id': _r.id, 'name': _r.name, 'startTime': str(_r.starttime), 'period': _r.period} for _r in routes]

        available_shifts = k_schedule.objects.filter(
            date__range=[date.today() - timedelta(days=30), date.today() + timedelta(days=80)],
            classid__in=result
        )
        existed_dates = [_d['date'] for _d in available_shifts.values('date').distinct()]

        shift_data = {}
        for day in existed_dates:
            day_shifts = []
            available_day_shifts = available_shifts.filter(date=day)
            for r in route_data:
                try:
                    available_day_route_shifts = available_day_shifts.filter(route=r['id'])
                except Exception, e:
                    print e
                if available_day_route_shifts.exists():
                    r['users'] = [dd['user'] for dd in available_day_route_shifts.values('user').distinct()]
                    day_shifts.append(r.copy())
            shift_data[str(day)] = day_shifts

        return HttpResponse(json.dumps({'shifts': shift_data}))


@login_required
def auto_schedule(request):
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    route_ids = [int(r) for r in request.POST.getlist('routes')]

    time_length = request.POST.get('time_length', 1)
    d = {'week1': 1, 'week2': 2, 'month1': 4, 'month2': 8}
    num_week = d[time_length]

    day_start = date.today() - timedelta(days=date.today().weekday())
    schedules = k_schedule.objects.filter(
        date__range=[day_start, day_start + timedelta(days=80)],
        classid__in=result
    )

    for i in range(7):
        day = day_start + timedelta(days=i)
        source_schedules = schedules.filter(date=day, route__in=route_ids)
        for k in range(num_week):
            target_date = day + timedelta(days=7*(k+1))
            existed_schedules = schedules.filter(date=target_date, route__in=route_ids)
            for s in existed_schedules:
                s.delete()
            if request.POST.get('operation') == 'copy':
                for s in source_schedules:
                    k_schedule.objects.create(classid=s.classid, route=s.route, user=s.user, date=target_date)
            else:  # operation = delete
                pass

    return HttpResponseRedirect('/view_schedule/')


@login_required
def view_role(request):
    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    allrole = k_role.objects.filter(classid__in=result)

    roledata = []
    for p in allrole:
        onerole = {}
        onerole["id"] = p.id
        onerole['classname'] = p.classid.name
        onerole["name"] = p.name
        onerole["purviews"] = []
        therolepurviews = p.purviews.all()
        lastname = ""
        nowitem = ""
        for i in xrange(0, len(therolepurviews)):
            q = therolepurviews[i]
            if q.name == lastname:
                nowitem += ", "+q.item
            elif q.name != lastname:
                if lastname != "":
                    onepurview = {}
                    onepurview["name"] = lastname
                    onepurview["item"] = nowitem
                    onerole["purviews"].append(onepurview)
                lastname = q.name
                nowitem = q.item
            if i == len(therolepurviews) - 1:
                onepurview = {}
                onepurview["name"] = lastname
                onepurview["item"] = nowitem
                onerole["purviews"].append(onepurview)
        onerole["memo"] = p.memo
        therole = k_role.objects.get(name=p.name)
        try:
            thecreator = k_user.objects.get(id=p.creatorid)
            onerole["creator"] = thecreator.username
        except ObjectDoesNotExist:
            onerole["creator"] = '该用户已被删除'
        onerole["createdatetime"] = therole.createdatetime
        try:
            theeditor = k_user.objects.get(id=p.editorid)
            onerole["editor"] = theeditor.username
        except ObjectDoesNotExist:
            onerole["editor"] = '该用户已被删除'
        onerole["editdatetime"] = therole.editdatetime
        roledata.append(onerole)
    return get_purviews_and_render_to_response(request.user.username, 'roleview.html', {'username': user.username, 'useravatar': user.avatar,'data': roledata})


@login_required
def operate_role(request):
    theid = request.GET.get("id")
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ""

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _classes = []
    _allclasses = k_class.objects.filter(id__in=result)
    for _class in _allclasses:
        _classes.append(_class.name)
    user = k_user.objects.get(username=request.user.username)
    if theid:
        roledata = {}
        therole = k_role.objects.get(id=theid)
        roledata["id"] = therole.id
        roledata["name"] = therole.name

        therolepurviews = therole.purviews.all()
        purview_ids = []
        for q in therolepurviews:
            purview_ids.append(q.id)
        roledata["memo"] = therole.memo
        try:
            thecreator = k_user.objects.get(id=therole.creatorid)
            roledata["creator"] = thecreator.username
        except ObjectDoesNotExist:
            roledata["creator"] = '该用户已被删除'
        roledata["createdatetime"] = therole.createdatetime
        try:
            theeditor = k_user.objects.get(id=therole.editorid)
            roledata["editor"] = theeditor.username
        except ObjectDoesNotExist:
            roledata["editor"] = '该用户已被删除'
        roledata["editdatetime"] = therole.editdatetime
        roledata['classname'] = therole.classid.name

        all_purview = k_purview.objects.all()
        roledata["purviews"] = []
        for _purview in all_purview:
            roledata['purviews'].append({
                'id': _purview.id,
                'name': _purview.name + ', ' + _purview.item,
                'selected': _purview.id in purview_ids
            })
        return get_purviews_and_render_to_response(request.user.username, 'roleoperate.html', {'username':user.username,'useravatar': user.avatar,'isNew': False, 'data': roledata, "classes": _classes, 'server_msg': server_msg})
    else:
        data = {}
        data['purviews'] = []
        purviews = k_purview.objects.all()
        for p in purviews:
            data['purviews'].append({
                'id': p.id,
                'name': p.name + ', ' + p.item,
                'selected': False
            })

        return get_purviews_and_render_to_response(request.user.username, 'roleoperate.html', {'username':user.username,'useravatar': user.avatar,'isNew': True, 'data': data, "classes": _classes, 'server_msg': server_msg})


@login_required
def delete_role(request):
    _id = request.GET.get('id')
    if _id:
        _role = k_role.objects.get(id=_id)
        _role.delete()
    return HttpResponseRedirect('/view_role/')


@login_required
def submit_role(request, _id=''):
    _classname = request.GET.get('classname')
    _name = request.GET.get('name')
    _editdatetime = get_current_date()
    # 编辑者
    _user = k_user.objects.get(username=request.user.username)
    _editor = _user.id
    _purviews = request.GET.getlist('duallistbox')
    _memo = request.GET.get('memo')

    _class = k_class.objects.get(name=_classname)
    if _id:
        _role = k_role.objects.get(id=_id)
        _role.classid = _class
        _roles = k_role.objects.filter(name=_name)
        if len(_roles) > 1 or (len(_roles) == 1 and _roles[0].id != int(_id)):
            server_msg = '名称为'+_roles[0].name+'的角色已存在！'
            return HttpResponseRedirect('/operate_role/?msg='+server_msg+'&id='+_id)
    else:
        _roles = k_role.objects.filter(name=_name)
        if len(_roles) > 0:
            server_msg = '名称为'+_roles[0].name+'的角色已存在！'
            return HttpResponseRedirect('/operate_role/?msg='+server_msg)
        _role = k_role.objects.create(classid=_class)
        _role.creatorid = _editor
    _role.name = _name
    _role.editdatetime = _editdatetime
    _role.editorid = _editor
    _role.purviews = _purviews
    _role.memo = _memo

    _role.save()
    return HttpResponseRedirect('/view_role/')


@login_required
def view_route(request):
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    routes = k_route.objects.filter(classid__in=result)
    data = []
    for r in routes:
        route = {}
        _class = k_class.objects.get(id=r.classid_id)
        route['id'] = r.id
        route['class'] = _class.name
        if r.formid:
            route['forms'] = ', '.join('form' + _form_id for _form_id in r.formid.split(','))
        else:
            route['forms'] = '暂未指定路线设备'
        route['name'] = r.name
        route['startTime'] = r.starttime
        route['endTime'] = r.endtime
        route['period'] = r.period
        try:
            route['creator'] = k_user.objects.get(id=r.creatorid).username
        except ObjectDoesNotExist:
            route['creator'] = '该用户已被删除'
        route['createTime'] = r.createdatetime
        try:
            route['editor'] = k_user.objects.get(id=r.editorid).username
        except ObjectDoesNotExist:
            route['editor'] = '该用户已被删除'
        route['editTime'] = r.editdatetime
        #route['status'] = r.status
        data.append(route)
    return get_purviews_and_render_to_response(request.user.username, 'routeview.html', {'routes': data, 'username':user.username, 'useravatar': user.avatar})


@login_required
def operate_route(request):
    user = k_user.objects.get(username=request.user.username)

    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    data = {}
    _id = request.GET.get('id')

    if _id:
        # 修改路线
        _route = k_route.objects.get(id=_id)
        data['id'] = _route.id
        _forms = _route.formid.split(',')
        data['name'] = _route.name
        data['startTime'] = _route.starttime
        data['endTime'] = _route.endtime
        data['period'] = _route.period
        try:
            data['creator'] = k_user.objects.get(id=_route.creatorid).username
        except ObjectDoesNotExist:
            data['creator'] = '该用户已被删除'
        data['createTime'] = _route.createdatetime
        try:
            data['editor'] = k_user.objects.get(id=_route.editorid).username
        except ObjectDoesNotExist:
            data['editor'] = '该用户已被删除'
        data['editTime'] = _route.editdatetime

        all_form = k_form.objects.filter(classid__in=result)
        data['forms'] = []
        for _form in all_form:
            _device = k_device.objects.get(brief=_form.brief)
            data['forms'].append({
                'id': _form.id,
                'brief': _form.brief,
                'name': _device.name,
                'selected': str(_form.id) in _forms
            })

        data['routeString'] = _route.formid

        return get_purviews_and_render_to_response(request.user.username, 'routeoperate.html', {'isNew': False, 'data': data,
                                                                                                'username':user.username, 'useravatar': user.avatar})
    else:
        # 添加路线
        all_form = k_form.objects.filter(classid__in=result)
        data['forms'] = []
        for _form in all_form:
            try:
                _device = k_device.objects.get(brief=_form.brief)
            except ObjectDoesNotExist:
                # 表单（设备）中的简称不存在
                continue
            data['forms'].append({
                'id': _form.id,
                'brief': _form.brief,
                'name': _device.name,
                'selected': False
            })
        return get_purviews_and_render_to_response(request.user.username, 'routeoperate.html', {'isNew': True, 'data': data,
                                                                                                'username':user.username, 'useravatar': user.avatar})


@login_required
def submit_route(request, _id=''):
    _user = k_user.objects.get(username=request.user.username)
    _editor = _user.id
    error_list = []
    _forms = request.POST.get('routeString')
    _name = request.POST.get('name')
    _period = request.POST.get('period')
    # _start_time = request.GET.get('startTime')
    _start_hour = request.POST.get('startHour')
    _start_minute = request.POST.get('startMinute')
    _start_time = _start_hour + ':' + _start_minute
    _end_hour = request.POST.get('endHour')
    _end_minute = request.POST.get('endMinute')
    _end_time = _end_hour + ':' + _end_minute
    _edit_time = get_current_date()
    if _id:
        route = k_route.objects.get(id=_id)
    else:
        route = k_route(classid=_user.classid)
        route.creatorid = _editor

    route.name = _name
    route.formid = _forms
    try:
        route.starttime = datetime.strptime(_start_time, '%H:%M').time()
    except ValueError:
        _start_time = _start_time.replace('24:', '0:')
        route.starttime = datetime.strptime(_start_time, '%H:%M').time()
    try:
        route.endtime = datetime.strptime(_end_time, '%H:%M').time()
    except ValueError:
        _end_time = _end_time.replace('24:', '0:')
        route.endtime = datetime.strptime(_end_time, '%H:%M').time()
    route.period = _period
    route.editorid = _editor
    route.editdatetime = _edit_time

    route.save()

    return HttpResponseRedirect('/view_route/')


@login_required
def delete_route(request):
    _id = request.GET.get('id')
    if _id:
        _route = k_route.objects.get(id=_id)
        _route.delete()
    return HttpResponseRedirect('/view_route/')


@login_required
def view_form(request):
    user = k_user.objects.get(username=request.user.username)
    _id = request.GET.get('id')
    if _id:
        _device = k_device.objects.get(id=_id)
        _brief = _device.brief
    else:
        _brief = request.GET.get('brief')
        _device = k_device.objects.get(brief=_brief)
    _form = k_form.objects.filter(brief=_brief)
    if len(_form) == 0:
        _form = k_form.objects.create(classid=_device.classid,brief=_brief)
    else:
        _form = _form[0]
    _formitems = k_formitem.objects.filter(formid_id=_form.id)
    devices = k_form.objects.all()
    _devices = list()
    for d in devices:
        _devices.append(d.brief)
    return get_purviews_and_render_to_response(request.user.username, 'formview.html', {'brief': _brief, 'formid': _form.id, 'data': _formitems, 'devices': _devices,
                                                                                        'username':user.username, 'useravatar': user.avatar})
   
@login_required
def set_template_form(request):
    template_brief = request.GET.get('template_brief')
    _form = k_form.objects.filter(brief=template_brief)
    if len(_form) > 0:
        _form = _form[0]
        formitems = k_formitem.objects.filter(formid_id=_form.id)
        _formitems = list()
        datatypelist = list()
        datatype2str = dict(k_formitem.FORM_DATATYPE)
        for fi in formitems:
            datatypelist.append( datatype2str[str(fi.datatype)] )
            temp = serializers.serialize('json', [fi,])
            struct = json.loads(temp)
            _formitems.append(struct[0])
        return HttpResponse(json.dumps({
            'flag': 1,
            'formitems': _formitems,
            'datatypes': datatypelist,
            'length': len(_formitems)
            }
        ), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "flag": 0
            }
        ), content_type="application/json")


@login_required
def submit_template_form(request):
    template_brief = request.GET.get('template_brief')
    device_brief = request.GET.get('device_brief')
    # _form = k_form.objects.filter(brief=template_brief)
    # if len(_form) > 0:
    #     _form = _form[0]
    #     formitems = k_formitem.objects.filter(formid_id=_form.id)
    #     _formitems = list()
    #     datatypelist = list()
    #     datatype2str = dict(k_formitem.FORM_DATATYPE)
    #     for fi in formitems:
    #         datatypelist.append( datatype2str[str(fi.datatype)] )
    #         temp = serializers.serialize('json', [fi,])
    #         struct = json.loads(temp)
    #         _formitems.append(struct[0])
    if 1:
        return HttpResponse(json.dumps({
            'flag': 1,
            #'formitems': _formitems,
            #'datatypes': datatypelist,
            'msg': device_brief
            }
        ), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "flag": 0
            }
        ), content_type="application/json")


@login_required
def submit_form(request):
    _brief = request.GET.get('brief')

    _name = request.GET.get('name')
    _datatype = request.GET.get('datatype')
    _unit = request.GET.get('unit')
    _lowerthreshold = request.GET.get('lowerthreshold')
    _upperthreshold = request.GET.get('upperthreshold')
    _choices = request.GET.get('choices')
    _memo = request.GET.get('memo')

    _id = request.GET.get('id')
    _formid = request.GET.get('formid')
    _user = k_user.objects.get(username=request.user.username)

    if _formid == "":
        _formitem = k_formitem.objects.get(id=_id)
        _formitem.editorid = _user.id
        _formitem.editdatetime = get_current_date()
    else:
        _form = k_form.objects.get(brief=_brief)
        _formitem = k_formitem.objects.create(classid=_form.classid, formid_id=_formid)
        _formitem.creatorid = _user.id
        _formitem.createdatetime = get_current_date()
    _formitem.name = _name
    if _datatype == 'numeric':
        _formitem.datatype = 0
        _formitem.unit = _unit
        _formitem.lowerthreshold = _lowerthreshold
        _formitem.upperthreshold = _upperthreshold
        _formitem.choices = '-'
    if _datatype == 'optional':
        _formitem.datatype = 1
        _formitem.unit = '-'
        _formitem.lowerthreshold = '-'
        _formitem.upperthreshold = '-'
        _formitem.choices = _choices
    _formitem.memo = _memo

    _formitem.save()
    return HttpResponseRedirect('/view_form/?brief='+_brief)


@login_required
def delete_form(request):
    _id = request.GET.get('id')
    _brief = request.GET.get('brief')
    if _id:
        _formitem = k_formitem.objects.get(id=_id)
        _formitem.delete()
    return HttpResponseRedirect('/view_form/?brief='+_brief)


@login_required
def deviceplanbatch_add(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username':user.username, 'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'deviceplanbatchadd.html', variables)

@login_required
def deviceplanbatch_submit(request):
    # 登陆成功
    _user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': _user.username})
    if request.method == "POST":
        raw_post_data = request.body
        json_data = json.loads(raw_post_data)
        success_num = 0
        try:
            for json_key in json_data:
                obj_datas = json_data[json_key]
                for obj_data in obj_datas:
                    _brief = obj_data['brief']
                    _title = obj_data['title']
                    _editor = obj_data['maintainer']
                    _period = obj_data['period']
                    _createcontent = obj_data['createcontent']
                    _memo = obj_data['memo']
                    try:
                        _editor = k_user.objects.get(name=_editor)
                        _device = k_device.objects.get(brief=_brief)
                        _deviceid = str(_device.id)
                        _periodstring = dict(k_deviceplan.DEVICEPLAN_PERIODS)[_period]
                    except:
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加出错：'
                        return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    _maintenance = k_maintenance.objects.create(mtype=1,classid=_user.classid,deviceid_id=_deviceid,state=2)
                    _deviceplan = k_deviceplan.objects.create(deviceid_id=_deviceid,maintenanceid=_maintenance)
                    _maintenance.creatorid = _user.id
                    _maintenance.assignorid = _user.id
                    _maintenance.assigndatetime = get_current_time()
                    _maintenance.title = _title
                    _maintenance.createcontent = _createcontent
                    _maintenance.editorid = _editor.id
                    _maintenance.memo = _memo+"（周期为："+dict(k_deviceplan.DEVICEPLAN_PERIODS)[_period]+"）"
                    _maintenance.state = 2
                    _maintenance.save()

                    _deviceplan.assignorid = _user.id
                    _deviceplan.assigndatetime = get_current_date()
                    _deviceplan.title = _title
                    _deviceplan.period = _period
                    _deviceplan.createcontent = _createcontent
                    _deviceplan.editorid = _editor.id
                    _deviceplan.memo = _memo
                    _deviceplan.save()

                    success_num += 1
            server_msg = '成功添加'+str(success_num)+'条工具信息！'
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
        except Exception as e:
            server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查填写是否正确！'
            print e
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
    server_msg = "导入失败，请检查数据格式是否符合模板要求！"
    return HttpResponse(json.dumps({
        "username": _user.username,
        "server_msg":server_msg
        }), content_type="application/json")


@login_required
def view_deviceplan(request):
    #权限判断
    # _msg = check_purview(request.user.username, 28)
    # if _msg != 0:
    #     return HttpResponseRedirect('/device/?msg='+_msg)

    _deviceid = request.GET.get('id')
    _device = k_device.objects.get(id=_deviceid)
    _brief = _device.brief
    _deviceplans = k_deviceplan.objects.filter(deviceid=_device)
    data = []
    for _deviceplan in _deviceplans:
        try:
            _assignor = k_user.objects.get(id=_deviceplan.assignorid).name
        except ObjectDoesNotExist:
            _assignor = '该用户已被删除'
        try:
            _editor = k_user.objects.get(id=_deviceplan.editorid).name
        except ObjectDoesNotExist:
            _editor = '该用户已被删除'
        data.append({
            'id': _deviceplan.id,
            'title': _deviceplan.title,
            'period': _deviceplan.get_period_display(),
            'createcontent': _deviceplan.createcontent,
            'memo': _deviceplan.memo,
            'assignor': _assignor,
            'assigndatetime': _deviceplan.assigndatetime,
            'editor': _editor
        })

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _users = k_user.objects.filter(classid__in=result)
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'deviceplanview.html', {'brief': _brief, 'deviceid': _deviceid, 'data': data,
                                                                                              'maintainers': _maintainers, 'purview_msg': purview_msg,
                                                                                              'username':user.username,'useravatar': user.avatar})


@login_required
def add_deviceplan(request):
    #权限判断
    # _msg = check_purview(request.user.username, 33)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)
    
    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _users = k_user.objects.filter(classid__in=result)
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    _devices = k_device.objects.filter(classid__in=result)
    # _briefs = []
    # for _device in _devices:
    #     _briefs.append(_device.brief)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'deviceplanadd.html', {'maintainers': _maintainers, 'devices': _devices,
                                                                                              'purview_msg': purview_msg,
                                                                                              'username':user.username,
                                                                                              'useravatar': user.avatar})

@login_required
def submit_deviceplan(request):
    _deviceid = request.GET.get('deviceid')
    if _deviceid == None:
        _brief = request.GET.get('brief')
        _device = k_device.objects.get(brief=_brief)
        _deviceid = str(_device.id)
    #权限判断
    # _msg = check_purview(request.user.username, 29)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_deviceplan/?msg='+_msg+'&id='+_deviceid)
    
    _title = request.GET.get('title')
    _period = request.GET.get('period')
    _createcontent = request.GET.get('createcontent')
    _editor = request.GET.get('editor')
    _memo = request.GET.get('memo')

    _id = request.GET.get('id')
    _user = k_user.objects.get(username=request.user.username)
    if _editor != '该用户已被删除':
        _editor = k_user.objects.get(name=_editor)

    if _id != "":
        _deviceplan = k_deviceplan.objects.get(id=_id)
        _maintenance = k_maintenance.objects.get(id=_deviceplan.maintenanceid_id)
    else:
        _maintenance = k_maintenance.objects.create(mtype=1,classid=_user.classid,deviceid_id=_deviceid,state=2)
        _deviceplan = k_deviceplan.objects.create(deviceid_id=_deviceid,maintenanceid=_maintenance)

    _maintenance.creatorid = _user.id
    _maintenance.assignorid = _user.id
    _maintenance.assigndatetime = get_current_time()
    _maintenance.title = _title
    _maintenance.createcontent = _createcontent
    if _editor != '该用户已被删除':
        _maintenance.editorid = _editor.id
    _maintenance.memo = _memo+"（周期为："+dict(k_deviceplan.DEVICEPLAN_PERIODS)[_period]+"）"
    _maintenance.state = 2
    _maintenance.save()

    _deviceplan.assignorid = _user.id
    _deviceplan.assigndatetime = get_current_date()
    _deviceplan.title = _title
    _deviceplan.period = _period
    _deviceplan.createcontent = _createcontent
    if _editor != '该用户已被删除':
        _deviceplan.editorid = _editor.id
    _deviceplan.memo = _memo
    _deviceplan.save()

    return HttpResponseRedirect('/view_deviceplan/?id='+_deviceid)


@login_required
def delete_deviceplan(request):
    _id = request.GET.get('id')
    _deviceid = request.GET.get('deviceid')
    #权限判断
    # _msg = check_purview(request.user.username, 30)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_deviceplan/?msg='+_msg+'&id='+_deviceid)
    
    if _id:
        _deviceplan = k_deviceplan.objects.get(id=_id)
        _maintenance = k_maintenance.objects.filter(id=_deviceplan.maintenanceid_id)
        _deviceplan.delete()
        _maintenance.delete()
    return HttpResponseRedirect('/view_deviceplan/?id='+_deviceid)


@login_required
def view_maintaining(request):
    #权限判断
    # _msg = check_purview(request.user.username, 31)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    thedeviceid = request.GET.get('deviceid')
    _maintainings = k_maintenance.objects.filter(classid__in=result, mtype=2, state__in=[1,2,3,'a','b'])
    if thedeviceid:
        _maintainings = k_maintenance.objects.filter(classid__in=result, mtype=2, state__in=[1,2,3,'a','b'], deviceid_id=thedeviceid)
    # _maintainings = k_maintenance.objects.filter(mtype=2, state__lte=3)

    data = []
    for _maintaining in _maintainings:
        _device = _maintaining.deviceid
        _db = _dn = _dp = ""
        if _device != None:
            _db = _device.brief
            _dn = _device.name
            _dp = _device.position
        try:
            _creator = k_user.objects.get(id=_maintaining.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        memo = _maintaining.memo
        if _maintaining.creatorid == 0:
            _creator = _maintaining.memo.split("审核未通过：")[0]
            memo = ""
        
        if _maintaining.image:
            _imageurl = _maintaining.image.url
        else:
            _imageurl = ""
        if _maintaining.assignorid == 0:
            data.append({
                'id': _maintaining.id,
                'classname': _maintaining.classid.name,
                'title': _maintaining.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'imageurl': _imageurl,
                'creator': _creator,
                'createdatetime': _maintaining.createdatetime,
                'createcontent': _maintaining.createcontent,
                'memo': memo,
                'priority': _maintaining.get_priority_display(),
                'state': _maintaining.state
            })
        else:
            try:
                _assignor = k_user.objects.get(id=_maintaining.assignorid).name
            except ObjectDoesNotExist:
                _assignor = '该用户已被删除'
            try:
                _editor = k_user.objects.get(id=_maintaining.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            data.append({
                'id': _maintaining.id,
                'classname': _maintaining.classid.name,
                'title': _maintaining.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'imageurl': _imageurl,
                'creator': _creator,
                'createdatetime': _maintaining.createdatetime,
                'assignor': _assignor,
                'assigndatetime': _maintaining.assigndatetime,
                'editor': _editor,
                'createcontent': _maintaining.createcontent,
                'memo': memo,
                'priority': _maintaining.get_priority_display(),
                'state': _maintaining.state
            })

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _users = k_user.objects.filter(classid__in=result)
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    _devices = k_device.objects.filter(classid__in=result)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #其他错误信息
    other_msg = request.GET.get('other_msg')
    if other_msg == None:
       other_msg = ''

    return get_purviews_and_render_to_response(request.user.username, 'maintainingview.html', {'data': data, 'maintainers': _maintainers, 'devices': _devices,
                                                                                               'purview_msg': purview_msg,
                                                                                               'other_msg': other_msg,
                                                                                               'username':user.username,
                                                                                               'useravatar': user.avatar})


@login_required
def view_maintained(request):
    #权限判断
    # _msg = check_purview(request.user.username, 31)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    thedeviceid = request.GET.get('deviceid')
    _maintaineds = k_maintenance.objects.filter(classid__in=result, mtype=2, state__in=[4,5])
    if thedeviceid:
        _maintaineds = k_maintenance.objects.filter(classid__in=result, mtype=2, state__in=[4,5], deviceid_id=thedeviceid)
    # _maintaineds = k_maintenance.objects.filter(mtype=2, state__gte=4)


    data = []
    for _maintained in _maintaineds:
        _device = _maintained.deviceid
        _db = _dn = _dp = ""
        if _device != None:
            _db = _device.brief
            _dn = _device.name
            _dp = _device.position
        try:
            _creator = k_user.objects.get(id=_maintained.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        memo = _maintained.memo
        if _maintained.creatorid == 0:
            _creator = _maintained.memo.split("审核未通过：")[0]
            memo = ""
        try:
            _assignor = k_user.objects.get(id=_maintained.assignorid).name
        except ObjectDoesNotExist:
            _assignor = '该用户已被删除'
        try:
            _editor = k_user.objects.get(id=_maintained.editorid).name
        except ObjectDoesNotExist:
            _editor = '该用户已被删除'
        if _maintained.image:
            _imageurl = _maintained.image.url
        else:
            _imageurl = ""
        if _maintained.auditorid == 0:
            data.append({
                'id': _maintained.id,
                'classname': _maintained.classid.name,
                'title': _maintained.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'imageurl': _imageurl,
                'creator': _creator,
                'createdatetime': _maintained.createdatetime,
                'assignor': _assignor,
                'assigndatetime': _maintained.assigndatetime,
                'editor': _editor,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': memo,
                'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'state': _maintained.state
            })
        else:
            try:
                _auditor = k_user.objects.get(id=_maintained.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            data.append({
                'id': _maintained.id,
                'classname': _maintained.classid.name,
                'title': _maintained.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'imageurl': _imageurl,
                'creator': _creator,
                'createdatetime': _maintained.createdatetime,
                'assignor': _assignor,
                'assigndatetime': _maintained.assigndatetime,
                'editor': _editor,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': memo,
                'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'auditor': _auditor,
                'auditdatetime': _maintained.auditdatetime,
                'factor': _maintained.factor,
                'state': _maintained.state
            })
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''

    return get_purviews_and_render_to_response(request.user.username, 'maintainedview.html', {'data': data, 'purview_msg': purview_msg,
                                                                                              'username':user.username,
                                                                                              'useravatar': user.avatar})


@login_required
def add_maintenance(request):
    #权限判断
    # _msg = check_purview(request.user.username, 33)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)
    
    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _users = k_user.objects.filter(classid__in=result)
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    _devices = k_device.objects.filter(classid__in=result)
    #_briefs = []
    #for _device in _devices:
    #    _briefs.append(_device.brief)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'maintenanceadd.html', {'maintainers': _maintainers, 'devices': _devices,
                                                                                              'purview_msg': purview_msg,
                                                                                              'username':user.username,
                                                                                              'useravatar': user.avatar})


@login_required
def submit_maintenance(request):
    _id = request.GET.get('id')
    _factor = request.GET.get('factor')
    _editor = request.GET.get('editor')
    #权限判断
    # if _factor:
    #     _msg = check_purview(request.user.username, 34)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_maintained/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 33)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_maintaining/?msg='+_msg)
    #     if _id:
    #         _maintenance = k_maintenance.objects.get(id=_id)
    #         if _editor == "nopersonchosen":
    #             if _maintenance.editorid != 0:
    #                 _msg = check_purview(request.user.username, 32)
    #                 if _msg != 0:
    #                     return HttpResponseRedirect('/view_maintaining/?msg='+_msg)
    #         else:
    #             _maintainer = k_user.objects.get(name=_editor)
    #             if _maintenance.editorid != _maintainer.id:
    #                 _msg = check_purview(request.user.username, 32)
    #                 if _msg != 0:
    #                     return HttpResponseRedirect('/view_maintaining/?msg='+_msg)
    #     else:
    #         if _editor != "nopersonchosen":
    #             _msg = check_purview(request.user.username, 32)
    #             if _msg != 0:
    #                 return HttpResponseRedirect('/add_maintenance/?msg='+_msg)
    
    _title = request.GET.get('title')
    _brief = request.GET.get('brief')
    _createcontent = request.GET.get('createcontent')
    _priority = request.GET.get('priority')
    _memo = request.GET.get('memo')

    _user = k_user.objects.get(username=request.user.username)
    if _factor:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.auditorid = _user.id
        _maintenance.auditdatetime = get_current_time()
        _maintenance.factor = _factor
        _maintenance.state = 5
        if int(_factor) < 0:
            _maintenance.memo = _maintenance.memo.split("审核未通过：")[0] + "审核未通过：" + request.GET.get('failedreason')
            _maintenance.factor = 0
            if request.GET.get('issameperson') == '1':
                _maintenance.state = 'a'
            else:
                _maintenance.state = 'b'
            _maintenance.assigndatetime = get_current_time()
            _maintenance.save()
            return HttpResponseRedirect('/view_maintaining/')
        _maintenance.save()

        "记录积分"
        department_class = _user.classid
        while department_class.depth > 1:
            department_class = k_class.objects.get(id=department_class.parentid)
        try:
            project = k_project.objects.get(classid=department_class)
        except ObjectDoesNotExist:
            project = k_project(
                classid=department_class,
                meterscore=2,
                maintenancescore=2,
                taskscore=2
            )
            project.save()
        try:
            _maintainer = k_user.objects.get(id=_maintenance.editorid)
            staffscoreinfo = k_staffscoreinfo(
                userid=_maintainer,
                score=float(_factor) * float(project.maintenancescore),
                content=str(project.maintenancescore) + ';' + _factor + ';维修',
                time=get_current_date()
            )
            staffscoreinfo.save()
        except ObjectDoesNotExist:
            _maintainer = '该用户已被删除'

        return HttpResponseRedirect('/view_maintained/')
    elif _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        if _editor != "nopersonchosen" and _editor:
            if _editor != '该用户已被删除':
                try:
                    _maintainer = k_user.objects.get(name=_editor)
                    _maintenance.editorid = _maintainer.id
                    _maintenance.assignorid = _user.id
                    _maintenance.assigndatetime = get_current_time()
                    _maintenance.state = 2
                except:
                    return HttpResponseRedirect('/view_maintaining/?other_msg=该用户已被删除')
        else:
            _maintenance.editorid = 0
            _maintenance.assignorid = 0
            _maintenance.state = 1
        if _brief != 'nopersonchosen' and _brief != "":
            _device = k_device.objects.filter(brief=_brief)
            _maintenance.deviceid = _device[0]
        else:
            _maintenance.deviceid = None
        _maintenance.title = _title
        _maintenance.createcontent = _createcontent
        _maintenance.priority = _priority
        #_maintenance.memo = _memo
    else:
        _maintenance = k_maintenance.objects.create(
            classid=_user.classid,
            title=_title,
            createcontent=_createcontent,
            priority=_priority,
            memo=_memo,
            creatorid=0,
            createdatetime=get_current_time(),
            state=1,
            mtype=2
        )
        if _brief != 'nopersonchosen' and _brief != "":
            _device = k_device.objects.filter(brief=_brief)
            _maintenance.deviceid = _device[0]
        if _editor != 'nopersonchosen' and _editor:
            _maintenance.assignorid = _user.id
            _maintenance.assigndatetime = get_current_time()
            _maintainer = k_user.objects.get(name=_editor)
            _maintenance.editorid = _maintainer.id
            _maintenance.state = 2
    _maintenance.save()
    return HttpResponseRedirect('/view_maintaining/')


@login_required
def delete_maintenance(request):
    _type = request.GET.get('type')
    #权限判断
    # _msg = check_purview(request.user.username, 34)
    # if _msg != 0:
    #     if _type == "1":
    #         return HttpResponseRedirect('/view_maintained/?msg='+_msg)
    #     else:
    #         return HttpResponseRedirect('/view_maintaining/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.delete()
    if _type == "1":
        return HttpResponseRedirect('/view_maintained/')
    else:
        return HttpResponseRedirect('/view_maintaining/')


@login_required
def view_upkeeping(request):
    #权限判断
    # _msg = check_purview(request.user.username, 28)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _maintainings = k_maintenance.objects.filter(classid__in=result, mtype=1, state__in=[1,2,3,'a','b'])
    # _maintainings = k_maintenance.objects.filter(mtype=1, state__lte=3)

    data = []
    for _maintaining in _maintainings:
        _device = _maintaining.deviceid
        _db = _dn = _dp = "该设备已被删除"
        if _device != None:
            _db = _device.brief
            _dn = _device.name
            _dp = _device.position
        try:
            _assignor = k_user.objects.get(id=_maintaining.assignorid).name
        except ObjectDoesNotExist:
            _assignor = '该用户已被删除'
        try:
            _editor = k_user.objects.get(id=_maintaining.editorid).name
        except ObjectDoesNotExist:
            _editor = '该用户已被删除'
        data.append({
            'id': _maintaining.id,
            'classname': _maintaining.classid.name,
            'title': _maintaining.title,
            'brief': _db,
            'name': _dn,
            'position': _dp,
            'assignor': _assignor,
            'assigndatetime': _maintaining.assigndatetime,
            #
            'deadline': get_current_date(),
            'editor': _editor,
            'createcontent': _maintaining.createcontent,
            'memo': _maintaining.memo,
            'state': _maintaining.state
        })
    
    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _users = k_user.objects.filter(classid__in=result)
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'upkeepingview.html', {'data': data, 'maintainers': _maintainers,
                                                                                             'purview_msg': purview_msg,
                                                                                             'username': user.username,
                                                                                             'useravatar': user.avatar})

@login_required
def view_upkeeped(request):
    #权限判断
    # _msg = check_purview(request.user.username, 28)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    thedeviceid = request.GET.get('deviceid')
    _maintaineds = k_maintenance.objects.filter(classid__in=result, mtype=1, state__in=[4,5])
    if thedeviceid:
        _maintaineds = k_maintenance.objects.filter(classid__in=result, mtype=1, state__in=[4,5], deviceid_id=thedeviceid)
    # _maintaineds = k_maintenance.objects.filter(mtype=1, state__gte=4)

    data = []
    for _maintained in _maintaineds:
        _device = _maintained.deviceid
        _db = _dn = _dp = "该设备已被删除"
        if _device != None:
            _db = _device.brief
            _dn = _device.name
            _dp = _device.position
        #_creator = k_user.objects.get(id=_maintained.creatorid)
        try:
            _assignor = k_user.objects.get(id=_maintained.assignorid).name
        except ObjectDoesNotExist:
            _assignor = '该用户已被删除'
        try:
            _editor = k_user.objects.get(id=_maintained.editorid).name
        except ObjectDoesNotExist:
            _editor = '该用户已被删除'
        if _maintained.auditorid == 0:
            data.append({
                'id': _maintained.id,
                'classname': _maintained.classid.name,
                'title': _maintained.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                #'creator': _creator.name,
                #'createdatetime': _maintained.createdatetime,
                'assignor': _assignor,
                'assigndatetime': _maintained.assigndatetime,
                #
                'deadline': get_current_date(),
                'editor': _editor,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': _maintained.memo,
                #'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'state': _maintained.state
            })
        else:
            try:
                _auditor = k_user.objects.get(id=_maintained.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            data.append({
                'id': _maintained.id,
                'classname': _maintained.classid.name,
                'title': _maintained.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                #'creator': _creator.name,
                #'createdatetime': _maintained.createdatetime,
                'assignor': _assignor,
                'assigndatetime': _maintained.assigndatetime,
                #
                'deadline': get_current_date(),
                'editor': _editor,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': _maintained.memo,
                #'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'auditor': _auditor,
                'auditdatetime': _maintained.auditdatetime,
                'factor': _maintained.factor,
                'state': _maintained.state
            })
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'upkeepedview.html', {'data': data, 'purview_msg': purview_msg,
                                                                                            'username':user.username,
                                                                                            'useravatar': user.avatar})


@login_required
def submit_upkeep(request):
    #权限判断
    # _msg = check_purview(request.user.username, 30)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_upkeeped/?msg='+_msg)
        
    _id = request.GET.get('id')
    _factor = request.GET.get('factor')
    _user = k_user.objects.get(username=request.user.username)
    _maintenance = k_maintenance.objects.get(id=_id)
    _maintenance.auditorid = _user.id
    _maintenance.auditdatetime = get_current_time()
    _maintenance.factor = _factor
    _maintenance.state = 5
    if int(_factor) < 0:
        _maintenance.memo = "审核未通过：" + request.GET.get('failedreason')
        _maintenance.factor = 0
        if request.GET.get('issameperson') == '1':
            _maintenance.state = 'a'
        else:
            _maintenance.state = 'b'
        _maintenance.assigndatetime = get_current_time()
        _maintenance.save()
        return HttpResponseRedirect('/view_upkeeping/')
    _maintenance.save()

    "记录积分"
    department_class = _user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)
    try:
        project = k_project.objects.get(classid=department_class)
    except ObjectDoesNotExist:
        project = k_project(
            classid=department_class,
            meterscore=2,
            maintenancescore=2,
            taskscore=2
        )
        project.save()
    try:
        _maintainer = k_user.objects.get(id=_maintenance.editorid)
        staffscoreinfo = k_staffscoreinfo(
            userid=_maintainer,
            score=float(_factor) * float(project.maintenancescore),
            content=str(project.maintenancescore) + ';' + _factor + ';保养',
            time=get_current_date()
        )
        staffscoreinfo.save()
    except ObjectDoesNotExist:
        _maintainer = '该用户已被删除'

    return HttpResponseRedirect('/view_upkeeped/')


@login_required
def delete_upkeep(request):
    #权限判断
    # _msg = check_purview(request.user.username, 30)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_upkeeped/?msg='+_msg)
        
    _id = request.GET.get('id')
    if _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.delete()
    return HttpResponseRedirect('/view_upkeeped/')


@login_required
def view_tasking(request):
    #权限判断
    # _msg = check_purview(request.user.username, 35)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _maintainings = k_task.objects.filter(classid__in=result, state__in=[1,2,'a','b'])
    # _maintainings = k_task.objects.filter(state__lte=2)

    data = []
    for _maintaining in _maintainings:
        try:
            _creator = k_user.objects.get(id=_maintaining.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        data.append({
            'id': _maintaining.id,
            'classname': _maintaining.classid.name,
            'title': _maintaining.title,
            'creator': _creator,
            'createdatetime': _maintaining.createdatetime,
            'createcontent': _maintaining.createcontent,
            'memo': _maintaining.memo,
            'priority': _maintaining.get_priority_display(),
            'state': _maintaining.get_state_display()
        })
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'taskingview.html', {'data': data, 'purview_msg': purview_msg,
                                                                                           'username':user.username,
                                                                                           'useravatar': user.avatar})


@login_required
def view_tasked(request):
    #权限判断
    # _msg = check_purview(request.user.username, 35)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _maintaineds = k_task.objects.filter(classid__in=result, state__in=[3,4])
    # _maintaineds = k_task.objects.filter(state__gte=3)

    data = []
    for _maintained in _maintaineds:
        try:
            _creator = k_user.objects.get(id=_maintained.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        data.append({
            'id': _maintained.id,
            'classname': _maintained.classid.name,
            'title': _maintained.title,
            'creator': _creator,
            'createdatetime': _maintained.createdatetime,
            'createcontent': _maintained.createcontent,
            'memo': _maintained.memo,
            'priority': _maintained.get_priority_display(),
            'state': _maintained.get_state_display()
        })
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'taskedview.html', {'data': data, 'purview_msg': purview_msg,
                                                                                          'username':user.username,
                                                                                          'useravatar': user.avatar})


@login_required
def add_task(request):
    #权限判断
    # _msg = check_purview(request.user.username, 36)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)
    user=k_user.objects.get(username=request.user.username)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'taskadd.html', {'purview_msg': purview_msg,
                                                                                       'username':user.username,
                                                                                       'useravatar': user.avatar})


@login_required
def submit_task(request):
    #权限判断
    # _msg = check_purview(request.user.username, 36)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_tasking/?msg='+_msg)
        
    _title = request.GET.get('title')
    _createcontent = request.GET.get('createcontent')
    _priority = request.GET.get('priority')
    _memo = request.GET.get('memo')

    _id = request.GET.get('id')

    _user = k_user.objects.get(username=request.user.username)
    if _id:
        _maintenance = k_task.objects.get(id=_id)
        _maintenance.title = _title
        _maintenance.createcontent = _createcontent
        _maintenance.priority = _priority
        _maintenance.memo = _memo
        _maintenance.creatorid = _user.id
        _maintenance.createdatetime = get_current_date()
    else:
        _maintenance = k_task.objects.create(
            classid=_user.classid,
            title=_title,
            createcontent=_createcontent,
            priority=_priority,
            memo=_memo,
            creatorid=_user.id,
            createdatetime=get_current_date(),
            state=1
        )
    _maintenance.save()
    return HttpResponseRedirect('/view_tasking/')


@login_required
def delete_task(request):
    _id = request.GET.get('id')
    _type = request.GET.get('type')
    #权限判断
    # _msg = check_purview(request.user.username, 37)
    # if _msg != 0:
    #     if _type == "1":
    #         return HttpResponseRedirect('/view_tasked/?msg='+_msg)
    #     else:
    #         return HttpResponseRedirect('/view_tasking/?msg='+_msg)
        
    if _id:
        _task = k_task.objects.get(id=_id)
        _taskitems = k_taskitem.objects.filter(taskid_id=_task.id)
        _taskitems.delete()
        _task.delete()
    if _type == "1":
        return HttpResponseRedirect('/view_tasked/')
    else:
        return HttpResponseRedirect('/view_tasking/')


@login_required
def view_taskitem(request):
    #权限判断
    # _msg = check_purview(request.user.username, 35)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    _id = request.GET.get('id')
    _task = k_task.objects.get(id=_id)
    _taskitems = k_taskitem.objects.filter(taskid_id=_task.id)
    data = []
    for _taskitem in _taskitems:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_taskitem.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        try:
            _editor = k_user.objects.get(id=_taskitem.editorid).name
        except ObjectDoesNotExist:
            _editor = '该用户已被删除'
        _helpersid = _taskitem.helpersid.split(";")
        _helpers = []
        if _helpersid != ['']:
            for _helperid in _helpersid:
                try:
                    _helper = k_user.objects.get(id=int(_helperid))
                    _helpers.append(_helper.name)
                except ObjectDoesNotExist:
                    _helper = '该用户已被删除'
        dataitem['id'] = _taskitem.id
        dataitem['title'] = _taskitem.title
        dataitem['createcontent'] = _taskitem.createcontent
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _taskitem.createdatetime
        dataitem['priority'] = _taskitem.get_priority_display()
        dataitem['memo'] = _taskitem.memo
        dataitem['editor'] = _editor
        dataitem['helpers'] = ";".join(_helpers)
        dataitem['state'] = _taskitem.get_state_display()

        if _taskitem.state == "3" or _taskitem.state == "4":
            dataitem['editdatetime'] = _taskitem.editdatetime
            dataitem['editcontent'] = _taskitem.editcontent

        if _taskitem.state == "4":
            try:
                _auditor = k_user.objects.get(id=_taskitem.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _taskitem.auditdatetime
            dataitem['factor'] = _taskitem.factor
        data.append(dataitem)
    
    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _taskers = []
    _users = k_user.objects.filter(classid__in=result)
    for _user in _users:
        _taskers.append(_user.name)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'taskitemview.html', {'title': _task.title, 'taskers': _taskers,
                                                                                            'taskid': _task.id, 'data': data, 'purview_msg': purview_msg,
                                                                                            'username':user.username,'useravatar': user.avatar})


@login_required
def submit_taskitem(request):
    _id = request.GET.get('id')
    _taskid = request.GET.get('taskid')
    _editor = request.GET.get('editor')
    _submittype = request.GET.get('submittype')
    _title = request.GET.get('title')
    _createcontent = request.GET.get('createcontent')
    _priority = request.GET.get('priority')
    _memo = request.GET.get('memo')
    _factor = request.GET.get('factor')
    _user = k_user.objects.get(username=request.user.username)

    #权限判断
    # if _submittype == "1":
    #     _msg = check_purview(request.user.username, 37)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)
    # elif _submittype == "2":
    #     _msg = check_purview(request.user.username, 36)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)

    #     # _taskitem = k_taskitem.objects.get(id=_id)

    #     # _tasker = k_user.objects.get(name=_editor)
    #     # if _taskitem.editorid != _tasker.id:
    #     #     _msg = check_purview(request.user.username, 35.5)
    #     #     if _msg != 0:
    #     #         return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)
    # else:
    #     _msg = check_purview(request.user.username, 36)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)
    #     # _msg = check_purview(request.user.username, 35.5)
    #     # if _msg != 0:
    #     #     return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)


    if _submittype == "1":
        _taskitem = k_taskitem.objects.get(id=_id)
        _taskitem.auditorid = _user.id
        _taskitem.auditdatetime = get_current_time()
        _taskitem.factor = _factor
        _taskitem.state = 4
        if int(_factor) < 0:
            _taskitem.memo = "审核未通过：" + request.GET.get('failedreason')
            _taskitem.factor = 0
            if request.GET.get('issameperson') == '1':
                _taskitem.state = 'a'
            else:
                _taskitem.state = 'b'
            _taskitem.createdatetime = get_current_time()
            _taskitem.save()
            _task = k_task.objects.get(id=_taskitem.taskid_id)
            _task.state = 2
            _task.save()
            return HttpResponseRedirect('/view_taskitem?id=%i' % _taskitem.taskid_id)
        _taskitem.save()
        _taskitems = k_taskitem.objects.filter(taskid_id=_taskitem.taskid_id)
        _auditcomplete = True
        for _one in _taskitems:
            if _one.state != "4":
                _auditcomplete = False
        if _auditcomplete == True:
            _task = k_task.objects.get(id=_taskitem.taskid_id)
            _task.state = 4
            _task.save()

        "记录积分"
        department_class = _user.classid
        while department_class.depth > 1:
            department_class = k_class.objects.get(id=department_class.parentid)
        try:
            project = k_project.objects.get(classid=department_class)
        except ObjectDoesNotExist:
            project = k_project(
                classid=department_class,
                meterscore=2,
                maintenancescore=2,
                taskscore=2
            )
            project.save()
        try:
            _tasker = k_user.objects.get(id=_taskitem.editorid)
            staffscoreinfo = k_staffscoreinfo(
                userid=_tasker,
                score=float(_factor) * float(project.taskscore),
                content=str(project.taskscore) + ';' + _factor + ';任务',
                time=get_current_date()
            )
            staffscoreinfo.save()
        except ObjectDoesNotExist:
            _tasker = '该用户已被删除'

        return HttpResponseRedirect('/view_taskitem?id=%i' % _taskitem.taskid_id)
    
    if _submittype == "2":
        _taskitem = k_taskitem.objects.get(id=_id)
    else:
        _taskitem = k_taskitem.objects.create(taskid_id=_taskid, state=1)
        _task = k_task.objects.get(id=_taskid)
        _task.state = 1
        _task.save()
    _taskitem.creatorid = _user.id
    _taskitem.createdatetime = get_current_time()
    _taskitem.title = _title
    _taskitem.createcontent = _createcontent
    _taskitem.priority = _priority
    _taskitem.memo = _memo
    _taskitem.state = 1
    if _editor != '该用户已被删除':
        _tasker = k_user.objects.get(name=_editor)
        _taskitem.editorid = _tasker.id
    _helpers = request.GET.get('helpersstring')
    _helpers = _helpers.split(";")
    _helpersid = []
    if _helpers != ['']:
        for _helper in _helpers:
            _thehelper = k_user.objects.get(name=_helper)
            _helpersid.append(str(_thehelper.id))
        _taskitem.helpersid = ";".join(_helpersid)
    else:
        _taskitem.helpersid = ""
        
    _taskitem.save()
    return HttpResponseRedirect('/view_taskitem?id='+_taskid)


@login_required
def delete_taskitem(request):
    _id = request.GET.get('id')
    _taskitem = k_taskitem.objects.get(id=_id)
    #权限判断
    # _msg = check_purview(request.user.username, 37)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id=%i' % _taskitem.taskid_id)

    if _id:
        _taskitem = k_taskitem.objects.get(id=_id)
        _taskitem.delete()
        _taskitems = k_taskitem.objects.filter(taskid_id=_taskitem.taskid_id)
        _states = []
        for _one in _taskitems:
            _states.append(_one.state)
        _task = k_task.objects.get(id=_taskitem.taskid_id)
        if _states != []:
            _states.sort()
            _task.state = _states[0]
            _task.save()
    return HttpResponseRedirect('/view_taskitem?id=%i' % _taskitem.taskid_id)


@login_required
def view_spare(request):
    #权限判断
    # _msg = check_purview(request.user.username, 22)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    thedeviceid = request.GET.get('deviceid')
    _spares = k_spare.objects.filter(classid__in=result)
    if thedeviceid:
        _spares = k_spare.objects.filter(classid__in=result, k_device=thedeviceid)

    data = []
    for _spare in _spares:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_spare.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        
        dataitem['id'] = _spare.id
        dataitem['classname'] = _spare.classid.name
        dataitem['brand'] = _spare.brand
        if _spare.producerid:
            dataitem['producer'] = _spare.producerid.name
        if _spare.supplierid:
            dataitem['supplier'] = _spare.supplierid.name
        dataitem['name'] = _spare.name
        dataitem['brief'] = _spare.brief
        dataitem['model'] = _spare.model
        dataitem['minimum'] = _spare.minimum
        dataitem['eligiblestock'] = _spare.eligiblestock
        dataitem['ineligiblestock'] = _spare.ineligiblestock
        dataitem['content'] = _spare.content
        dataitem['memo'] = _spare.memo
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _spare.createdatetime

        if _spare.editorid != 0:
            try:
                _editor = k_user.objects.get(id=_spare.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            
            dataitem['editor'] = _editor
            dataitem['editdatetime'] = _spare.editdatetime

        if _spare.auditorid != 0:
            try:
                _auditor = k_user.objects.get(id=_spare.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _spare.auditdatetime

        data.append(dataitem)

    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'spare.html', {"data": data, 'purview_msg': purview_msg,
                                                                                     'username':user.username, 'useravatar': user.avatar})


def operate_spare(request):
    _id = request.GET.get('id')
    #权限判断
    # _msg = check_purview(request.user.username, 23)
    # if _msg != 0:
    #     if _id:
    #         return HttpResponseRedirect('/view_spare/?msg='+_msg)
    #     else:
    #         return HttpResponseRedirect('/?msg='+_msg)

    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ""
    _data = {}
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _data["id"] = _id
        _data["isNew"] = False
        _data["brand"] = _spare.brand
        if _spare.producerid:
            _data['producer'] = _spare.producerid.name
        if _spare.supplierid:
            _data['supplier'] = _spare.supplierid.name
        _data["name"] = _spare.name
        _data["brief"] = _spare.brief
        _data["model"] = _spare.model
        _data["minimum"] = _spare.minimum
        _data["content"] = _spare.content
        _data["memo"] = _spare.memo
        _data['classname'] = _spare.classid.name
    else:
        _data["isNew"] = True

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _classes = []
    _allclasses = k_class.objects.filter(id__in=result)
    for _class in _allclasses:
        _classes.append(_class.name)
    _producers = []
    _allproducers = k_producer.objects.all()
    for _producer in _allproducers:
        _producers.append(_producer.name)
    _suppliers = []
    _allsuppliers = k_supplier.objects.all()
    for _supplier in _allsuppliers:
        _suppliers.append(_supplier.name)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'spareoperate.html', {"data": _data, "producers": _producers,
                                                                                            "suppliers": _suppliers, "classes": _classes,
                                                                                            'server_msg': server_msg, 'purview_msg': purview_msg,
                                                                                            'username':user.username, 'useravatar': user.avatar})


def submit_spare(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    # if _audit:
    #     _msg = check_purview(request.user.username, 24)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_spare/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 23)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_spare/?msg='+_msg)

    _classname = request.GET.get('classname')
    _brand = request.GET.get('brand')
    _producer = request.GET.get('producer')
    _supplier = request.GET.get('supplier')
    _name = request.GET.get('name')
    _brief = request.GET.get('brief')
    _model = request.GET.get('model')
    _minimum = request.GET.get('minimum')
    _content = request.GET.get('content')
    _memo = request.GET.get('memo')

    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _spare = k_spare.objects.get(id=_id)
        _spare.auditorid = _user.id
        _spare.auditdatetime = get_current_date()
        _spare.save()
        return HttpResponseRedirect('/view_spare')
    _class = k_class.objects.get(name=_classname)
    if _producer != "":
        _producer = k_producer.objects.get(name=_producer)
    else:
        _producer = None
    if _supplier != "":
        _supplier = k_supplier.objects.get(name=_supplier)
    else:
        _supplier = None
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _spares = k_spare.objects.filter(name=_name, classid=_class)
        if len(_spares) > 1 or (len(_spares) == 1 and _spares[0].id != int(_id)):
            server_msg = '名称为'+_spares[0].name+'且所属为'+_classname+'的备件已存在！'
            return HttpResponseRedirect('/operate_spare/?msg='+server_msg+'&id='+_id)
        _spares = k_spare.objects.filter(brief=_brief)
        if len(_spares) > 1 or (len(_spares) == 1 and _spares[0].id != int(_id)):
            server_msg = '简称为'+_spares[0].brief+'的备件已存在！'
            return HttpResponseRedirect('/operate_spare/?msg='+server_msg+'&id='+_id)
        _spare.editorid = _user.id
        _spare.editdatetime = get_current_date()
        _spare.auditorid = 0
        _spare.classid = _class
    else:
        _spares = k_spare.objects.filter(name=_name, classid=_class)
        if len(_spares) > 0:
            server_msg = '名称为'+_spares[0].name+'且所属为'+_classname+'的备件已存在！'
            return HttpResponseRedirect('/operate_spare/?msg='+server_msg)
        _spares = k_spare.objects.filter(brief=_brief)
        if len(_spares) > 0:
            server_msg = '简称为'+_spares[0].brief+'的备件已存在！'
            return HttpResponseRedirect('/operate_spare/?msg='+server_msg)
        _spare = k_spare.objects.create(classid=_class)
        _spare.creatorid = _user.id
        _spare.createdatetime = get_current_date()
    _spare.producerid = _producer
    _spare.supplierid = _supplier
    _spare.brand = _brand
    _spare.name = _name
    _spare.brief = _brief
    _spare.model = _model
    _spare.minimum = int(float(_minimum))
    _spare.content = _content
    _spare.memo = _memo
    _spare.save()

    if _id:
        return HttpResponseRedirect('/view_spare')
    else:
        return HttpResponseRedirect('/view_spare/?msg=您可在“库存”->“备件出入库”中先进行备件入库')


def delete_spare(request):
    #权限判断
    # _msg = check_purview(request.user.username, 24)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_spare/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _sparebills = k_sparebill.objects.filter(spareid=_spare)
        _sparecounts = k_sparecount.objects.filter(spareid=_spare)
        _sparebills.delete()
        _sparecounts.delete()
        _spare.delete()
    return HttpResponseRedirect('/view_spare')


@login_required
def sparebatch_add(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username':user.username, 'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'sparebatchadd.html', variables)

@login_required
def sparebatch_submit(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    if request.method == "POST":
        raw_post_data = request.body
        json_data = json.loads(raw_post_data)
        success_num = 0
        try:
            for json_key in json_data:
                obj_datas = json_data[json_key]
                for obj_data in obj_datas:
                    _brief = obj_data['brief']
                    _name = obj_data['name']
                    _classname = obj_data['classname']
                    _classid = k_class.objects.get(name=_classname)
                    if obj_data['producer'] == "无":
                        _producerid = ''
                    else:
                        _producer = k_producer.objects.filter(name=obj_data['producer'])
                        if len(_producer) == 0:
                            _producerid = k_producer.objects.create(
                                name=obj_data['producer'], creatorid = request.user.id, createdatetime=get_current_date(),
                                editorid=request.user.id, editdatetime=get_current_date()
                            )
                        elif len(_producer) == 1:
                            _producerid = _producer[0]
                        else:
                            server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加生产厂家出错：'
                            return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    if obj_data['supplier'] == "无":
                        _supplierid = ''
                    else:
                        _supplier = k_supplier.objects.filter(name=obj_data['supplier'])
                        if len(_supplier) == 0:
                            _supplierid = k_supplier.objects.create(
                                name=obj_data['supplier'], creatorid = request.user.id, createdatetime=get_current_date(),
                                editorid=request.user.id, editdatetime=get_current_date()
                            )
                        elif len(_supplier) == 1:
                            _supplierid = _supplier[0]
                        else:
                            server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加供应商出错：'
                            return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    _spares = k_spare.objects.filter(brief=_brief)
                    _spares = _spares.filter(name=_name)
                    if len(_spares) > 0:
                        _dev = _spares[0]
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += _classname+'中'+_dev.name+'('+_dev.brief+')的备件已存在！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")
                    _minimum = obj_data['minimum']
                    if not isinstance(_minimum, int):
                        if isinstance(_minimum, str):
                            if _minimum.isdigit():
                                _minimum = int(_minimum)
                            else:
                                server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                                server_msg += '最小库存应为正整数！'
                                return HttpResponse(json.dumps({
                                    "server_msg":server_msg
                                    }), content_type="application/json")
                    _spare = k_spare.objects.create(
                        classid=_classid,
                        name=obj_data['name'],
                        brief=obj_data['brief'],
                        brand=obj_data['brand'],
                        model=obj_data['model'],
                        content=obj_data['content'],
                        memo=obj_data['memo'],
                        minimum=_minimum,
                        creatorid=request.user.id,
                        createdatetime=get_current_date(),
                        editorid=request.user.id,
                        editdatetime=get_current_date()
                    )
                    if _supplierid != '':
                        _spare.supplierid = _supplierid
                    if _producerid != '':
                        _spare.producerid = _producerid
                    _spare.save()
                    success_num += 1
            server_msg = '成功添加'+str(success_num)+'条备品备件信息！'
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
        except Exception as e:
            server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查所属部门、备件名称和最小库存等是否正确！'
            print e
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
    server_msg = "导入失败，请检查数据格式是否符合模板要求！"
    return HttpResponse(json.dumps({
        "username": user.username,
        "server_msg":server_msg
        }), content_type="application/json")

def view_sparebill(request):
    #权限判断
    # _msg = check_purview(request.user.username, 38)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _sparebills = k_sparebill.objects.filter(classid__in=result)

    data = []
    for _sparebill in _sparebills:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_sparebill.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        try:
            _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        except ObjectDoesNotExist:
            continue
        dataitem['id'] = _sparebill.id
        dataitem['brief'] = _spare.brief
        dataitem['using'] = _sparebill.using
        dataitem['returned'] = _sparebill.returned
        dataitem['depleted'] = _sparebill.depleted
        dataitem['damaged'] = _sparebill.damaged
        dataitem['rejected'] = _sparebill.rejected
        dataitem['user'] = _sparebill.user
        dataitem['memo'] = _sparebill.memo
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _sparebill.createdatetime

        dataitem['notreturned'] = dataitem['using'] - dataitem['returned'] - dataitem['depleted'] - dataitem['damaged'] - dataitem['rejected']

        if _sparebill.editorid != 0:
            try:
                _editor = k_user.objects.get(id=_sparebill.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            
            dataitem['editor'] = _editor
            dataitem['editdatetime'] = _sparebill.editdatetime

        if _sparebill.auditorid != 0:
            try:
                _auditor = k_user.objects.get(id=_sparebill.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _sparebill.auditdatetime
        elif _sparebill.using == _sparebill.returned + _sparebill.depleted + _sparebill.damaged + _sparebill.rejected:
            dataitem['audit'] = 'audit'
        data.append(dataitem)

    #分类筛选
    _spares = k_spare.objects.filter(classid__in=result)
    #_briefs = []
    #for _spare in _spares:
        #_briefs.append(_spare.brief)

    _briefinfos = []
    for s in _spares:
        _spare = dict()
        _spare["brief"] = s.brief
        _spare['sparename'] = s.name
        _spare["eligiblestock"] = s.eligiblestock
        _spare["ineligiblestock"] = s.ineligiblestock
        _briefinfos.append(_spare)
    
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg


    #return get_purviews_and_render_to_response(request.user.username, 'sparebill.html', {'data': data, 'briefs': _briefs})
    return get_purviews_and_render_to_response(request.user.username, 'sparebill.html', {'data': data, 'briefinfos': _briefinfos,
                                                                                         'server_msg': server_msg, 'purview_msg': purview_msg,
                                                                                         'username':user.username, 'useravatar': user.avatar})


def submit_sparebill(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    # if _audit:
    #     _msg = check_purview(request.user.username, 40)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_sparebill/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 39)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_sparebill/?msg='+_msg)

    #_using = request.GET.get('using')
    _returned = request.GET.get('returned')
    _depleted = request.GET.get('depleted')
    _damaged = request.GET.get('damaged')
    _rejected = request.GET.get('rejected')
    _memo = request.GET.get('memo')
    _name = request.GET.get('user')

    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _sparebill = k_sparebill.objects.get(id=_id)
        _sparebill.auditorid = _user.id
        _sparebill.auditdatetime = get_current_date()
        _sparebill.save()
        return HttpResponseRedirect('/view_sparebill')
    _sparebill = k_sparebill.objects.get(id=_id)
    _sparebill.editorid = _user.id
    _sparebill.editdatetime = get_current_date()
    """
    if _sparebill.using != int(float(_using)):
        _sparecount = k_sparecount.objects.get(sparebillid=_id, state="5")
        _sparecount.count = -int(float(_using))
        _sparecount.editorid = _user.id
        _sparecount.editdatetime = get_current_date()
        _sparecount.auditorid = 0
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.eligiblestock = _spare.eligiblestock + _sparebill.using - int(float(_using))
        _spare.save()
        _sparecount.save()
    """
    if _sparebill.returned != int(float(_returned)):
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.eligiblestock = _spare.eligiblestock - _sparebill.returned + int(float(_returned))
        _sparecount = k_sparecount.objects.create(classid=_user.classid, sparebillid=_id, spareid=_spare)
        _sparecount.count = int(float(_returned)) - _sparebill.returned
        _sparecount.state = "2"
        _sparecount.iseligible = "1"
        _sparecount.memo = _sparebill.memo
        _sparecount.creatorid = _user.id
        _sparecount.createdatetime = get_current_date()
        _spare.save()
        _sparecount.save()

    if _sparebill.rejected != int(float(_rejected)):
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.ineligiblestock = _spare.ineligiblestock - _sparebill.rejected + int(float(_rejected))
        _sparecount = k_sparecount.objects.create(classid=_user.classid, sparebillid=_id, spareid=_spare)
        _sparecount.count = int(float(_rejected)) - _sparebill.rejected
        _sparecount.state = "2"
        _sparecount.iseligible = "2"
        _sparecount.memo = _sparebill.memo
        _sparecount.creatorid = _user.id
        _sparecount.createdatetime = get_current_date()
        _spare.save()
        _sparecount.save()

    #_sparebill.using = int(float(_using))
    _sparebill.returned = int(float(_returned))
    _sparebill.depleted = int(float(_depleted))
    _sparebill.damaged = int(float(_damaged))
    _sparebill.rejected = int(float(_rejected))
    _sparebill.user = _name
    _sparebill.memo = _memo

    _sparebill.save()
    return HttpResponseRedirect('/view_sparebill')


def delete_sparebill(request):
    #权限判断
    # _msg = check_purview(request.user.username, 40)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_sparebill/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _sparebill = k_sparebill.objects.get(id=_id)

        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.eligiblestock = _spare.eligiblestock + _sparebill.using - _sparebill.returned
        _spare.ineligiblestock = _spare.ineligiblestock - _sparebill.rejected

        _spare.save()

        _sparecount = k_sparecount.objects.filter(sparebillid=_id)
        _sparecount.delete()

        _sparebill.delete()
    return HttpResponseRedirect('/view_sparebill')


def view_sparecount(request):
    #权限判断
    # _msg = check_purview(request.user.username, 38)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _sparecounts = k_sparecount.objects.filter(classid__in=result)

    data = []
    for _sparecount in _sparecounts:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_sparecount.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        
        try:
            _spare = k_spare.objects.get(id=_sparecount.spareid_id)
        except ObjectDoesNotExist:
            continue
        dataitem['id'] = _sparecount.id
        dataitem['sparebillid'] = _sparecount.sparebillid
        dataitem['brief'] = _spare.brief
        dataitem['count'] = _sparecount.count
        dataitem['state'] = _sparecount.get_state_display()
        dataitem['iseligible'] = _sparecount.get_iseligible_display()
        dataitem['memo'] = _sparecount.memo
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _sparecount.createdatetime

        if _sparecount.editorid != 0:
            try:
                _editor = k_user.objects.get(id=_sparecount.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            
            dataitem['editor'] = _editor
            dataitem['editdatetime'] = _sparecount.editdatetime

        if _sparecount.auditorid != 0:
            try:
                _auditor = k_user.objects.get(id=_sparecount.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _sparecount.auditdatetime
        """
        if _sparecount.sparebillid != 0:
            _sparebill = k_sparebill.objects.get(id=_sparecount.sparebillid)
            dataitem['using'] = _sparebill.using
            dataitem['returned'] = _sparebill.returned
            dataitem['depleted'] = _sparebill.depleted
            dataitem['damaged'] = _sparebill.damaged
            dataitem['rejected'] = _sparebill.rejected
            dataitem['user'] = _sparebill.user
            dataitem['memobill'] = _sparebill.memo
        """
        data.append(dataitem)

    #分类筛选
    _spares = k_spare.objects.filter(classid__in=result)
    #_briefs = []
    #for _spare in _spares:
        #_briefs.append(_spare.brief)

    _briefinfos = []
    for s in _spares:
        _spare = dict()
        _spare["brief"] = s.brief
        _spare['sparename'] = s.name
        _spare["eligiblestock"] = s.eligiblestock
        _spare["ineligiblestock"] = s.ineligiblestock
        _briefinfos.append(_spare)
    
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg


    #return get_purviews_and_render_to_response(request.user.username, 'sparecount.html', {'data': data, 'briefs': _briefs})
    return get_purviews_and_render_to_response(request.user.username, 'sparecount.html', {'data': data, 'briefinfos': _briefinfos,
                                                                                          'server_msg': server_msg, 'purview_msg': purview_msg,
                                                                                          'username':user.username, 'useravatar': user.avatar})


def submit_sparecount(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    # if _audit:
    #     _msg = check_purview(request.user.username, 40)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_sparecount/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 39)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_sparecount/?msg='+_msg)

    _brief = request.GET.get('brief')
    _state = request.GET.get('state')
    _iseligible = request.GET.get('iseligible')
    _count = request.GET.get('count')
    _memo = request.GET.get('memo')
    _name = request.GET.get('user')

    if _state == "4" or _state == "5" or _state == "6":
        _count = -int(float(_count))
    elif _count:
        _count = int(float(_count))

    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _sparecount = k_sparecount.objects.get(id=_id)
        _sparecount.auditorid = _user.id
        _sparecount.auditdatetime = get_current_date()
        _sparecount.save()
        return HttpResponseRedirect('/view_sparecount')

    ## check if spare stock has enough quantity
    _sparecount = None
    _sparecountcount = 0
    if _id != '':
        _sparecount = k_sparecount.objects.get(id=_id)
        _sparecountcount = _sparecount.count
        _spare = k_spare.objects.get(id=_sparecount.spareid_id)
    else:
        _spare = k_spare.objects.get(brief=_brief)
    calcueligible = 0
    calcuineligible = 0
    if _sparecount == None or _iseligible == _sparecount.iseligible:
        if _iseligible == "1":
            calcueligible = _spare.eligiblestock - _sparecountcount + _count
        else:
            calcuineligible = _spare.ineligiblestock - _sparecountcount + _count
    else:
        if _iseligible == "1":
            calcuineligible = _spare.ineligiblestock - _sparecountcount
            calcueligible = _spare.eligiblestock + _count
        else:
            calcueligible = _spare.eligiblestock - _sparecountcount
            calcuineligible = _spare.ineligiblestock + _count
    if calcueligible < 0:
        if _state == "5":
            return HttpResponseRedirect('/view_sparebill/?msg=操作失败，合格品库存不足')
        else:
            return HttpResponseRedirect('/view_sparecount/?msg=操作失败，合格品库存不足')
    if calcuineligible < 0:
        if _state == "5":
            return HttpResponseRedirect('/view_sparebill/?msg=操作失败，不合格品库存不足')
        else:
            return HttpResponseRedirect('/view_sparecount/?msg=操作失败，不合格品库存不足')
    ## end check

    if _id != '':
        _sparecount = k_sparecount.objects.get(id=_id)
        _sparecount.editorid = _user.id
        _sparecount.editdatetime = get_current_date()
    else:
        _spare = k_spare.objects.get(brief=_brief)
        _sparecount = k_sparecount.objects.create(classid=_user.classid, spareid=_spare)
        _sparecount.creatorid = _user.id
        _sparecount.createdatetime = get_current_date()
        if _state == "5":
            _sparebill = k_sparebill.objects.create(classid=_user.classid, spareid=_spare)
            _sparebill.using = -_count
            _sparebill.user = _name
            _sparebill.memo = _memo
            _sparebill.creatorid = _user.id
            _sparebill.createdatetime = get_current_date()
            _sparebill.save()
            _sparecount.sparebillid = _sparebill.id

    _spare = k_spare.objects.get(id=_sparecount.spareid_id)
    if _iseligible == _sparecount.iseligible:
        if _iseligible == "1":
            _spare.eligiblestock = _spare.eligiblestock - _sparecount.count + _count
        else:
            _spare.ineligiblestock = _spare.ineligiblestock - _sparecount.count + _count
    else:
        if _iseligible == "1":
            _spare.ineligiblestock = _spare.ineligiblestock - _sparecount.count
            _spare.eligiblestock = _spare.eligiblestock + _count
        else:
            _spare.eligiblestock = _spare.eligiblestock - _sparecount.count
            _spare.ineligiblestock = _spare.ineligiblestock + _count

    _spare.save()

    _sparecount.state = _state
    _sparecount.iseligible = _iseligible
    _sparecount.count = _count
    _sparecount.memo = _memo

    _sparecount.save()
    if _state == "5":
        if _spare.eligiblestock < _spare.minimum:
            return HttpResponseRedirect('/view_sparebill/?msg=操作成功，但合格品库存低于最小库存，需补'+str(_spare.minimum-_spare.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_sparebill')
    else:
        if _spare.eligiblestock < _spare.minimum:
            return HttpResponseRedirect('/view_sparecount/?msg=操作成功，但合格品库存低于最小库存，需补'+str(_spare.minimum-_spare.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_sparecount')


def delete_sparecount(request):
    #权限判断
    # _msg = check_purview(request.user.username, 40)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_sparecount/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _sparecount = k_sparecount.objects.get(id=_id)

        _spare = k_spare.objects.get(id=_sparecount.spareid_id)
        if _sparecount.iseligible == "1":
            _spare.eligiblestock = _spare.eligiblestock - _sparecount.count
        else:
            _spare.ineligiblestock = _spare.ineligiblestock - _sparecount.count

        _spare.save()

        _sparecount.delete()
    return HttpResponseRedirect('/view_sparecount')


@login_required
def view_tool(request):
    #权限判断
    # _msg = check_purview(request.user.username, 25)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _tools = k_tool.objects.filter(classid__in=result)

    data = []
    for _tool in _tools:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_tool.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        
        dataitem['id'] = _tool.id
        dataitem['classname'] = _tool.classid.name
        dataitem['brand'] = _tool.brand
        if _tool.producerid:
            dataitem['producer'] = _tool.producerid.name
        if _tool.supplierid:
            dataitem['supplier'] = _tool.supplierid.name
        dataitem['name'] = _tool.name
        dataitem['brief'] = _tool.brief
        dataitem['model'] = _tool.model
        dataitem['minimum'] = _tool.minimum
        dataitem['eligiblestock'] = _tool.eligiblestock
        dataitem['ineligiblestock'] = _tool.ineligiblestock
        dataitem['content'] = _tool.content
        dataitem['memo'] = _tool.memo
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _tool.createdatetime
        dataitem['ownername'] = _tool.ownerid.name

        if _tool.editorid != 0:
            try:
                _editor = k_user.objects.get(id=_tool.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            
            dataitem['editor'] = _editor
            dataitem['editdatetime'] = _tool.editdatetime

        if _tool.auditorid != 0:
            try:
                _auditor = k_user.objects.get(id=_tool.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _tool.auditdatetime

        data.append(dataitem)
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg


    return get_purviews_and_render_to_response(request.user.username, 'tool.html', {"data": data, 'purview_msg': purview_msg,
                                                                                    'username':user.username, 'useravatar': user.avatar})


def operate_tool(request):
    _id = request.GET.get('id')
    #权限判断
    # _msg = check_purview(request.user.username, 26)
    # if _msg != 0:
    #     if _id:
    #         return HttpResponseRedirect('/view_tool/?msg='+_msg)
    #     else:
    #         return HttpResponseRedirect('/?msg='+_msg)

    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ""
    _data = {}
    if _id:
        _tool = k_tool.objects.get(id=_id)
        _data["id"] = _id
        _data["isNew"] = False
        _data["brand"] = _tool.brand
        if _tool.producerid:
            _data['producer'] = _tool.producerid.name
        if _tool.supplierid:
            _data['supplier'] = _tool.supplierid.name
        _data["name"] = _tool.name
        _data["brief"] = _tool.brief
        _data["model"] = _tool.model
        _data["minimum"] = _tool.minimum
        _data["content"] = _tool.content
        _data["memo"] = _tool.memo
        _data['classname'] = _tool.classid.name
        _data['ownername'] = _tool.ownerid.name
    else:
        _data["isNew"] = True

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _classes = []
    _allclasses = k_class.objects.filter(id__in=result)
    for _class in _allclasses:
        _classes.append(_class.name)
    _producers = []
    _allproducers = k_producer.objects.all()
    for _producer in _allproducers:
        _producers.append(_producer.name)
    _suppliers = []
    _allsuppliers = k_supplier.objects.all()
    for _supplier in _allsuppliers:
        _suppliers.append(_supplier.name)
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return get_purviews_and_render_to_response(request.user.username, 'tooloperate.html', {"data": _data, "producers": _producers, "suppliers": _suppliers,
                                                                                           "classes": _classes, 'server_msg': server_msg, 'purview_msg': purview_msg,
                                                                                           'username':user.username, 'useravatar': user.avatar})


def submit_tool(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    # if _audit:
    #     _msg = check_purview(request.user.username, 27)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_tool/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 26)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_tool/?msg='+_msg)

    _classname = request.GET.get('classname')
    _brand = request.GET.get('brand')
    _producer = request.GET.get('producer')
    _supplier = request.GET.get('supplier')
    _name = request.GET.get('name')
    _brief = request.GET.get('brief')
    _model = request.GET.get('model')
    _ownername = request.GET.get('ownername')
    _minimum = request.GET.get('minimum')
    _content = request.GET.get('content')
    _memo = request.GET.get('memo')

    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _tool = k_tool.objects.get(id=_id)
        _tool.auditorid = _user.id
        _tool.auditdatetime = get_current_date()
        _tool.save()
        return HttpResponseRedirect('/view_tool')
    _class = k_class.objects.get(name=_classname)
    if _producer != "":
        _producer = k_producer.objects.get(name=_producer)
    else:
        _producer = None
    if _supplier != "":
        _supplier = k_supplier.objects.get(name=_supplier)
    else:
        _supplier = None
    _owner = k_class.objects.get(name=_ownername)
    if _id:
        _tool = k_tool.objects.get(id=_id)
        _tools = k_tool.objects.filter(name=_name, classid=_class)
        if len(_tools) > 1 or (len(_tools) == 1 and _tools[0].id != int(_id)):
            server_msg = '名称为'+_tools[0].name+'且所属为'+_classname+'的工具已存在！'
            return HttpResponseRedirect('/operate_tool/?msg='+server_msg+'&id='+_id)
        _tools = k_tool.objects.filter(brief=_brief)
        if len(_tools) > 1 or (len(_tools) == 1 and _tools[0].id != int(_id)):
            server_msg = '简称为'+_tools[0].brief+'的工具已存在！'
            return HttpResponseRedirect('/operate_tool/?msg='+server_msg+'&id='+_id)
        _tool.editorid = _user.id
        _tool.editdatetime = get_current_date()
        _tool.auditorid = 0
        _tool.classid = _class
        _tool.ownerid = _owner
    else:
        _tools = k_tool.objects.filter(name=_name, classid=_class)
        if len(_tools) > 0:
            server_msg = '名称为'+_tools[0].name+'且所属为'+_classname+'的工具已存在！'
            return HttpResponseRedirect('/operate_tool/?msg='+server_msg)
        _tools = k_tool.objects.filter(brief=_brief)
        if len(_tools) > 0:
            server_msg = '简称为'+_tools[0].brief+'的工具已存在！'
            return HttpResponseRedirect('/operate_tool/?msg='+server_msg)
        _tool = k_tool.objects.create(classid=_class, ownerid=_owner)
        _tool.creatorid = _user.id
        _tool.createdatetime = get_current_date()
    _tool.producerid = _producer
    _tool.supplierid = _supplier
    _tool.brand = _brand
    _tool.name = _name
    _tool.brief = _brief
    _tool.model = _model
    _tool.minimum = int(float(_minimum))
    _tool.content = _content
    _tool.memo = _memo
    _tool.save()

    if _id:
        return HttpResponseRedirect('/view_tool')
    else:
        return HttpResponseRedirect('/view_tool/?msg=您可在“库存”->“工具出入库”中先进行工具入库')


def delete_tool(request):
    #权限判断
    # _msg = check_purview(request.user.username, 27)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_tool/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _tool = k_tool.objects.get(id=_id)
        _tooluses = k_tooluse.objects.filter(toolid=_tool)
        _toolcounts = k_toolcount.objects.filter(toolid=_tool)
        _tooluses.delete()
        _toolcounts.delete()
        _tool.delete()
    return HttpResponseRedirect('/view_tool')


@login_required
def toolbatch_add(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username':user.username, 'useravatar': user.avatar})
    return get_purviews_and_render_to_response(request.user.username, 'toolbatchadd.html', variables)

@login_required
def toolbatch_submit(request):
    # 登陆成功
    user = k_user.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    if request.method == "POST":
        raw_post_data = request.body
        json_data = json.loads(raw_post_data)
        success_num = 0
        try:
            for json_key in json_data:
                obj_datas = json_data[json_key]
                for obj_data in obj_datas:
                    _brief = obj_data['brief']
                    _name = obj_data['name']
                    _classname = obj_data['classname']
                    _classid = k_class.objects.get(name=_classname)
                    _ownername = obj_data['ownername']
                    _ownerid = k_class.objects.get(name=_ownername)
                    if obj_data['producer'] == "无":
                        _producerid = ''
                    else:
                        _producer = k_producer.objects.filter(name=obj_data['producer'])
                        if len(_producer) == 0:
                            _producerid = k_producer.objects.create(
                                name=obj_data['producer'], creatorid = request.user.id, createdatetime=get_current_date(),
                                editorid=request.user.id, editdatetime=get_current_date()
                            )
                        elif len(_producer) == 1:
                            _producerid = _producer[0]
                        else:
                            server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加生产厂家出错：'
                            return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    if obj_data['supplier'] == "无":
                        _supplierid = ''
                    else:
                        _supplier = k_supplier.objects.filter(name=obj_data['supplier'])
                        if len(_supplier) == 0:
                            _supplierid = k_supplier.objects.create(
                                name=obj_data['supplier'], creatorid = request.user.id, createdatetime=get_current_date(),
                                editorid=request.user.id, editdatetime=get_current_date()
                            )
                        elif len(_supplier) == 1:
                            _supplierid = _supplier[0]
                        else:
                            server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条添加供应商出错：'
                            return HttpResponse(json.dumps({
                                "server_msg":server_msg
                                }), content_type="application/json")
                    _tools = k_tool.objects.filter(brief=_brief)
                    _tools = _tools.filter(name=_name)
                    if len(_tools) > 0:
                        _dev = _tools[0]
                        server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                        server_msg += _classname+'中'+_dev.name+'('+_dev.brief+')的工具已存在！'
                        return HttpResponse(json.dumps({
                            "server_msg":server_msg
                            }), content_type="application/json")
                    _minimum = obj_data['minimum']
                    if not isinstance(_minimum, int):
                        if isinstance(_minimum, str):
                            if _minimum.isdigit():
                                _minimum = int(_minimum)
                            else:
                                server_msg = '已成功添加'+str(success_num)+'条数据，第'+str(success_num+1)+'条出错：'
                                server_msg += '最小库存应为正整数！'
                                return HttpResponse(json.dumps({
                                    "server_msg":server_msg
                                    }), content_type="application/json")
                    _tool = k_tool.objects.create(
                        classid=_classid,
                        ownerid=_ownerid,
                        name=obj_data['name'],
                        brief=obj_data['brief'],
                        brand=obj_data['brand'],
                        model=obj_data['model'],
                        content=obj_data['content'],
                        memo=obj_data['memo'],
                        minimum=_minimum,
                        creatorid=request.user.id,
                        createdatetime=get_current_date(),
                        editorid=request.user.id,
                        editdatetime=get_current_date()
                    )
                    if _supplierid != '':
                        _tool.supplierid = _supplierid
                    if _producerid != '':
                        _tool.producerid = _producerid
                    _tool.save()
                    success_num += 1
            server_msg = '成功添加'+str(success_num)+'条工具信息！'
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
        except Exception as e:
            server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查所属部门、工具名称和最小库存等是否正确！'
            print e
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
    server_msg = "导入失败，请检查数据格式是否符合模板要求！"
    return HttpResponse(json.dumps({
        "username": user.username,
        "server_msg":server_msg
        }), content_type="application/json")



def view_tooluse(request):
    #权限判断
    # _msg = check_purview(request.user.username, 41)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _tooluses = k_tooluse.objects.filter(classid__in=result)

    data = []
    for _tooluse in _tooluses:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_tooluse.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        
        try:
            _tool = k_tool.objects.get(id=_tooluse.toolid_id)
        except ObjectDoesNotExist:
            continue
        dataitem['id'] = _tooluse.id
        dataitem['brief'] = _tool.brief
        dataitem['using'] = _tooluse.using
        dataitem['returned'] = _tooluse.returned
        dataitem['depleted'] = _tooluse.depleted
        dataitem['damaged'] = _tooluse.damaged
        dataitem['rejected'] = _tooluse.rejected
        dataitem['user'] = _tooluse.user
        dataitem['memo'] = _tooluse.memo
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _tooluse.createdatetime

        dataitem['notreturned'] = dataitem['using'] - dataitem['returned'] - dataitem['depleted'] - dataitem['damaged'] - dataitem['rejected']

        if _tooluse.editorid != 0:
            try:
                _editor = k_user.objects.get(id=_tooluse.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            
            dataitem['editor'] = _editor
            dataitem['editdatetime'] = _tooluse.editdatetime

        if _tooluse.auditorid != 0:
            try:
                _auditor = k_user.objects.get(id=_tooluse.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _tooluse.auditdatetime
        elif _tooluse.using == _tooluse.returned + _tooluse.depleted + _tooluse.damaged + _tooluse.rejected:
            dataitem['audit'] = 'audit'
        data.append(dataitem)

    #分类筛选
    _tools = k_tool.objects.filter(classid__in=result)
    #_briefs = []
    #for _tool in _tools:
        #_briefs.append(_tool.brief)

    _briefinfos = []
    for s in _tools:
        _tool = dict()
        _tool["brief"] = s.brief
        _tool['toolname'] = s.name
        _tool["eligiblestock"] = s.eligiblestock
        _tool["ineligiblestock"] = s.ineligiblestock
        _briefinfos.append(_tool)
    
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg


    #return get_purviews_and_render_to_response(request.user.username, 'tooluse.html', {'data': data, 'briefs': _briefs})
    return get_purviews_and_render_to_response(request.user.username, 'tooluse.html', {'data': data, 'briefinfos': _briefinfos,
                                                                                       'server_msg': server_msg, 'purview_msg': purview_msg,
                                                                                       'username':user.username, 'useravatar': user.avatar})


def submit_tooluse(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    # if _audit:
    #     _msg = check_purview(request.user.username, 43)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_tooluse/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 42)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_tooluse/?msg='+_msg)

    #_using = request.GET.get('using')
    _returned = request.GET.get('returned')
    _depleted = request.GET.get('depleted')
    _damaged = request.GET.get('damaged')
    _rejected = request.GET.get('rejected')
    _memo = request.GET.get('memo')
    _name = request.GET.get('user')

    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _tooluse = k_tooluse.objects.get(id=_id)
        _tooluse.auditorid = _user.id
        _tooluse.auditdatetime = get_current_date()
        _tooluse.save()
        return HttpResponseRedirect('/view_tooluse')
    _tooluse = k_tooluse.objects.get(id=_id)
    _tooluse.editorid = _user.id
    _tooluse.editdatetime = get_current_date()
    """
    if _tooluse.using != int(float(_using)):
        _toolcount = k_toolcount.objects.get(tooluseid=_id, state="5")
        _toolcount.count = -int(float(_using))
        _toolcount.editorid = _user.id
        _toolcount.editdatetime = get_current_date()
        _toolcount.auditorid = 0
        _tool = k_tool.objects.get(id=_tooluse.toolid_id)
        _tool.eligiblestock = _tool.eligiblestock + _tooluse.using - int(float(_using))
        _tool.save()
        _toolcount.save()
    """
    if _tooluse.returned != int(float(_returned)):
        _tool = k_tool.objects.get(id=_tooluse.toolid_id)
        _tool.eligiblestock = _tool.eligiblestock - _tooluse.returned + int(float(_returned))
        _toolcount = k_toolcount.objects.create(classid=_user.classid, tooluseid=_id, toolid=_tool)
        _toolcount.count = int(float(_returned)) - _tooluse.returned
        _toolcount.state = "2"
        _toolcount.iseligible = "1"
        _toolcount.memo = _tooluse.memo
        _toolcount.creatorid = _user.id
        _toolcount.createdatetime = get_current_date()
        _tool.save()
        _toolcount.save()

    if _tooluse.rejected != int(float(_rejected)):
        _tool = k_tool.objects.get(id=_tooluse.toolid_id)
        _tool.ineligiblestock = _tool.ineligiblestock - _tooluse.rejected + int(float(_rejected))
        _toolcount = k_toolcount.objects.create(classid=_user.classid, tooluseid=_id, toolid=_tool)
        _toolcount.count = int(float(_rejected)) - _tooluse.rejected
        _toolcount.state = "2"
        _toolcount.iseligible = "2"
        _toolcount.memo = _tooluse.memo
        _toolcount.creatorid = _user.id
        _toolcount.createdatetime = get_current_date()
        _tool.save()
        _toolcount.save()

    #_tooluse.using = int(float(_using))
    _tooluse.returned = int(float(_returned))
    _tooluse.depleted = int(float(_depleted))
    _tooluse.damaged = int(float(_damaged))
    _tooluse.rejected = int(float(_rejected))
    _tooluse.user = _name
    _tooluse.memo = _memo

    _tooluse.save()
    return HttpResponseRedirect('/view_tooluse')


def delete_tooluse(request):
    #权限判断
    # _msg = check_purview(request.user.username, 43)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_tooluse/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _tooluse = k_tooluse.objects.get(id=_id)

        _tool = k_tool.objects.get(id=_tooluse.toolid_id)
        _tool.eligiblestock = _tool.eligiblestock + _tooluse.using - _tooluse.returned
        _tool.ineligiblestock = _tool.ineligiblestock - _tooluse.rejected

        _tool.save()

        _toolcount = k_toolcount.objects.filter(tooluseid=_id)
        _toolcount.delete()

        _tooluse.delete()
    return HttpResponseRedirect('/view_tooluse')


def view_toolcount(request):
    #权限判断
    # _msg = check_purview(request.user.username, 41)
    # if _msg != 0:
    #     return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _toolcounts = k_toolcount.objects.filter(classid__in=result)

    data = []
    for _toolcount in _toolcounts:
        dataitem = {}

        try:
            _creator = k_user.objects.get(id=_toolcount.creatorid).name
        except ObjectDoesNotExist:
            _creator = '该用户已被删除'
        
        try:
            _tool = k_tool.objects.get(id=_toolcount.toolid_id)
        except ObjectDoesNotExist:
            continue
        dataitem['id'] = _toolcount.id
        dataitem['tooluseid'] = _toolcount.tooluseid
        dataitem['brief'] = _tool.brief
        dataitem['count'] = _toolcount.count
        dataitem['state'] = _toolcount.get_state_display()
        dataitem['iseligible'] = _toolcount.get_iseligible_display()
        dataitem['memo'] = _toolcount.memo
        dataitem['creator'] = _creator
        dataitem['createdatetime'] = _toolcount.createdatetime

        if _toolcount.editorid != 0:
            try:
                _editor = k_user.objects.get(id=_toolcount.editorid).name
            except ObjectDoesNotExist:
                _editor = '该用户已被删除'
            
            dataitem['editor'] = _editor
            dataitem['editdatetime'] = _toolcount.editdatetime

        if _toolcount.auditorid != 0:
            try:
                _auditor = k_user.objects.get(id=_toolcount.auditorid).name
            except ObjectDoesNotExist:
                _auditor = '该用户已被删除'
            
            dataitem['auditor'] = _auditor
            dataitem['auditdatetime'] = _toolcount.auditdatetime
        """
        if _toolcount.tooluseid != 0:
            _tooluse = k_tooluse.objects.get(id=_toolcount.tooluseid)
            dataitem['using'] = _tooluse.using
            dataitem['returned'] = _tooluse.returned
            dataitem['depleted'] = _tooluse.depleted
            dataitem['damaged'] = _tooluse.damaged
            dataitem['rejected'] = _tooluse.rejected
            dataitem['user'] = _tooluse.user
            dataitem['memobill'] = _tooluse.memo
        """
        data.append(dataitem)

    #分类筛选
    _tools = k_tool.objects.filter(classid__in=result)
    #_briefs = []
    #for _tool in _tools:
        #_briefs.append(_tool.brief)

    _briefinfos = []
    for s in _tools:
        _tool = dict()
        _tool["brief"] = s.brief
        _tool['toolname'] = s.name
        _tool["eligiblestock"] = s.eligiblestock
        _tool["ineligiblestock"] = s.ineligiblestock
        _briefinfos.append(_tool)
    
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg


    #return get_purviews_and_render_to_response(request.user.username, 'toolcount.html', {'data': data, 'briefs': _briefs})
    return get_purviews_and_render_to_response(request.user.username, 'toolcount.html', {'data': data, 'briefinfos': _briefinfos,
                                                                                         'server_msg': server_msg, 'purview_msg': purview_msg,
                                                                                         'username':user.username, 'useravatar': user.avatar})


def submit_toolcount(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    # if _audit:
    #     _msg = check_purview(request.user.username, 43)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_toolcount/?msg='+_msg)
    # else:
    #     _msg = check_purview(request.user.username, 42)
    #     if _msg != 0:
    #         return HttpResponseRedirect('/view_toolcount/?msg='+_msg)

    _brief = request.GET.get('brief')
    _state = request.GET.get('state')
    _iseligible = request.GET.get('iseligible')
    _count = request.GET.get('count')
    _memo = request.GET.get('memo')
    _name = request.GET.get('user')

    if _state == "4" or _state == "5" or _state == "6":
        _count = -int(float(_count))
    elif _count:
        _count = int(float(_count))

    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _toolcount = k_toolcount.objects.get(id=_id)
        _toolcount.auditorid = _user.id
        _toolcount.auditdatetime = get_current_date()
        _toolcount.save()
        return HttpResponseRedirect('/view_toolcount')

    ## check if tool stock has enough quantity
    _toolcount = None
    _toolcountcount = 0
    if _id != '':
        _toolcount = k_toolcount.objects.get(id=_id)
        _toolcountcount = _toolcount.count
        _tool = k_tool.objects.get(id=_toolcount.toolid_id)
    else:
        _tool = k_tool.objects.get(brief=_brief)
    calcueligible = 0
    calcuineligible = 0
    if _toolcount == None or _iseligible == _toolcount.iseligible:
        if _iseligible == "1":
            calcueligible = _tool.eligiblestock - _toolcountcount + _count
        else:
            calcuineligible = _tool.ineligiblestock - _toolcountcount + _count
    else:
        if _iseligible == "1":
            calcuineligible = _tool.ineligiblestock - _toolcountcount
            calcueligible = _tool.eligiblestock + _count
        else:
            calcueligible = _tool.eligiblestock - _toolcountcount
            calcuineligible = _tool.ineligiblestock + _count
    if calcueligible < 0:
        if _state == "5":
            return HttpResponseRedirect('/view_tooluse/?msg=操作失败，合格品库存不足')
        else:
            return HttpResponseRedirect('/view_toolcount/?msg=操作失败，合格品库存不足')
    if calcuineligible < 0:
        if _state == "5":
            return HttpResponseRedirect('/view_tooluse/?msg=操作失败，不合格品库存不足')
        else:
            return HttpResponseRedirect('/view_toolcount/?msg=操作失败，不合格品库存不足')
    ## end check
    if _id != '':
        _toolcount = k_toolcount.objects.get(id=_id)
        _toolcount.editorid = _user.id
        _toolcount.editdatetime = get_current_date()
    else:
        _tool = k_tool.objects.get(brief=_brief)
        _toolcount = k_toolcount.objects.create(classid=_user.classid, toolid=_tool)
        _toolcount.creatorid = _user.id
        _toolcount.createdatetime = get_current_date()
        if _state == "5":
            _tooluse = k_tooluse.objects.create(classid=_user.classid, toolid=_tool)
            _tooluse.using = -_count
            _tooluse.user = _name
            _tooluse.memo = _memo
            _tooluse.creatorid = _user.id
            _tooluse.createdatetime = get_current_date()
            _tooluse.save()
            _toolcount.tooluseid = _tooluse.id

    _tool = k_tool.objects.get(id=_toolcount.toolid_id)
    if _iseligible == _toolcount.iseligible:
        if _iseligible == "1":
            _tool.eligiblestock = _tool.eligiblestock - _toolcount.count + _count
        else:
            _tool.ineligiblestock = _tool.ineligiblestock - _toolcount.count + _count
    else:
        if _iseligible == "1":
            _tool.ineligiblestock = _tool.ineligiblestock - _toolcount.count
            _tool.eligiblestock = _tool.eligiblestock + _count
        else:
            _tool.eligiblestock = _tool.eligiblestock - _toolcount.count
            _tool.ineligiblestock = _tool.ineligiblestock + _count

    _tool.save()

    _toolcount.state = _state
    _toolcount.iseligible = _iseligible
    _toolcount.count = _count
    _toolcount.memo = _memo

    _toolcount.save()
    if _state == "5":
        if _tool.eligiblestock < _tool.minimum:
            return HttpResponseRedirect('/view_tooluse/?msg=操作成功，但合格品库存低于最小库存，需补'+str(_tool.minimum-_tool.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_tooluse')
    else:
        if _tool.eligiblestock < _tool.minimum:
            return HttpResponseRedirect('/view_toolcount/?msg=操作成功，但合格品库存低于最小库存，需补'+str(_tool.minimum-_tool.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_toolcount')


def delete_toolcount(request):
    #权限判断
    # _msg = check_purview(request.user.username, 43)
    # if _msg != 0:
    #     return HttpResponseRedirect('/view_toolcount/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _toolcount = k_toolcount.objects.get(id=_id)

        _tool = k_tool.objects.get(id=_toolcount.toolid_id)
        if _toolcount.iseligible == "1":
            _tool.eligiblestock = _tool.eligiblestock - _toolcount.count
        else:
            _tool.ineligiblestock = _tool.ineligiblestock - _toolcount.count

        _tool.save()

        _toolcount.delete()
    return HttpResponseRedirect('/view_toolcount')


'''
部门设置开始
'''


def department(request):
    if request.user.is_authenticated():
        user = k_user.objects.get(username=request.user.username)
        classes = k_class.objects.all()
        parents = 0
        datas = get_dept_type_node(classes, parents) #获取节点树
        server_msg = request.GET.get("msg")
        if server_msg == None:
            server_msg = ""
            #非法权限信息
        purview_msg = request.GET.get('msg')
        if purview_msg == None:
           purview_msg = ''
        #, 'purview_msg': purview_msg
        _id = request.GET.get('id')
        if _id:
            department_info = {}
            _departs = k_class.objects.filter(id=_id)
            if len(_departs) == 1:
                department_info["id"] = _id
                department_info["name"] = _departs[0].name
                department_info["phone"] = _departs[0].phone
                department_info["address"] = _departs[0].address
                department_info["zipcode"] = _departs[0].zipcode
                department_info["code"] = _departs[0].code
                department_info["license"] = _departs[0].license
                variables=RequestContext(request,{'username':user.username, 'useravatar': user.avatar, 'data':datas, 'server_msg':server_msg, 'purview_msg': purview_msg,
                                              'department_info':department_info})
            else:
                variables=RequestContext(request,{'username':user.username, 'useravatar': user.avatar, 'data':datas, 'server_msg':server_msg, 'purview_msg': purview_msg})
        else:
            variables=RequestContext(request,{'username':user.username, 'useravatar': user.avatar, 'data':datas, 'server_msg':server_msg, 'purview_msg': purview_msg})
        return get_purviews_and_render_to_response(request.user.username, 'department.html',variables)
    else:
        return HttpResponseRedirect('/login/')

@login_required
def department_revise(request):
    _id = request.GET.get('id')
    if _id:
        #分类筛选
        user = k_user.objects.get(username=request.user.username)
        result = [user.classid.id]
        get_class_set(result, user.classid.id)
        datas = dict()
        k_classes = k_class.objects.filter(id__in=result)
        class_list = list()
        for c in k_classes:
            class_list.append(c.name)
        datas['class_list'] = class_list
        datas['isNew'] = True

        _tmp_class = k_class.objects.filter(id=_id)
        if len(_tmp_class) == 1:
            _existed_info = _tmp_class[0]
            datas["id"] = _id
            datas["name"] = _existed_info.name
            datas["code"] = _existed_info.code
            datas["logo"] = _existed_info.logo
            datas["address"] = _existed_info.address
            datas["zipcode"] = _existed_info.zipcode
            datas["phone"] = _existed_info.phone
            datas["license"] = _existed_info.license
            datas["content"] = _existed_info.content
            datas["memo"] = _existed_info.memo
            if datas['class_list'].count(_existed_info.name) > 0:
                datas['class_list'].remove(_existed_info.name)
            existed_parentid = _existed_info.parentid
            parent_classes = k_class.objects.filter(id = existed_parentid)
            if len(parent_classes) == 1:
                datas['chosen_class'] = parent_classes[0].name
        #非法权限信息
        purview_msg = request.GET.get('msg')
        if purview_msg == None:
           purview_msg = ''
        #, 'purview_msg': purview_msg

        variables=RequestContext(request,{'username':user.username, 'useravatar': user.avatar,  'data':datas, 'purview_msg': purview_msg})
        return get_purviews_and_render_to_response(request.user.username, 'departmentadd.html',variables)
    else:
        HttpResponseRedirect('/department/?msg="非法访问！"')


@login_required
def departmentadd(request):
    if request.user.is_authenticated():
        user=User.objects.get(username=request.user.username)
        #分类筛选
        user = k_user.objects.get(username=request.user.username)
        result = [user.classid.id]
        get_class_set(result, user.classid.id)
        datas = dict()
        k_classes = k_class.objects.filter(id__in=result)
        class_list = list()
        for c in k_classes:
            class_list.append(c.name)
        k_roles = k_role.objects.filter(classid__in=result)
        role_list = list()
        for r in k_roles:
            role_list.append(r.name)
        datas['class_list'] = class_list
        datas['role_list'] = role_list
            #非法权限信息
        purview_msg = request.GET.get('msg')
        if purview_msg == None:
           purview_msg = ''
        #, 'purview_msg': purview_msg

        variables=RequestContext(request,{'username':user.username, 'useravatar': user.avatar, 'data':datas, 'purview_msg': purview_msg})
        return get_purviews_and_render_to_response(request.user.username, 'departmentadd.html',variables)
    else:
        return HttpResponseRedirect('/login/')


@login_required
def department_submit(request):
    _parentname = request.GET.get('parentname')
    _name = request.GET.get('name')
    _code = request.GET.get('code')
    _logo = request.GET.get('logo')
    _address = request.GET.get('address')
    _zipcode = request.GET.get('zipcode')
    _phone = request.GET.get('phone')
    _license = request.GET.get('license')
    _licensetype = request.GET.get('licensetype')
    _content = request.GET.get('content')
    _memo = request.GET.get('memo')
    _cur_id = request.GET.get('id')
    #tmp_class = k_class.objects.filter(name = request.GET.get('name'))
    if not _cur_id:
        if len(_parentname) > 0:
            _parent = k_class.objects.filter(name=_parentname)
            if len(_parent) == 1:
                _id = _parent[0].id
                _depth = _parent[0].depth+1
            else:
                return HttpResponseRedirect('/department/?msg="父级类别有误！"')

            tmp_class = k_class.objects.filter(name = _name)
            if len(tmp_class) == 0:
                _class = k_class.objects.create(name=_name, parentid=_id,depth=_depth,memo=_memo, code=_code,
                                                license=_license, logo=_logo, address=_address, zipcode=_zipcode,
                                                phone=_phone, licensetype=_licensetype,content=_content,
                                                creatorid = request.user.id, createdatetime=get_current_date(),
                                                editorid=request.user.id, editdatetime=get_current_date())
                _class.save()
                return HttpResponseRedirect('/department/')
            else:
                return HttpResponseRedirect('/department/?msg=""'+_name+'"已存在！"')
        else:
            return HttpResponseRedirect('/department/?msg="父级类别有误！"')
    else:
        _tmp_class = k_class.objects.filter(id = _cur_id)
        if len(_tmp_class) == 1:
            _tmp_class[0].name = _name
            _tmp_class[0].license = _license
            _tmp_class[0].code = _code
            _tmp_class[0].logo = _logo
            _tmp_class[0].address = _address
            _tmp_class[0].zipcode = _zipcode
            _tmp_class[0].phone = _phone
            _tmp_class[0].licensetype = _licensetype
            _tmp_class[0].content = _content
            _tmp_class[0].memo = _memo
            _tmp_class[0].save()
            return HttpResponseRedirect('/department/?msg="修改部门（"'+_name+'"）成功！"')
        else:
            return HttpResponseRedirect('/department/?msg="修改部门信息失败！"')

@login_required
def department_del(request):
    _id = request.GET.get('id')
    if _id:
        _department = k_class.objects.filter(id=_id)
        if len(_department) == 1:
            _user = k_user.objects.filter(classid_id=_id)
            if len(_user) > 0:
                msg = "有"+str(len(_user))+"个用户属于该部门，无法删除部门："+_department[0].name
            else:
                msg = "成功删除部门："+_department[0].name
                _department[0].delete()
        else:
            msg = "该部门不存在！"
        return HttpResponseRedirect('/department/?msg='+msg)
    else:
        return HttpResponseRedirect('/department/')

'''部门设置结束'''


@login_required
def score(request):
    msg = request.GET.get("msg")
    if msg is None:
        msg = ""

    user=k_user.objects.get(username=request.user.username)
    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)

    try:
        project = k_project.objects.get(classid=department_class)
    except ObjectDoesNotExist:
        project = k_project(
            classid=department_class,
            meterscore=2,
            maintenancescore=2,
            taskscore=2
        )
        project.save()

    return get_purviews_and_render_to_response(request.user.username, 'score.html', {
        'meterscore': project.meterscore,
        'maintenancescore': project.maintenancescore,
        'taskscore': project.taskscore,
        'username':user.username,
        'useravatar': user.avatar,
        'msg': msg
    })


@login_required
def score_submit(request):
    meterscore = request.POST.get('meterscore')
    maintenancescore = request.POST.get('maintenancescore')
    taskscore = request.POST.get('taskscore')

    user = k_user.objects.get(username=request.user.username)
    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)

    try:
        project = k_project.objects.get(classid=department_class)
        project.meterscore = meterscore
        project.maintenancescore = maintenancescore
        project.taskscore = taskscore
        project.save()
    except ObjectDoesNotExist:
        project = k_project(
            classid=department_class,
            meterscore=meterscore,
            maintenancescore=maintenancescore,
            taskscore=taskscore,
        )
        project.save()

    return HttpResponseRedirect('/score/?msg=修改成功！')


@login_required
def score_history(request):
    user = k_user.objects.get(username=request.user.username)
    if request.method == "GET":
        #分类筛选
        user = k_user.objects.get(username=request.user.username)
        result = [user.classid.id]
        get_class_set(result, user.classid.id)
        class_list = list()
        classes = k_class.objects.filter(id__in=result)
        for c in classes:
            class_list.append(c.name)

        bonus_records = k_staffscoreinfo.objects.all()
        start_date_str = datetime.today().strftime("%Y-%m-01")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        bonus_records = bonus_records.filter(time__gte=start_date)


        bonus_users = k_user.objects.filter(classid__in=classes)
        bonus_records = bonus_records.filter(userid__in=bonus_users)

        show_record_type = 'monthly'
        data = []
        score_dict = dict()
        for bonus_record in bonus_records:
            key = str(bonus_record.userid.id) +  ',' + bonus_record.time.strftime("%Y-%m") \
            + ',' +bonus_record.userid.name + ',' + bonus_record.userid.classid.name
            score_dict[key] = score_dict.get(key, 0) + bonus_record.score
        
        for key, value in score_dict.items():
            res = key.split(',')
            d = {
                'date': res[1],
                'name': res[2],
                'dept': res[3],
                'score': value
            }
            data.append(d)
        data = sorted(data, key=lambda elem: (elem['date'], -elem['score'])) 
        return get_purviews_and_render_to_response(request.user.username, "score_history.html", {
            'bonus_records': data,
            'start_date': start_date_str,
            'username':user.username,
            'useravatar': user.avatar,
            'class_list': class_list,
            'classname': user.classid.name,
            'show_record_type': show_record_type
        })

    else:
        start_date_str = request.POST.get("start-date", "")
        end_date_str = request.POST.get("end-date", "")
        name = request.POST.get("name", "")
        classname = request.POST.get('classname', "")
        show_record_type = request.POST.get('show_record_type', "")
        bonus_records = k_staffscoreinfo.objects.all()

        user = k_user.objects.get(username=request.user.username)
        result = [user.classid.id]
        get_class_set(result, user.classid.id)
        class_list = list()
        classes = k_class.objects.filter(id__in=result)
        for c in classes:
            class_list.append(c.name)

        if start_date_str != "":
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            bonus_records = bonus_records.filter(time__gte=start_date)

        if end_date_str != "":
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            bonus_records = bonus_records.filter(time__lte=end_date)

        if classname != "":
            classid = k_class.objects.filter(name=classname)[0]
            res = [classid.id]
            get_class_set(res, classid.id)
            classlist = k_class.objects.filter(id__in=res)
            bonus_users = k_user.objects.filter(classid__in=classlist)
            bonus_records = bonus_records.filter(userid__in=bonus_users)

        if len(name) > 0:
            bonus_users = k_user.objects.filter(name=name)
            bonus_records = bonus_records.filter(userid__in=bonus_users)


        if show_record_type == 'detail':
            data = []
            for bonus_record in bonus_records:
                d = {
                    'date': bonus_record.time,
                    'name': bonus_record.userid.name,
                    'dept': bonus_record.userid.classid.name,
                    'score': bonus_record.score,
                    'scorebase': bonus_record.content.split(";")[0],
                    'scorefactor': bonus_record.content.split(";")[1],
                    'scoretype': bonus_record.content.split(";")[2]
                }
                data.append(d)
            return get_purviews_and_render_to_response(request.user.username, "score_history.html", {
                'bonus_records': data,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'username':user.username,
                'useravatar': user.avatar,
                'name': name,
                'class_list': class_list,
                'classname': classname,
                'show_record_type': show_record_type
            })
        else:
            data = []
            score_dict = dict()
            for bonus_record in bonus_records:
                key = str(bonus_record.userid.id) +  ',' + bonus_record.time.strftime("%Y-%m") \
                + ',' +bonus_record.userid.name + ',' + bonus_record.userid.classid.name
                score_dict[key] = score_dict.get(key, 0) + bonus_record.score
            
            for key, value in score_dict.items():
                res = key.split(',')
                d = {
                    'date': res[1],
                    'name': res[2],
                    'dept': res[3],
                    'score': value
                }
                data.append(d)
            data = sorted(data, key=lambda elem: (elem['date'], -elem['score'])) 
            return get_purviews_and_render_to_response(request.user.username, "score_history.html", {
                'bonus_records': data,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'username':user.username,
                'useravatar': user.avatar,
                'name': name,
                'class_list': class_list,
                'classname': classname,
                'show_record_type': show_record_type
            })


@login_required
def egg(request):
    msg = request.GET.get("msg")
    if msg is None:
        msg = ""

    user = k_user.objects.get(username=request.user.username)
    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)

    try:
        config = k_config.objects.get(classid=department_class)
    except ObjectDoesNotExist:
        config = k_config(
            eggbonus=0,
            eggprobability=0,
            classid=department_class,
            starttime=time(2, 0, 0, 0),
            endtime=time(4, 0, 0, 0)
        )
        config.save()

    return get_purviews_and_render_to_response(request.user.username, 'egg.html', {
        'bonus': config.eggbonus,
        'probability': config.eggprobability,
        'starttime': config.starttime.hour,
        'endtime': config.endtime.hour,
        'range': xrange(24),
        'username':user.username,
        'useravatar': user.avatar,
        'msg': msg
    })


@login_required
def egg_submit(request):
    bonus = request.POST.get('bonus')
    probability = request.POST.get('probability')
    start_time = request.POST.get('starttime')
    end_time = request.POST.get('endtime')


    if start_time.isdigit():
        start_time = int(start_time)

    if end_time.isdigit():
        end_time = int(end_time)

    user = k_user.objects.get(username=request.user.username)
    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)

    try:
        config = k_config.objects.get(classid=department_class)
        config.eggbonus = bonus
        config.eggprobability = probability
        config.classid = department_class
        config.starttime = time(start_time, 0, 0, 0)
        config.endtime = time(end_time, 0, 0, 0)
        config.save()
    except ObjectDoesNotExist:
        config = k_config(
            eggbonu=bonus,
            eggprobability=probability,
            classid=department_class,
            starttime=time(start_time, 0, 0, 0),
            endtime=time(end_time, 0, 0, 0)
        )
        config.save()

    return HttpResponseRedirect('/egg/?msg=修改成功！')


@login_required
def egg_history(request):
    user = k_user.objects.get(username=request.user.username)
    if request.method == "GET":
        return get_purviews_and_render_to_response(request.user.username, "egg_history.html", {
            'username':user.username,
            'useravatar': user.avatar
        })
    else:
        start_date_str = request.POST.get("start-date", "")
        end_date_str = request.POST.get("end-date", "")
        name = request.POST.get("name", "")
        bonus_records = k_staffegginfo.objects.all()

        if start_date_str != "":
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            bonus_records = bonus_records.filter(time__gte=start_date)

        if end_date_str != "":
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            bonus_records = bonus_records.filter(time__lte=end_date)


        if len(name) > 0:
            bonus_users = k_user.objects.filter(name=name)
            bonus_records = bonus_records.filter(userid__in=bonus_users)

        data = []
        for bonus_record in bonus_records:
            d = {
                'id': bonus_record.id,
                'date': bonus_record.time,
                'name': bonus_record.userid.name,
                'dept': bonus_record.userid.classid.name,
                'bonus': bonus_record.bonus,
                'probability': bonus_record.probability
            }

            if bonus_record.state == '0':
                d['state'] = u'未中奖'
            elif bonus_record.state == '1':
                d['state'] = u'中奖未领'
            elif bonus_record.state == '2':
                d['state'] = u'已领取'
            data.append(d)
        return get_purviews_and_render_to_response(request.user.username, "egg_history.html", {
            'bonus_records': data,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'username':user.username,
            'useravatar': user.avatar,
            'name': name
        })


@login_required
def receive_bonus(request, bonus_record_id=""):
    if request.method == 'POST':
        if bonus_record_id:
            bonus_record = k_staffegginfo.objects.filter(id=bonus_record_id)
            if len(bonus_record) > 0:
                bonus_record = bonus_record[0]
                bonus_record.state = 2                     #change state to received state
                bonus_record.save()
                return HttpResponse("ok")
            else:
                return HttpResponse("record not found")
        else:
            return HttpResponse("error")
    else:
        return HttpResponse("error")


def meter(request):
    if request.method == 'GET':
        today_this_month = date.today()
        today_last_month = date.today() - relativedelta(months=1)
        user = k_user.objects.get(username=request.user.username)
        brief = request.GET.get('brief')

        return get_purviews_and_render_to_response(request.user.username, 'meter.html', {
            'brief': brief,
            'username': user.username,
            'useravatar': user.avatar,
            'start_date': today_last_month,
            'end_date': today_this_month
        })


def meter_date(request):
    date_string_start = request.GET.get('date_start')
    date_string_end = request.GET.get('date_end')
    date_start = datetime.strptime(date_string_start, '%Y-%m-%d').date()
    date_end = datetime.strptime(date_string_end, '%Y-%m-%d').date()

    user = k_user.objects.get(username=request.user.username)

    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    meters = k_meter.objects.filter(metertime__range=(date_start, date_end + timedelta(days=1)), classid__in=result)
    data = []
    for m in meters:
        d = {'brief': m.brief, 'route': m.routeid.name if m.routeid else '', 'user': m.userid.name, 'time': m.metertime}
        json_dict = json.loads(m.json)
        if 'qrcode' in json_dict:
            if json_dict['qrcode'] == m.brief:
                d['check'] = u'已签到'
            else:
                d['check'] = u'签到错误'
            del json_dict['qrcode']
        else:
            d['check'] = u'未签到'
        d['content'] = json.dumps(json_dict, ensure_ascii=False).lstrip('{').rstrip('}').replace('\"', '')
        data.append(d)

    return get_purviews_and_render_to_response(request.user.username, 'meterview.html', {
        'meters': data,
        'search_type': 'date',
        'date_start': date_string_start,
        'date_end': date_string_end,
        'username':user.username,
        'useravatar': user.avatar
    })


def meter_device_date(request):
    brief = request.GET.get('brief')
    date_string_start = request.GET.get('date_start')
    date_string_end = request.GET.get('date_end')
    date_start = datetime.strptime(date_string_start, '%Y-%m-%d').date()
    date_end = datetime.strptime(date_string_end, '%Y-%m-%d').date()
    if not brief:
        return HttpResponseRedirect('/meter_date/?date_start=%s&date_end=%s' % (date_string_start, date_string_end))

    user = k_user.objects.get(username=request.user.username)

    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    meters = k_meter.objects.filter(metertime__range=(date_start, date_end + timedelta(days=1)), classid__in=result)
    if brief:
        meters = meters.filter(brief=brief)

    data = []
    arr = []
    for m in meters:
        d = {'brief': m.brief, 'route': m.routeid.name if m.routeid else '', 'user': m.userid.name, 'time': m.metertime}
        json_dict = json.loads(m.json)
        if 'qrcode' in json_dict:
            if json_dict['qrcode'] == m.brief:
                d['check'] = u'已签到'
            else:
                d['check'] = u'签到错误'
            del json_dict['qrcode']
        else:
            d['check'] = u'未签到'
        raw_str = m.json.lstrip('{').rstrip('}')
        r = re.compile('"(.*?)":"(.*?)"')
        arr = r.findall(raw_str)
        d['content'] = []
        for k, v in arr:
            if not k == 'qrcode':
                d['content'].append(v.strip())
        data.append(d)

    table_heads = []
    for k, v in arr:
        table_heads.append(k.strip())

    return get_purviews_and_render_to_response(request.user.username, 'meterview.html', {
        'heads': table_heads,
        'meters': data,
        'search_type': 'date_device' if brief else 'date',
        'brief': brief,
        'date_start': date_string_start,
        'date_end': date_string_end,
        'username':user.username,
        'useravatar': user.avatar
    })


def meter_export_date(request, start_date='', end_date=''):
    user = k_user.objects.get(username=request.user.username)

    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
    date_end = datetime.strptime(end_date, '%Y-%m-%d').date()

    meters = k_meter.objects.filter(metertime__range=(date_start, date_end + timedelta(days=1)), classid__in=result)

    data = []
    for m in meters:
        d = {
            'brief': m.brief,
            'route': m.routeid.name if m.routeid else '',
            'user': m.userid.name,
            'time': m.metertime.strftime('%Y-%m-%d %H:%M:%S')
        }
        json_dict = json.loads(m.json)
        if 'qrcode' in json_dict:
            if json_dict['qrcode'] == m.brief:
                d['check'] = u'已签到'
            else:
                d['check'] = u'签到错误'
            del json_dict['qrcode']
        else:
            d['check'] = u'未签到'
        d['content'] = json.dumps(json_dict, ensure_ascii=False).lstrip('{').rstrip('}').replace('\"', '')
        data.append(d)

    # 响应设置
    response = HttpResponse(mimetype='application/ms-excel')
    # 文件名
    response['Content-Disposition'] = 'attachment;filename=Data_%s_%s.xls' % (smart_str(start_date), smart_str(end_date))
    # 文件对象
    book = xlwt.Workbook(encoding='utf-8')
    # 工作表对象
    sheet = book.add_sheet('抄表数据')
    # 定义导出列
    columns = [
        {'key': 'time', 'head': '抄表时间', 'width': 256 * 22},
        {'key': 'user', 'head': '抄表人', 'width': 256 * 10},
        {'key': 'route', 'head': '抄表路线', 'width': 256 * 20},
        {'key': 'brief', 'head': '设备编号', 'width': 256 * 15},
        {'key': 'check', 'head': '签到状态', 'width': 256 * 12},
        {'key': 'content', 'head': '表单内容', 'width': 256 * 80}
    ]
    # 设置表头样式
    head_style = xlwt.easyxf('font: bold on;')
    # 写表头
    for col, item in enumerate(columns):
        sheet.write(0, col, item['head'], head_style)
        sheet.col(col).width = item['width']
    # 设置数据样式
    data_style = xlwt.easyxf('font: bold off;')
    # 写数据
    for row, m in enumerate(data):
        for col, x in enumerate(columns):
            sheet.write(row + 1, col, m[x['key']], data_style)

    book.save(response)
    return response


def meter_export_device_date(request, brief='', start_date='', end_date=''):
    user = k_user.objects.get(username=request.user.username)

    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
    date_end = datetime.strptime(end_date, '%Y-%m-%d').date()

    meters = k_meter.objects.filter(metertime__range=(date_start, date_end + timedelta(days=1)), classid__in=result)
    if brief:
        meters = meters.filter(brief=brief)

    data = []
    arr = []
    for m in meters:
        d = {
            'brief': m.brief,
            'route': m.routeid.name if m.routeid else '',
            'user': m.userid.name,
            'time': m.metertime.strftime('%Y-%m-%d %H:%M:%S')
        }
        json_dict = json.loads(m.json)
        if 'qrcode' in json_dict:
            if json_dict['qrcode'] == m.brief:
                d['check'] = u'已签到'
            else:
                d['check'] = u'签到错误'
            del json_dict['qrcode']
        else:
            d['check'] = u'未签到'
        raw_str = m.json.lstrip('{').rstrip('}')
        r = re.compile('"(.*?)":"(.*?)"')
        arr = r.findall(raw_str)
        d['content'] = []
        for k, v in arr:
            if not k == 'qrcode':
                d['content'].append(v.strip())
        data.append(d)

    table_heads = []
    for k, v in arr:
        table_heads.append(k.strip())

    # 响应设置
    response = HttpResponse(mimetype='application/ms-excel')
    # 文件名
    response['Content-Disposition'] = 'attachment;filename=Data_%s_%s_%s.xls' % (smart_str(brief), smart_str(start_date), smart_str(end_date))
    # 文件对象
    book = xlwt.Workbook(encoding='utf-8')
    # 工作表对象
    sheet = book.add_sheet('抄表数据')
    # 定义导出列
    columns = [
        {'key': 'time', 'head': '抄表时间', 'width': 256 * 22},
        {'key': 'user', 'head': '抄表人', 'width': 256 * 10},
        {'key': 'route', 'head': '抄表路线', 'width': 256 * 20},
        {'key': 'brief', 'head': '设备编号', 'width': 256 * 15},
        {'key': 'check', 'head': '签到状态', 'width': 256 * 12},
        # {'key': 'content', 'head': '表单内容', 'width': 256 * 80}
    ]
    for i, h in enumerate(table_heads):
        columns.append({
            'content': True,
            'key': i,
            'head': h,
            'width': 256 * 20
        })
    # 设置表头样式
    head_style = xlwt.easyxf('font: bold on;')
    # 写表头
    for col, item in enumerate(columns):
        sheet.write(0, col, item['head'], head_style)
        sheet.col(col).width = item['width']
    # 设置数据样式
    data_style = xlwt.easyxf('font: bold off;')
    # 写数据
    for row, m in enumerate(data):
        for col, x in enumerate(columns):
            if 'content' in x:
                sheet.write(row + 1, col, m['content'][x['key']], data_style)
            else:
                sheet.write(row + 1, col, m[x['key']], data_style)

    book.save(response)
    return response


@login_required
def attendance_history(request):
    user = k_user.objects.get(username=request.user.username)

    result = [user.classid.id]
    get_class_set(result, user.classid.id)

    if request.method == "GET":
        return get_purviews_and_render_to_response(request.user.username, "attendance_history.html", {
            'username': user.username,
            'useravatar': user.avatar
        })
    else:
        start_date_str = request.POST.get("start-date", "")
        end_date_str = request.POST.get("end-date", "")
        name = request.POST.get("name", "")
        attendance_records = k_staffworkinfo.objects.filter(classid__in=result)

        if start_date_str != "":
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            attendance_records = attendance_records.filter(date__gte=start_date)

        if end_date_str != "":
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            attendance_records = attendance_records.filter(date__lte=end_date)


        if len(name) > 0:
            attendance_users = k_user.objects.filter(name=name)
            attendance_records = attendance_records.filter(userid__in=attendance_users)

        data = []
        for attendance_record in attendance_records:
            d = {
                'date': attendance_record.date,
                'name': attendance_record.userid.name,
                'dept': attendance_record.userid.classid.name,
                'checkin': attendance_record.checkin,
                'checkout': attendance_record.checkout
            }
            data.append(d)
        return get_purviews_and_render_to_response(request.user.username, "attendance_history.html", {
            'attendance_records': data,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'name': name,
            'username':user.username,
            'useravatar': user.avatar
        })
