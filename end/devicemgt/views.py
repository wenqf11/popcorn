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
from datetime import datetime, timedelta
from helper import handle_uploaded_file, get_current_time, get_current_date, get_type_node, get_device_node, get_device_by_class
import json


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
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username, 'clicked_item': 'index', 'purview_msg': purview_msg})
    return render_to_response('index.html', variables)


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
        result.append(userdata)
    for c in child_node_list:
        userdata = dict()
        userdata["text"] = c.name.decode('utf-8')
        sub_child_list = k_class.objects.filter(parentid = c.id)
        sub_leaf_list = k_user.objects.filter(classid_id=c.id)
        if sub_child_list:
            userdata["nodes"] = get_node(sub_leaf_list, sub_child_list)
        elif sub_leaf_list:
            userdata["nodes"] = get_leaf(sub_leaf_list)
        result.append(userdata)
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
        leaf_list = k_user.objects.filter(classid_id=current_class_id)
        for leaf in leaf_list:
            userdata = dict()
            userdata["text"] = leaf.name.decode('utf-8')
            userdata["href"] = "/user?id=" + str(leaf.id)
            userdatas.append(userdata)
        for c in class_set:
            userdata = dict()
            userdata["text"] = c.name.decode('utf-8')
            child_list = k_class.objects.filter(parentid = c.id)
            leaf_list = k_user.objects.filter(classid_id=c.id)
            #if child_list:
            userdata["nodes"] = get_node(leaf_list, child_list)
            #elif leaf_list:
            #    userdata["nodes"] = get_leaf(leaf_list)
            userdatas.append(userdata)

        cur_datas = dict()
        datas = list()
        cur_datas["text"] = current_class.name.decode('utf-8')
        cur_datas['nodes'] = userdatas
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
            'clicked_item': 'user',
            'data': datas,
            'server_msg': server_msg
        })
        return render_to_response('user.html', variables)


@login_required
def operate_user(request):
    """
        update user information
    """
    if request.method == 'GET':
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
            key_list = ['state', 'username', 'name', 'face', 'mobile', 'email', 'address', 'zipcode', 'birthday',
                        'idcard', 'idcardtype', 'contact','contactmobile', 'content', 'memo', 'birthday']
            for key in key_list:
                userdata[key] = eval('theuser.' + key)

            userdata['class_name'] = theuser.classid.name

            k_chosed_roles = k_role.objects.filter(k_user=_id)
            chosed_roles = []
            for k_chosed_role in k_chosed_roles:
                chosed_roles.append(k_chosed_role.name)
            userdata['chosen_roles'] = chosed_roles
        else:
            userdata['isNew'] = True

        server_msg = request.GET.get('msg')
        if server_msg:
            variables = RequestContext(request, {'username': user.username, 'data': userdata, 'server_msg': server_msg})
        else:
            variables = RequestContext(request, {'username': user.username, 'data': userdata})
        return render_to_response('useroperate.html', variables)
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
    server_msg = ''
    cur_user_id = 0
    if request.method == 'POST':
        # face = handle_uploaded_file(request.POST['username'],request.FILES['face'])
        face = "../static/images/user.png"
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
                face=face,
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
                creatorid=0,
                createdatetime=get_current_date(),
                editorid=0,
                editdatetime=get_current_date(),
                auditorid=0,
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
            key_list = ['username', 'name', 'face', 'mobile', 'email', 'address', 'zipcode', 'birthday',
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
            variables = RequestContext(request, {'username': user.username, 'data': userdata, 'server_msg': server_msg})
        else:
            variables = RequestContext(request, {'username': user.username, 'data': userdata})
        return render_to_response('useradd.html',variables)


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
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    return render_to_response('userset.html', variables)

@login_required
def userbatch_add(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    return render_to_response('userbatchadd.html', variables)


@login_required
def userbatch_submit(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    return render_to_response('userbatchadd.html', variables)

'''
用户管理结束
设备管理开始
'''

@login_required
def devicebyclass(request):
    user = k_user.objects.get(username=request.user.username)
    #_class = k_class.objects.get(id=_user.classid)
    parents = user.classid
    classes = k_class.objects.all()
    datas = list()
    data = dict()
    data['text'] = parents.name
    data['nodes'] = get_device_by_class(classes, parents.id)
    if data['nodes']:
        datas.append(data)
        variables=RequestContext(request,{'username':user.username, 'data':datas})
        return render_to_response('devicebyclass.html',variables)
    else:
        return HttpResponseRedirect('/device/')

@login_required
def devicemgt(request):
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    server_msg = request.GET.get('msg')
    if server_msg == None:
        server_msg = ''
    devicetypes = k_devicetype.objects.all()
    parents = 0
    datas = get_device_node(devicetypes, parents) #获取节点树
    _id = request.GET.get('id')
    deviceinfo = dict()
    if (_id):
        device = k_device.objects.filter(id=_id)
        if len(device) == 1:
            device = device[0]
            deviceinfo['id'] = _id
            deviceinfo['brief'] = device.brief
            deviceinfo['name']  = device.name
            deviceinfo['position'] = device.position
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
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device', 'data':datas, 'server_msg':server_msg, 'deviceinfo':deviceinfo, 'purview_msg':purview_msg})
    else:
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device', 'data':datas, 'server_msg':server_msg, 'purview_msg':purview_msg})
    return render_to_response('device.html',variables)


@login_required
def operate_device(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
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
    classes = k_class.objects.filter(id__in=result)
    for c in classes:
        class_list.append(c.name)
    types = k_devicetype.objects.all()
    for t in types:
        type_list.append(t.name)
    suppliers = k_supplier.objects.all()
    for s in suppliers:
        supplier_list.append(s.name)
    producers = k_producer.objects.all()
    for p in producers:
        producer_list.append(p.name)
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
        _owner = k_user.objects.filter(id=thedevice.ownerid)
        if len(_owner) == 1:
            _owner = _owner[0]
            userdata['chosen_owner'] = _owner.name
    else:
        userdata['isNew'] = True
    variables = RequestContext(request, {'username': user.username, 'clicked_item': 'user', 'data': userdata, 'server_msg': server_msg})
    return render_to_response('deviceadd.html', variables)


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
                spare=request.POST['spare'],
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
            _device.save()
            server_msg = '添加设备成功！'
            return HttpResponseRedirect('/operate_device/?id='+str(_device.id)+'&msg='+server_msg)
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
            _dev.spare = request.POST['spare']
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
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
    variables = RequestContext(request, {'username': user.username, 'server_msg': server_msg})
    return render_to_response('devicebatchadd.html', variables)

@login_required
def devicebatch_submit(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
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
                    if obj_data['state'] == '正常':
                        _state = 1
                    elif obj_data['state'] == '停用':
                        _state = 2
                    elif obj_data['state'] == '故障':
                        _state = 3
                    elif obj_data['state'] == '维修':
                        _state = 4
                    elif obj_data['state'] == '保养':
                        _state = 5
                    else:
                        _state = 0

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
                        spare=obj_data['spare'],
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
                    _device.save()
                    success_num += 1
            server_msg = '成功添加'+str(success_num)+'条设备信息！'
            return HttpResponse(json.dumps({
                "server_msg":server_msg
                }), content_type="application/json")
        except Exception as e:
            server_msg = '第'+str(success_num+1)+'条数据添加有误！请检查所属部门、设备类别和责任人用户名是否正确！'
            print e
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
    user = User.objects.get(username=request.user.username)
    devicetypes = k_devicetype.objects.all()
    parents = 0
    datas = get_type_node(devicetypes, parents) #获取节点树
    server_msg = request.GET.get("msg")
    if server_msg == None:
        server_msg = ""
    variables = RequestContext(request,{'username': user.username, 'clicked_item': 'device', 'data': datas, 'server_msg': server_msg})
    return render_to_response('devicetype.html', variables)


@login_required
def device_type_add(request):
    user = User.objects.get(username=request.user.username)
    k_devicetypes = k_devicetype.objects.all()
    devicetypes = list()
    for k_type in k_devicetypes:
        devicetypes.append(k_type.name)
    variables = RequestContext(request, {'username': user.username, 'clicked_item': 'device', 'devicetypes': devicetypes})
    return render_to_response('devicetypeadd.html', variables)


@login_required
def device_type_submit(request):
    if not k_devicetype.objects.filter(name=request.GET.get('name')):
        _parentname = request.GET.get('parentname')
        _name = request.GET.get('name')
        _memo = request.GET.get('memo')
        if len(_parentname) == 0:
            _id = 0
            _depth = 0
            _type = k_devicetype.objects.create(
                name=_name,
                parentid=_id,
                depth=_depth,
                memo=_memo,
                creatorid=request.user.id,
                createdatetime=get_current_date(),
                editorid=request.user.id,
                editdatetime=get_current_date()
            )
            _type.save()
            return HttpResponseRedirect('/device_type/')
        else:
            _parent = k_devicetype.objects.filter(name=_parentname)
            if len(_parent) == 1:
                _id = _parent[0].id
                _depth = _parent[0].depth+1
                _type = k_devicetype.objects.create(
                    name=_name,
                    parentid=_id,
                    depth=_depth,
                    memo=_memo,
                    creatorid=request.user.id,
                    createdatetime=get_current_date(),
                    editorid=request.user.id,
                    editdatetime=get_current_date()
                )
                _type.save()
                return HttpResponseRedirect('/device_type/')
            else:
                return HttpResponseRedirect('/device_type/?msg="父级类别有误！"')
    else:
        return HttpResponseRedirect('/device_type/?msg="该设备名称已存在！"')


def supplier(request):
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

    return render_to_response('supplier.html', {'data': data})


@login_required
def add_supplier(request):
    user = User.objects.get(username=request.user.username)
    variables = RequestContext(request, {'username': user.username, 'clicked_item': 'device'})
    return render_to_response('supplieradd.html', variables)

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
        if not k_supplier.objects.filter(name = request.GET.get('name')):
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
        else:
            return HttpResponseRedirect('/supplier/?msg="该供应商已存在！"')
    return HttpResponseRedirect('/supplier/')


@login_required
def producer(request):
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

    return render_to_response('producer.html', {'data': data})


@login_required
def add_producer(request):
    user = User.objects.get(username=request.user.username)
    variables = RequestContext(request, {'username': user.username, 'clicked_item': 'device'})
    return render_to_response('produceradd.html', variables)


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
        if not k_producer.objects.filter(name = request.GET.get('name')):
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
        else:
            return HttpResponseRedirect('/producer/?msg="error1"')


# 个人信息
@login_required
def profile(request):
    if request.method == "GET":
        user = k_user.objects.get(username=request.user.username)
        #user = User.objects.get(username=request.user.username)

        return render_to_response('profile.html', {
            'user': user
        }, context_instance=RequestContext(request))
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
        return render_to_response('profile.html', {
            'user': user,
            "msg": msg
        }, context_instance=RequestContext(request))


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
            "msg": msg
        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/profile/")


@login_required
def setting(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username, 'clicked_item': 'setting'})
    return render_to_response('setting.html', variables)


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
                return render_to_response('index.html', {'username': username})
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


def view_schedule(request):
    if request.method == 'GET':
        users = k_user.objects.all() # 此处应取对应班组的用户
        user_data = [{'id': user.id, 'name': user.username} for user in users]

        routes = k_route.objects.all()
        route_data = [{'id': r.id, 'name': r.name, 'startTime': r.starttime, 'period': r.period} for r in routes]

        return render_to_response('schedule.html', {'routes': route_data, 'users': user_data})
    else:
        routes = k_route.objects.all()
        route_data = [{'id': _r.id, 'name': _r.name, 'startTime': str(_r.starttime), 'period': _r.period} for _r in routes]

        available_shifts = k_schedule.objects.filter(
            date__range=[date.today() - timedelta(days=30), date.today() + timedelta(days=30)]
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
        thecreator = k_user.objects.get(id=p.creatorid)
        therole = k_role.objects.get(name=p.name)
        onerole["creator"] = thecreator.username
        onerole["createdatetime"] = therole.createdatetime
        theeditor = k_user.objects.get(id=p.editorid)
        onerole["editor"] = theeditor.username
        onerole["editdatetime"] = therole.editdatetime
        roledata.append(onerole)
    return render_to_response('roleview.html', {'username': user.username, 'data': roledata})


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
        thecreator = k_user.objects.get(id=therole.creatorid)
        roledata["creator"] = thecreator.username
        roledata["createdatetime"] = therole.createdatetime
        theeditor = k_user.objects.get(id=therole.editorid)
        roledata["editor"] = theeditor.username
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
        return render_to_response('roleoperate.html', {'username':user.username,'isNew': False, 'data': roledata, "classes": _classes, 'server_msg': server_msg})
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

        return render_to_response('roleoperate.html', {'username':user.username,'isNew': True, 'data': data, "classes": _classes, 'server_msg': server_msg})


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
    routes = k_route.objects.all()
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
        route['period'] = r.period
        route['creator'] = k_user.objects.get(id=r.creatorid).username
        route['createTime'] = r.createdatetime
        route['editor'] = k_user.objects.get(id=r.editorid).username
        route['editTime'] = r.editdatetime
        route['auditor'] = k_user.objects.get(id=r.auditorid).username
        route['auditTime'] = r.auditdatetime
        #route['status'] = r.status
        data.append(route)
    return render_to_response('routeview.html', {'routes': data})


@login_required
def operate_route(request):
    data = {}
    _id = request.GET.get('id')

    if _id:
        # 修改路线
        _route = k_route.objects.get(id=_id)
        data['id'] = _route.id
        _forms = _route.formid.split(',')
        data['name'] = _route.name
        data['startTime'] = _route.starttime
        data['period'] = _route.period
        data['creator'] = k_user.objects.get(id=_route.creatorid).username
        data['createTime'] = _route.createdatetime
        data['editor'] = k_user.objects.get(id=_route.editorid).username
        data['editTime'] = _route.editdatetime

        all_form = k_form.objects.all()
        data['forms'] = [{
            'id': _form.id,
            'brief': _form.brief,
            'selected': str(_form.id) in _forms
        } for _form in all_form]

        data['routeString'] = _route.formid

        return render_to_response('routeoperate.html', {'isNew': False, 'data': data})
    else:
        # 添加路线
        data['forms'] = []
        all_form = k_form.objects.all()
        for _form in all_form:
            data['forms'].append({
                'id': _form.id,
                'brief': _form.brief,
                'selected': False
            })
        return render_to_response('routeoperate.html', {'isNew': True, 'data': data})


@login_required
def submit_route(request, _id=''):
    _user = k_user.objects.get(username=request.user.username)
    _editor = _user.id
    _forms = request.POST.get('routeString')
    _name = request.POST.get('name')
    _period = request.POST.get('period')
    # _start_time = request.GET.get('startTime')
    _hour = request.POST.get('hour')
    _minute = request.POST.get('minute')
    _start_time = _hour + ':' + _minute
    _edit_time = get_current_date()
    if _id:
        route = k_route.objects.get(id=_id)
    else:
        route = k_route(classid=_user.classid)
        route.creatorid = _editor
    route.name = _name
    route.formid = _forms
    route.starttime = datetime.strptime(_start_time, '%H:%M').time()
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
    return render_to_response('formview.html', {'brief': _brief, 'formid': _form.id, 'data': _formitems})


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
def view_deviceplan(request):
    #权限判断
    _msg = check_purview(request.user.username, 28)
    if _msg != 0:
        return HttpResponseRedirect('/device/?msg='+_msg)

    _deviceid = request.GET.get('id')
    _device = k_device.objects.get(id=_deviceid)
    _brief = _device.brief
    _deviceplans = k_deviceplan.objects.filter(deviceid=_device)
    data = []
    for _deviceplan in _deviceplans:
        _assignor = k_user.objects.get(id=_deviceplan.assignorid)
        _editor = k_user.objects.get(id=_deviceplan.editorid)
        data.append({
            'id': _deviceplan.id,
            'title': _deviceplan.title,
            'period': _deviceplan.get_period_display(),
            'createcontent': _deviceplan.createcontent,
            'memo': _deviceplan.memo,
            'assignor': _assignor.name,
            'assigndatetime': _deviceplan.assigndatetime,
            'editor': _editor.name
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

    return render_to_response('deviceplanview.html', {'brief': _brief, 'deviceid': _deviceid, 'data': data, 'maintainers': _maintainers, 'purview_msg': purview_msg})


@login_required
def submit_deviceplan(request):
    _deviceid = request.GET.get('deviceid')
    #权限判断
    _msg = check_purview(request.user.username, 29)
    if _msg != 0:
        return HttpResponseRedirect('/view_deviceplan/?msg='+_msg+'&id='+_deviceid)
    
    _title = request.GET.get('title')
    _period = request.GET.get('period')
    _createcontent = request.GET.get('createcontent')
    _editor = request.GET.get('editor')
    _memo = request.GET.get('memo')

    _id = request.GET.get('id')
    _user = k_user.objects.get(username=request.user.username)
    _editor = k_user.objects.get(name=_editor)

    if _id != "":
        _deviceplan = k_deviceplan.objects.get(id=_id)
        _maintenance = k_maintenance.objects.get(id=_deviceplan.maintenanceid_id)
    else:
        _maintenance = k_maintenance.objects.create(mtype=1,deviceid_id=_deviceid,state=2)
        _deviceplan = k_deviceplan.objects.create(deviceid_id=_deviceid,maintenanceid=_maintenance)

    _maintenance.assignorid = _user.id
    _maintenance.assigndatetime = get_current_date()
    _maintenance.title = _title
    _maintenance.createcontent = _createcontent
    _maintenance.editorid = _editor.id
    _maintenance.memo = _memo
    _maintenance.save()

    _deviceplan.assignorid = _user.id
    _deviceplan.assigndatetime = get_current_date()
    _deviceplan.title = _title
    _deviceplan.period = _period
    _deviceplan.createcontent = _createcontent
    _deviceplan.editorid = _editor.id
    _deviceplan.memo = _memo
    _deviceplan.save()

    return HttpResponseRedirect('/view_deviceplan/?id='+_deviceid)


@login_required
def delete_deviceplan(request):
    _id = request.GET.get('id')
    _deviceid = request.GET.get('deviceid')
    #权限判断
    _msg = check_purview(request.user.username, 30)
    if _msg != 0:
        return HttpResponseRedirect('/view_deviceplan/?msg='+_msg+'&id='+_deviceid)
    
    if _id:
        _deviceplan = k_deviceplan.objects.get(id=_id)
        _deviceplan.delete()
    return HttpResponseRedirect('/view_deviceplan/?id='+_deviceid)


@login_required
def view_maintaining(request):
    #权限判断
    _msg = check_purview(request.user.username, 31)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    # user = k_user.objects.get(username=request.user.username)
    # result = [user.classid.id]
    # get_class_set(result, user.classid.id)
    # _maintainings = k_maintenance.objects.filter(classid__in=result, mtype=2, state__lte=3)
    _maintainings = k_maintenance.objects.filter(mtype=2, state__lte=3)

    data = []
    for _maintaining in _maintainings:
        _device = _maintaining.deviceid
        _db = _dn = _dp = ""
        if _device != None:
            _db = _device.brief
            _dn = _device.name
            _dp = _device.position
        _creator = k_user.objects.get(id=_maintaining.creatorid)
        if _maintaining.assignorid == 0:
            data.append({
                'id': _maintaining.id,
                'title': _maintaining.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'creator': _creator.name,
                'createdatetime': _maintaining.createdatetime,
                'createcontent': _maintaining.createcontent,
                'memo': _maintaining.memo,
                'priority': _maintaining.get_priority_display(),
                'state': _maintaining.state
            })
        else:
            _assignor = k_user.objects.get(id=_maintaining.assignorid)
            _editor = k_user.objects.get(id=_maintaining.editorid)
            data.append({
                'id': _maintaining.id,
                'title': _maintaining.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'creator': _creator.name,
                'createdatetime': _maintaining.createdatetime,
                'assignor': _assignor.name,
                'assigndatetime': _maintaining.assigndatetime,
                'editor': _editor.name,
                'createcontent': _maintaining.createcontent,
                'memo': _maintaining.memo,
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
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''

    return render_to_response('maintainingview.html', {'data': data, 'maintainers': _maintainers, 'purview_msg': purview_msg})


@login_required
def view_maintained(request):
    #权限判断
    _msg = check_purview(request.user.username, 31)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    # user = k_user.objects.get(username=request.user.username)
    # result = [user.classid.id]
    # get_class_set(result, user.classid.id)
    # _maintaineds = k_maintenance.objects.filter(classid__in=result, mtype=2, state__gte=4)
    _maintaineds = k_maintenance.objects.filter(mtype=2, state__gte=4)

    data = []
    for _maintained in _maintaineds:
        _device = _maintained.deviceid
        _db = _dn = _dp = ""
        if _device != None:
            _db = _device.brief
            _dn = _device.name
            _dp = _device.position
        _creator = k_user.objects.get(id=_maintained.creatorid)
        _assignor = k_user.objects.get(id=_maintained.assignorid)
        _editor = k_user.objects.get(id=_maintained.editorid)
        if _maintained.auditorid == 0:
            data.append({
                'id': _maintained.id,
                'title': _maintained.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'creator': _creator.name,
                'createdatetime': _maintained.createdatetime,
                'assignor': _assignor.name,
                'assigndatetime': _maintained.assigndatetime,
                'editor': _editor.name,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': _maintained.memo,
                'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'state': _maintained.state
            })
        else:
            _auditor = k_user.objects.get(id=_maintained.auditorid)
            data.append({
                'id': _maintained.id,
                'title': _maintained.title,
                'brief': _db,
                'name': _dn,
                'position': _dp,
                'creator': _creator.name,
                'createdatetime': _maintained.createdatetime,
                'assignor': _assignor.name,
                'assigndatetime': _maintained.assigndatetime,
                'editor': _editor.name,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': _maintained.memo,
                'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'auditor': _auditor.name,
                'auditdatetime': _maintained.auditdatetime,
                'factor': _maintained.factor,
                'state': _maintained.state
            })
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''

    return render_to_response('maintainedview.html', {'data': data, 'purview_msg': purview_msg})


@login_required
def add_maintenance(request):
    #权限判断
    _msg = check_purview(request.user.username, 33)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)
    
    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _users = k_user.objects.filter(classid__in=result)
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    _devices = k_device.objects.filter(classid__in=result)
    _briefs = []
    for _device in _devices:
        _briefs.append(_device.brief)
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return render_to_response('maintenanceadd.html', {'maintainers': _maintainers, 'briefs': _briefs, 'purview_msg': purview_msg})


@login_required
def submit_maintenance(request):
    _id = request.GET.get('id')
    _factor = request.GET.get('factor')
    _editor = request.GET.get('editor')
    #权限判断
    if _factor:
        _msg = check_purview(request.user.username, 34)
        if _msg != 0:
            return HttpResponseRedirect('/view_maintained/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 33)
        if _msg != 0:
            return HttpResponseRedirect('/view_maintaining/?msg='+_msg)
        if _id:
            _maintenance = k_maintenance.objects.get(id=_id)
            if _editor == "nopersonchosen":
                if _maintenance.editorid != 0:
                    _msg = check_purview(request.user.username, 32)
                    if _msg != 0:
                        return HttpResponseRedirect('/view_maintaining/?msg='+_msg)
            else:
                _maintainer = k_user.objects.get(name=_editor)
                if _maintenance.editorid != _maintainer.id:
                    _msg = check_purview(request.user.username, 32)
                    if _msg != 0:
                        return HttpResponseRedirect('/view_maintaining/?msg='+_msg)
        else:
            if _editor != "nopersonchosen":
                _msg = check_purview(request.user.username, 32)
                if _msg != 0:
                    return HttpResponseRedirect('/add_maintenance/?msg='+_msg)
    
    _title = request.GET.get('title')
    _brief = request.GET.get('brief')
    _createcontent = request.GET.get('createcontent')
    _priority = request.GET.get('priority')
    _memo = request.GET.get('memo')

    _user = k_user.objects.get(username=request.user.username)
    if _factor:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.auditorid = _user.id
        _maintenance.auditdatetime = get_current_date()
        _maintenance.factor = _factor
        _maintenance.state = 5
        _maintenance.save()
        return HttpResponseRedirect('/view_maintained/')
    elif _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        if _editor != "nopersonchosen":
            _maintainer = k_user.objects.get(name=_editor)
            _maintenance.editorid = _maintainer.id
            _maintenance.assignorid = _user.id
            _maintenance.assigndatetime = get_current_date()
            _maintenance.state = 2
        else:
            _maintenance.editorid = 0
            _maintenance.assignorid = 0
            _maintenance.state = 1           
        _maintenance.title = _title
        _maintenance.createcontent = _createcontent
        _maintenance.priority = _priority
        _maintenance.memo = _memo
    else:
        _maintenance = k_maintenance.objects.create(
            title=_title,
            createcontent=_createcontent,
            priority=_priority,
            memo=_memo,
            creatorid=_user.id,
            createdatetime=get_current_date(),
            state=1,
            mtype=2
        )
        if _brief != 'nopersonchosen':
            _device = k_device.objects.filter(brief=_brief)
            _maintenance.deviceid=_device[0]
        if _editor != 'nopersonchosen':
            _maintenance.assignorid = _user.id
            _maintenance.assigndatetime = get_current_date()
            _maintainer = k_user.objects.get(name=_editor)
            _maintenance.editorid = _maintainer.id
            _maintenance.state = 2
    _maintenance.save()
    return HttpResponseRedirect('/view_maintaining/')


@login_required
def delete_maintenance(request):
    _type = request.GET.get('type')
    #权限判断
    _msg = check_purview(request.user.username, 34)
    if _msg != 0:
        if _type == "1":
            return HttpResponseRedirect('/view_maintained/?msg='+_msg)
        else:
            return HttpResponseRedirect('/view_maintaining/?msg='+_msg)

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
    _msg = check_purview(request.user.username, 28)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    # user = k_user.objects.get(username=request.user.username)
    # result = [user.classid.id]
    # get_class_set(result, user.classid.id)
    # _maintainings = k_maintenance.objects.filter(classid__in=result, mtype=1, state__lte=3)
    _maintainings = k_maintenance.objects.filter(mtype=1, state__lte=3)

    data = []
    for _maintaining in _maintainings:
        _device = _maintaining.deviceid
        _assignor = k_user.objects.get(id=_maintaining.assignorid)
        _editor = k_user.objects.get(id=_maintaining.editorid)
        data.append({
            'id': _maintaining.id,
            'title': _maintaining.title,
            'brief': _device.brief,
            'name': _device.name,
            'position': _device.position,
            'assignor': _assignor.name,
            'assigndatetime': _maintaining.assigndatetime,
            #
            'deadline': get_current_date(),
            'editor': _editor.name,
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

    return render_to_response('upkeepingview.html', {'data': data, 'maintainers': _maintainers, 'purview_msg': purview_msg})

@login_required
def view_upkeeped(request):
    #权限判断
    _msg = check_purview(request.user.username, 28)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    # user = k_user.objects.get(username=request.user.username)
    # result = [user.classid.id]
    # get_class_set(result, user.classid.id)
    # _maintaineds = k_maintenance.objects.filter(classid__in=result, mtype=1, state__gte=4)
    _maintaineds = k_maintenance.objects.filter(mtype=1, state__gte=4)

    data = []
    for _maintained in _maintaineds:
        _device = _maintained.deviceid
        #_creator = k_user.objects.get(id=_maintained.creatorid)
        _assignor = k_user.objects.get(id=_maintained.assignorid)
        _editor = k_user.objects.get(id=_maintained.editorid)
        if _maintained.auditorid == 0:
            data.append({
                'id': _maintained.id,
                'title': _maintained.title,
                'brief': _device.brief,
                'name': _device.name,
                'position': _device.position,
                #'creator': _creator.name,
                #'createdatetime': _maintained.createdatetime,
                'assignor': _assignor.name,
                'assigndatetime': _maintained.assigndatetime,
                #
                'deadline': get_current_date(),
                'editor': _editor.name,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': _maintained.memo,
                #'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'state': _maintained.state
            })
        else:
            _auditor = k_user.objects.get(id=_maintained.auditorid)
            data.append({
                'id': _maintained.id,
                'title': _maintained.title,
                'brief': _device.brief,
                'name': _device.name,
                'position': _device.position,
                #'creator': _creator.name,
                #'createdatetime': _maintained.createdatetime,
                'assignor': _assignor.name,
                'assigndatetime': _maintained.assigndatetime,
                #
                'deadline': get_current_date(),
                'editor': _editor.name,
                'editdatetime': _maintained.editdatetime,
                'createcontent': _maintained.createcontent,
                'memo': _maintained.memo,
                #'priority': _maintained.get_priority_display(),
                'editcontent': _maintained.editcontent,
                'auditor': _auditor.name,
                'auditdatetime': _maintained.auditdatetime,
                'factor': _maintained.factor,
                'state': _maintained.state
            })
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return render_to_response('upkeepedview.html', {'data': data, 'purview_msg': purview_msg})


@login_required
def submit_upkeep(request):
    #权限判断
    _msg = check_purview(request.user.username, 30)
    if _msg != 0:
        return HttpResponseRedirect('/view_upkeeped/?msg='+_msg)
        
    _id = request.GET.get('id')
    _factor = request.GET.get('factor')
    _user = k_user.objects.get(username=request.user.username)
    _maintenance = k_maintenance.objects.get(id=_id)
    _maintenance.auditorid = _user.id
    _maintenance.auditdatetime = get_current_date()
    _maintenance.factor = _factor
    _maintenance.state = 5
    _maintenance.save()
    return HttpResponseRedirect('/view_upkeeped/')


@login_required
def delete_upkeep(request):
    #权限判断
    _msg = check_purview(request.user.username, 30)
    if _msg != 0:
        return HttpResponseRedirect('/view_upkeeped/?msg='+_msg)
        
    _id = request.GET.get('id')
    if _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.delete()
    return HttpResponseRedirect('/view_upkeeped/')


@login_required
def view_tasking(request):
    #权限判断
    _msg = check_purview(request.user.username, 35)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    # user = k_user.objects.get(username=request.user.username)
    # result = [user.classid.id]
    # get_class_set(result, user.classid.id)
    # _maintainings = k_task.objects.filter(classid__in=result, state__lte=2)
    _maintainings = k_task.objects.filter(state__lte=2)

    data = []
    for _maintaining in _maintainings:
        _creator = k_user.objects.get(id=_maintaining.creatorid)
        data.append({
            'id': _maintaining.id,
            'title': _maintaining.title,
            'creator': _creator.name,
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

    return render_to_response('taskingview.html', {'data': data, 'purview_msg': purview_msg})


@login_required
def view_tasked(request):
    #权限判断
    _msg = check_purview(request.user.username, 35)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    # user = k_user.objects.get(username=request.user.username)
    # result = [user.classid.id]
    # get_class_set(result, user.classid.id)
    # _maintaineds = k_task.objects.filter(state__gte=3)
    _maintaineds = k_task.objects.filter(classid__in=result, state__gte=3)

    data = []
    for _maintained in _maintaineds:
        _creator = k_user.objects.get(id=_maintained.creatorid)
        data.append({
            'id': _maintained.id,
            'title': _maintained.title,
            'creator': _creator.name,
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

    return render_to_response('taskedview.html', {'data': data, 'purview_msg': purview_msg})


@login_required
def add_task(request):
    #权限判断
    _msg = check_purview(request.user.username, 37)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)
        
    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return render_to_response('taskadd.html', {'purview_msg': purview_msg})


@login_required
def submit_task(request):
    #权限判断
    _msg = check_purview(request.user.username, 37)
    if _msg != 0:
        return HttpResponseRedirect('/view_tasking/?msg='+_msg)
        
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
    _msg = check_purview(request.user.username, 38)
    if _msg != 0:
        if _type == "1":
            return HttpResponseRedirect('/view_tasked/?msg='+_msg)
        else:
            return HttpResponseRedirect('/view_tasking/?msg='+_msg)
        
    if _id:
        _maintenance = k_task.objects.get(id=_id)
        _maintenance.delete()
    if _type == "1":
        return HttpResponseRedirect('/view_tasked/')
    else:
        return HttpResponseRedirect('/view_tasking/')


@login_required
def view_taskitem(request):
    #权限判断
    _msg = check_purview(request.user.username, 35)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    _id = request.GET.get('id')
    _task = k_task.objects.get(id=_id)
    _taskitems = k_taskitem.objects.filter(taskid_id=_task.id)
    data = []
    for _taskitem in _taskitems:
        dataitem = {}

        _creator = k_user.objects.get(id=_taskitem.creatorid)
        _editor = k_user.objects.get(id=_taskitem.editorid)
        _helpersid = _taskitem.helpersid.split(";")
        _helpers = []
        if _helpersid != ['']:
            for _helperid in _helpersid:
                _helper = k_user.objects.get(id=int(_helperid))
                _helpers.append(_helper.name)
        dataitem['id'] = _taskitem.id
        dataitem['title'] = _taskitem.title
        dataitem['createcontent'] = _taskitem.createcontent
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _taskitem.createdatetime
        dataitem['priority'] = _taskitem.get_priority_display()
        dataitem['memo'] = _taskitem.memo
        dataitem['editor'] = _editor.name
        dataitem['helpers'] = ";".join(_helpers)
        dataitem['state'] = _taskitem.get_state_display()

        if _taskitem.state == "3" or _taskitem.state == "4":
            dataitem['editdatetime'] = _taskitem.editdatetime
            dataitem['editcontent'] = _taskitem.editcontent

        if _taskitem.state == "4":
            _auditor = k_user.objects.get(id=_taskitem.auditorid)
            dataitem['auditor'] = _auditor.name
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

    return render_to_response('taskitemview.html', {'title': _task.title, 'taskers': _taskers, 'taskid': _task.id, 'data': data, 'purview_msg': purview_msg})


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
    if _submittype == "1":
        _msg = check_purview(request.user.username, 38)
        if _msg != 0:
            return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)
    elif _submittype == "2":
        _msg = check_purview(request.user.username, 37)
        if _msg != 0:
            return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)

        # _taskitem = k_taskitem.objects.get(id=_id)

        # _tasker = k_user.objects.get(name=_editor)
        # if _taskitem.editorid != _tasker.id:
        #     _msg = check_purview(request.user.username, 36)
        #     if _msg != 0:
        #         return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)
    else:
        _msg = check_purview(request.user.username, 37)
        if _msg != 0:
            return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)
        # _msg = check_purview(request.user.username, 36)
        # if _msg != 0:
        #     return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id='+_taskid)


    if _submittype == "1":
        _taskitem = k_taskitem.objects.get(id=_id)
        _taskitem.auditorid = _user.id
        _taskitem.auditdatetime = get_current_date()
        _taskitem.factor = _factor
        _taskitem.state = 4
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
        return HttpResponseRedirect('/view_taskitem?id=%i' % _taskitem.taskid_id)
    
    if _submittype == "2":
        _taskitem = k_taskitem.objects.get(id=_id)
    else:
        _taskitem = k_taskitem.objects.create(taskid_id=_taskid, state=1)
        _task = k_task.objects.get(id=_taskid)
        _task.state = 1
        _task.save()
    _taskitem.creatorid = _user.id
    _taskitem.createdatetime = get_current_date()
    _taskitem.title = _title
    _taskitem.createcontent = _createcontent
    _taskitem.priority = _priority
    _taskitem.memo = _memo
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
    _msg = check_purview(request.user.username, 38)
    if _msg != 0:
        return HttpResponseRedirect('/view_taskitem/?msg='+_msg+'&id=%i' % _taskitem.taskid_id)

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
    _msg = check_purview(request.user.username, 22)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _spares = k_spare.objects.filter(classid__in=result)

    data = []
    for _spare in _spares:
        dataitem = {}

        _creator = k_user.objects.get(id=_spare.creatorid)
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
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _spare.createdatetime

        if _spare.editorid != 0:
            _editor = k_user.objects.get(id=_spare.editorid)
            dataitem['editor'] = _editor.name
            dataitem['editdatetime'] = _spare.editdatetime

        if _spare.auditorid != 0:
            _auditor = k_user.objects.get(id=_spare.auditorid)
            dataitem['auditor'] = _auditor.name
            dataitem['auditdatetime'] = _spare.auditdatetime

        data.append(dataitem)

    #非法权限信息
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg

    return render_to_response('spare.html', {"data": data, 'purview_msg': purview_msg})


def operate_spare(request):
    _id = request.GET.get('id')
    #权限判断
    _msg = check_purview(request.user.username, 23)
    if _msg != 0:
        if _id:
            return HttpResponseRedirect('/view_spare/?msg='+_msg)
        else:
            return HttpResponseRedirect('/?msg='+_msg)

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

    return render_to_response('spareoperate.html', {"data": _data, "producers": _producers, "suppliers": _suppliers, "classes": _classes, 'server_msg': server_msg, 'purview_msg': purview_msg})


def submit_spare(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    if _audit:
        _msg = check_purview(request.user.username, 24)
        if _msg != 0:
            return HttpResponseRedirect('/view_spare/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 23)
        if _msg != 0:
            return HttpResponseRedirect('/view_spare/?msg='+_msg)

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
        _spares = k_spare.objects.filter(name=_name)
        if len(_spares) > 1 or (len(_spares) == 1 and _spares[0].id != int(_id)):
            server_msg = '名称为'+_spares[0].name+'的备件已存在！'
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
        _spares = k_spare.objects.filter(name=_name)
        if len(_spares) > 0:
            server_msg = '名称为'+_spares[0].name+'的备件已存在！'
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
    _msg = check_purview(request.user.username, 24)
    if _msg != 0:
        return HttpResponseRedirect('/view_spare/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _sparebills = k_sparebill.objects.filter(spareid=_spare)
        _sparecounts = k_sparecount.objects.filter(spareid=_spare)
        _spare.delete()
        _sparebills.delete()
        _sparecounts.delete()
    return HttpResponseRedirect('/view_spare')


@login_required
def sparebatch_add(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    variables = RequestContext(request, {'username': user.username})
    return render_to_response('sparebatchadd.html', variables)

@login_required
def sparebatch_submit(request):
    # 登陆成功
    # user = k_user.objects.get(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    # 读取权限，显示内容
    #variables = RequestContext(request, {'username': user.username})
    #return render_to_response('sparebatchadd.html', variables)
    return HttpResponse(json.dumps({
                "username": user.username,
                "test":"test"
                }
            ), content_type="application/json")

def view_sparebill(request):
    #权限判断
    _msg = check_purview(request.user.username, 39)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _sparebills = k_sparebill.objects.filter(classid__in=result)

    data = []
    for _sparebill in _sparebills:
        dataitem = {}

        _creator = k_user.objects.get(id=_sparebill.creatorid)
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        dataitem['id'] = _sparebill.id
        dataitem['brief'] = _spare.brief
        dataitem['using'] = _sparebill.using
        dataitem['returned'] = _sparebill.returned
        dataitem['depleted'] = _sparebill.depleted
        dataitem['damaged'] = _sparebill.damaged
        dataitem['rejected'] = _sparebill.rejected
        dataitem['user'] = _sparebill.user
        dataitem['memo'] = _sparebill.memo
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _sparebill.createdatetime

        dataitem['notreturned'] = dataitem['using'] - dataitem['returned'] - dataitem['depleted'] - dataitem['damaged'] - dataitem['rejected']

        if _sparebill.editorid != 0:
            _editor = k_user.objects.get(id=_sparebill.editorid)
            dataitem['editor'] = _editor.name
            dataitem['editdatetime'] = _sparebill.editdatetime

        if _sparebill.auditorid != 0:
            _auditor = k_user.objects.get(id=_sparebill.auditorid)
            dataitem['auditor'] = _auditor.name
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


    #return render_to_response('sparebill.html', {'data': data, 'briefs': _briefs})
    return render_to_response('sparebill.html', {'data': data, 'briefinfos': _briefinfos, 'server_msg': server_msg, 'purview_msg': purview_msg})


def submit_sparebill(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    if _audit:
        _msg = check_purview(request.user.username, 41)
        if _msg != 0:
            return HttpResponseRedirect('/view_sparebill/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 40)
        if _msg != 0:
            return HttpResponseRedirect('/view_sparebill/?msg='+_msg)

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
    _msg = check_purview(request.user.username, 41)
    if _msg != 0:
        return HttpResponseRedirect('/view_sparebill/?msg='+_msg)

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
    _msg = check_purview(request.user.username, 39)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _sparecounts = k_sparecount.objects.filter(classid__in=result)

    data = []
    for _sparecount in _sparecounts:
        dataitem = {}

        _creator = k_user.objects.get(id=_sparecount.creatorid)
        _spare = k_spare.objects.get(id=_sparecount.spareid_id)
        dataitem['id'] = _sparecount.id
        dataitem['sparebillid'] = _sparecount.sparebillid
        dataitem['brief'] = _spare.brief
        dataitem['count'] = _sparecount.count
        dataitem['state'] = _sparecount.get_state_display()
        dataitem['iseligible'] = _sparecount.get_iseligible_display()
        dataitem['memo'] = _sparecount.memo
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _sparecount.createdatetime

        if _sparecount.editorid != 0:
            _editor = k_user.objects.get(id=_sparecount.editorid)
            dataitem['editor'] = _editor.name
            dataitem['editdatetime'] = _sparecount.editdatetime

        if _sparecount.auditorid != 0:
            _auditor = k_user.objects.get(id=_sparecount.auditorid)
            dataitem['auditor'] = _auditor.name
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


    #return render_to_response('sparecount.html', {'data': data, 'briefs': _briefs})
    return render_to_response('sparecount.html', {'data': data, 'briefinfos': _briefinfos, 'server_msg': server_msg, 'purview_msg': purview_msg})


def submit_sparecount(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    if _audit:
        _msg = check_purview(request.user.username, 41)
        if _msg != 0:
            return HttpResponseRedirect('/view_sparecount/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 40)
        if _msg != 0:
            return HttpResponseRedirect('/view_sparecount/?msg='+_msg)

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
            return HttpResponseRedirect('/view_sparebill/?msg=库存不足，需补'+str(_spare.minimum-_spare.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_sparebill')
    else:
        if _spare.eligiblestock < _spare.minimum:
            return HttpResponseRedirect('/view_sparecount/?msg=库存不足，需补'+str(_spare.minimum-_spare.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_sparecount')


def delete_sparecount(request):
    #权限判断
    _msg = check_purview(request.user.username, 41)
    if _msg != 0:
        return HttpResponseRedirect('/view_sparecount/?msg='+_msg)

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
    _msg = check_purview(request.user.username, 25)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _tools = k_tool.objects.filter(classid__in=result)

    data = []
    for _tool in _tools:
        dataitem = {}

        _creator = k_user.objects.get(id=_tool.creatorid)
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
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _tool.createdatetime
        dataitem['ownername'] = _tool.ownerid.name

        if _tool.editorid != 0:
            _editor = k_user.objects.get(id=_tool.editorid)
            dataitem['editor'] = _editor.name
            dataitem['editdatetime'] = _tool.editdatetime

        if _tool.auditorid != 0:
            _auditor = k_user.objects.get(id=_tool.auditorid)
            dataitem['auditor'] = _auditor.name
            dataitem['auditdatetime'] = _tool.auditdatetime

        data.append(dataitem)
        #非法权限信息    
    purview_msg = request.GET.get('msg')
    if purview_msg == None:
       purview_msg = ''
    #, 'purview_msg': purview_msg


    return render_to_response('tool.html', {"data": data, 'purview_msg': purview_msg})


def operate_tool(request):
    _id = request.GET.get('id')
    #权限判断
    _msg = check_purview(request.user.username, 26)
    if _msg != 0:
        if _id:
            return HttpResponseRedirect('/view_tool/?msg='+_msg)
        else:
            return HttpResponseRedirect('/?msg='+_msg)

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

    return render_to_response('tooloperate.html', {"data": _data, "producers": _producers, "suppliers": _suppliers, "classes": _classes, 'server_msg': server_msg, 'purview_msg': purview_msg})


def submit_tool(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    if _audit:
        _msg = check_purview(request.user.username, 27)
        if _msg != 0:
            return HttpResponseRedirect('/view_tool/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 26)
        if _msg != 0:
            return HttpResponseRedirect('/view_tool/?msg='+_msg)

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
        _tools = k_tool.objects.filter(name=_name)
        if len(_tools) > 1 or (len(_tools) == 1 and _tools[0].id != int(_id)):
            server_msg = '名称为'+_tools[0].name+'的工具已存在！'
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
        _tools = k_tool.objects.filter(name=_name)
        if len(_tools) > 0:
            server_msg = '名称为'+_tools[0].name+'的工具已存在！'
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
    _msg = check_purview(request.user.username, 27)
    if _msg != 0:
        return HttpResponseRedirect('/view_tool/?msg='+_msg)

    _id = request.GET.get('id')
    if _id:
        _tool = k_tool.objects.get(id=_id)
        _tooluses = k_tooluse.objects.filter(toolid=_tool)
        _toolcounts = k_toolcount.objects.filter(toolid=_tool)
        _tool.delete()
        _tooluses.delete()
        _toolcounts.delete()
    return HttpResponseRedirect('/view_tool')


def view_tooluse(request):
    #权限判断
    _msg = check_purview(request.user.username, 42)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _tooluses = k_tooluse.objects.filter(classid__in=result)

    data = []
    for _tooluse in _tooluses:
        dataitem = {}

        _creator = k_user.objects.get(id=_tooluse.creatorid)
        _tool = k_tool.objects.get(id=_tooluse.toolid_id)
        dataitem['id'] = _tooluse.id
        dataitem['brief'] = _tool.brief
        dataitem['using'] = _tooluse.using
        dataitem['returned'] = _tooluse.returned
        dataitem['depleted'] = _tooluse.depleted
        dataitem['damaged'] = _tooluse.damaged
        dataitem['rejected'] = _tooluse.rejected
        dataitem['user'] = _tooluse.user
        dataitem['memo'] = _tooluse.memo
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _tooluse.createdatetime

        dataitem['notreturned'] = dataitem['using'] - dataitem['returned'] - dataitem['depleted'] - dataitem['damaged'] - dataitem['rejected']

        if _tooluse.editorid != 0:
            _editor = k_user.objects.get(id=_tooluse.editorid)
            dataitem['editor'] = _editor.name
            dataitem['editdatetime'] = _tooluse.editdatetime

        if _tooluse.auditorid != 0:
            _auditor = k_user.objects.get(id=_tooluse.auditorid)
            dataitem['auditor'] = _auditor.name
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


    #return render_to_response('tooluse.html', {'data': data, 'briefs': _briefs})
    return render_to_response('tooluse.html', {'data': data, 'briefinfos': _briefinfos, 'server_msg': server_msg, 'purview_msg': purview_msg})


def submit_tooluse(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    if _audit:
        _msg = check_purview(request.user.username, 44)
        if _msg != 0:
            return HttpResponseRedirect('/view_tooluse/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 43)
        if _msg != 0:
            return HttpResponseRedirect('/view_tooluse/?msg='+_msg)

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
    _msg = check_purview(request.user.username, 44)
    if _msg != 0:
        return HttpResponseRedirect('/view_tooluse/?msg='+_msg)

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
    _msg = check_purview(request.user.username, 42)
    if _msg != 0:
        return HttpResponseRedirect('/?msg='+_msg)

    #分类筛选
    user = k_user.objects.get(username=request.user.username)
    result = [user.classid.id]
    get_class_set(result, user.classid.id)
    _toolcounts = k_toolcount.objects.filter(classid__in=result)

    data = []
    for _toolcount in _toolcounts:
        dataitem = {}

        _creator = k_user.objects.get(id=_toolcount.creatorid)
        _tool = k_tool.objects.get(id=_toolcount.toolid_id)
        dataitem['id'] = _toolcount.id
        dataitem['tooluseid'] = _toolcount.tooluseid
        dataitem['brief'] = _tool.brief
        dataitem['count'] = _toolcount.count
        dataitem['state'] = _toolcount.get_state_display()
        dataitem['iseligible'] = _toolcount.get_iseligible_display()
        dataitem['memo'] = _toolcount.memo
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _toolcount.createdatetime

        if _toolcount.editorid != 0:
            _editor = k_user.objects.get(id=_toolcount.editorid)
            dataitem['editor'] = _editor.name
            dataitem['editdatetime'] = _toolcount.editdatetime

        if _toolcount.auditorid != 0:
            _auditor = k_user.objects.get(id=_toolcount.auditorid)
            dataitem['auditor'] = _auditor.name
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


    #return render_to_response('toolcount.html', {'data': data, 'briefs': _briefs})
    return render_to_response('toolcount.html', {'data': data, 'briefinfos': _briefinfos, 'server_msg': server_msg, 'purview_msg': purview_msg})


def submit_toolcount(request):
    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    #权限判断
    if _audit:
        _msg = check_purview(request.user.username, 44)
        if _msg != 0:
            return HttpResponseRedirect('/view_toolcount/?msg='+_msg)
    else:
        _msg = check_purview(request.user.username, 43)
        if _msg != 0:
            return HttpResponseRedirect('/view_toolcount/?msg='+_msg)

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
            return HttpResponseRedirect('/view_tooluse/?msg=库存不足，需补'+str(_tool.minimum-_tool.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_tooluse')
    else:
        if _tool.eligiblestock < _tool.minimum:
            return HttpResponseRedirect('/view_toolcount/?msg=库存不足，需补'+str(_tool.minimum-_tool.eligiblestock)+'个')
        else:
            return HttpResponseRedirect('/view_toolcount')


def delete_toolcount(request):
    #权限判断
    _msg = check_purview(request.user.username, 44)
    if _msg != 0:
        return HttpResponseRedirect('/view_toolcount/?msg='+_msg)

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
        user = User.objects.get(username=request.user.username)
        classes = k_class.objects.all()
        parents = 0
        datas = get_type_node(classes, parents) #获取节点树
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
                variables=RequestContext(request,{'username':user.username, 'data':datas, 'server_msg':server_msg, 'purview_msg': purview_msg,
                                              'department_info':department_info})
            else:
                variables=RequestContext(request,{'username':user.username, 'data':datas, 'server_msg':server_msg, 'purview_msg': purview_msg})
        else:
            variables=RequestContext(request,{'username':user.username, 'data':datas, 'server_msg':server_msg, 'purview_msg': purview_msg})
        return render_to_response('department.html',variables)
    else:
        return HttpResponseRedirect('/login/')

@login_required
def department_revise(request):
    _id = request.GET.get('id')
    if _id:
        #分类筛选
        user=User.objects.get(username=request.user.username)
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
        datas['isNew'] = True

        _tmp_class = k_class.objects.filter(id=_id)
        if len(_tmp_class) == 1:
            _existed_info = _tmp_class[0]
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

        #非法权限信息
        purview_msg = request.GET.get('msg')
        if purview_msg == None:
           purview_msg = ''
        #, 'purview_msg': purview_msg

        variables=RequestContext(request,{'username':user.username,  'data':datas, 'purview_msg': purview_msg})
        return render_to_response('departmentadd.html',variables)
    else:
        HttpResponseRedirect('/department/?msg="非法访问！"')


@login_required
def departmentadd(request):
    if request.user.is_authenticated():
        #分类筛选
        user=User.objects.get(username=request.user.username)
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

        variables=RequestContext(request,{'username':user.username, 'data':datas, 'purview_msg': purview_msg})
        return render_to_response('departmentadd.html',variables)
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
    _tmp_class = k_class.objects.filter(name = request.GET.get('name'))
    if not _tmp_class:
        if len(_parentname) > 0:
            _parent = k_class.objects.filter(name=_parentname)
            if len(_parent) == 1:
                _id = _parent[0].id
                _depth = _parent[0].depth+1
            else:
                return HttpResponseRedirect('/department/?msg="父级类别有误！"')

            _class = k_class.objects.create(name=_name, parentid=_id,depth=_depth,memo=_memo, code=_code,
                                            license=_license, logo=_logo, address=_address, zipcode=_zipcode,
                                            phone=_phone, licensetype=_licensetype,content=_content,
                                            creatorid = request.user.id, createdatetime=get_current_date(),
                                            editorid=request.user.id, editdatetime=get_current_date())
            _class.save()
            return HttpResponseRedirect('/department/')
    else:
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
        _department = k_class.objects.get(id=_id)
        msg = "成功删除部门："+_department.name
        _department.delete()
        return HttpResponseRedirect('/department/?msg='+msg)
    else:
        return HttpResponseRedirect('/department/')

'''部门设置结束'''


@login_required
def score(request):
    return render_to_response('score.html', {})


@login_required
def egg(request):
    configs = k_config.objects.all()
    config = list(configs[0:1])

    if not config:
        config = k_config.objects.create(eggbonus=0.0, eggprobability=0.0)
    else:
        config = config[0]

    return render_to_response('egg.html', {'data': {'bonus': config.eggbonus, 'probability': config.eggprobability}})


def egg_submit(request):
    bonus = request.POST.get('bonus')
    probability = request.POST.get('probability')

    configs = k_config.objects.all()
    config = list(configs[0:1])

    if not config:
        config = k_config()
    else:
        config = config[0]

    config.eggbonus = bonus
    config.eggprobability = probability
    config.save()

    return HttpResponseRedirect('/egg/?msg=修改成功')


def meter(request):
    if request.method == 'GET':
        return render_to_response('meter.html')


def meter_device(request):
    brief = request.GET.get('brief')

    # try:
    #     k_device.objects.get(brief=brief)
    # except ObjectDoesNotExist:
    #     return HttpResponseRedirect('/meter/')

    meters = k_meter.objects.filter(brief=brief)
    data = [{
        'brief': brief,
        'route': m.routeid.name,
        'user': m.userid.username,
        'time': m.metertime,
        'content': m.json
    } for m in meters]

    return render_to_response('meterview.html', {'meters': data})


def meter_date(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    date_string = year + '-' + month + '-' + day
    _date = datetime.strptime(date_string, '%Y-%m-%d').date()

    meters = k_meter.objects.filter(metertime__range=(_date, _date + timedelta(days=1)))
    data = [{
        'brief': m.brief,
        'route': m.routeid.name,
        'user': m.userid.username,
        'time': m.metertime,
        'content': m.json
    } for m in meters]

    return render_to_response('meterview.html', {'meters': data})


