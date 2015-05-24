#-*- encoding=UTF-8 -*-
__author__ = 'LY'


from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from models import *
from forms import *
from datetime import datetime, timedelta
from helper import handle_uploaded_file, get_current_time, get_current_date
import json


#首页
def index(request):
    if request.user.is_authenticated():
        #登陆成功
        #user = k_user.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables = RequestContext(request, {'username': user.username, 'clicked_item': 'index'})
        return render_to_response('index.html', variables)
    else:
        return HttpResponseRedirect('/login/')


'''用户管理开始
'''

def get_leaf(leaf_list):
    result = list()
    for leaf in leaf_list:
        userdata = dict()
        userdata["text"] = leaf.username.encode('utf8')
        userdata["href"] = "/user?id=" + str(leaf.id)
        result.append(userdata)
    return result

def get_node(child_leaf_list, child_node_list):
    result = list()
    for leaf in child_leaf_list:
        userdata = dict()
        userdata["text"] = leaf.username.encode('utf8')
        userdata["href"] = "/user?id=" + str(leaf.id)
        result.append(userdata)
    for c in child_node_list:
        userdata = dict()
        userdata["text"] = c.name.encode('utf8')
        sub_child_list = k_class.objects.filter(parentid = c.id)
        sub_leaf_list = k_user.objects.filter(classid_id=c.id)
        if sub_child_list:
            userdata["nodes"] = get_node(sub_leaf_list, sub_child_list)
        elif sub_leaf_list:
            userdata["nodes"] = get_leaf(sub_leaf_list)
        result.append(userdata)
    return result


def usermgt(request):
    if request.user.is_authenticated():
        #登陆成功
        user = k_user.objects.get(username=request.user.username)
        #user = User.objects.get(username=request.user.username)
        #读取权限，显示内容
        current_class_id = user.classid_id
        current_class = k_class.objects.get(id=current_class_id)
        server_msg = request.GET.get('msg')
        if server_msg == None:
           server_msg = ''
        else:
            server_msg = ''
        if current_class:
            userdatas = list()
            class_set = k_class.objects.filter(parentid = current_class_id)
            leaf_list = k_user.objects.filter(classid_id=current_class_id)
            for leaf in leaf_list:
                userdata = dict()
                userdata["text"] = leaf.username.encode('utf8')
                userdata["href"] = "/user?id=" + str(leaf.id)
                userdatas.append(userdata)
            for c in class_set:
                userdata = dict()
                userdata["text"] = c.name.encode('utf8')
                child_list = k_class.objects.filter(parentid = c.id)
                leaf_list = k_user.objects.filter(classid_id=c.id)
                if child_list:
                    userdata["nodes"] = get_node(leaf_list, child_list)
                #elif leaf_list:
                #    userdata["nodes"] = get_leaf(leaf_list)
                userdatas.append(userdata)

            cur_datas = dict()
            datas = list()
            cur_datas["text"] = current_class.name.encode('utf8')
            cur_datas['nodes'] = userdatas
            datas.append(cur_datas)

        #userdata = json.dumps(userdata)
        _id = request.GET.get('id')
        # 如果访问某个用户的信息
        if (_id):
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
            variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user', 'data': datas, 'userinfo':user_info,
                                              'user_role':user_role, 'user_class': user_class, 'server_msg':server_msg})
        else:
            variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user', 'data': datas, 'server_msg':server_msg})
        return render_to_response('user.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def operate_user(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        _id = request.GET.get('id')
        userdata = dict()
        class_list = list()
        classes = k_class.objects.all()
        for c in classes:
            class_list.append(c.name)
        role_list = list()
        roles = k_role.objects.all()
        for role in roles:
            role_list.append(role.name)

        userdata['class_list'] = class_list
        userdata['role_list'] = role_list
        if _id:
            theuser = k_user.objects.filter(id = _id)[0]
            key_list = ['username', 'password', 'name', 'face', 'mobile', 'email', 'address', 'zipcode', 'birthday',
                        'idcard', 'idcardtype','contactmobile', 'content', 'memo','birthday']
            for key in key_list:
                userdata[key] = eval('theuser.'+key)

            k_chosed_roles = k_role.objects.filter(k_user=_id)
            chosed_roles = []
            for k_chosed_role in k_chosed_roles:
                chosed_roles.append(k_chosed_role.name)
            userdata['chosen_roles'] = chosed_roles
        else:
            userdata['isNew'] = True

        server_msg = request.GET.get('msg')
        if server_msg:
            variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user', 'data': userdata,'server_msg':server_msg})
        else:
            variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user', 'data': userdata})
        return render_to_response('useradd.html',variables)
    else:
        return HttpResponseRedirect('/login/')

# 提交表单，添加用户
def useradd(request):
    if request.user.is_authenticated():
        #登陆成功
        #user = k_user.objects.get(username=request.user.username)
        if request.method == 'POST':
            #face = handle_uploaded_file(request.POST['username'],request.FILES['face'])
            face = "../static/images/user.png"
            #如果用户名相同，修改已有的用户
            server_msg = ''
            cur_user_id = 0
            user = k_user.objects.filter(username=request.POST['username'])
            if not user:
                #总共要有26项信息
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
                    gender =request.POST['gender'],
                    #birthday=request.POST['birthday'],
                    birthday="1993-05-28",
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
                cur_user_id = user.id
                #给roles和user也增加一条记录
                olduser = User.objects.create_user(
                    username=user.username,
                    email=user.email,
                    password=user.password
                )
                #保存
                user.save()
                olduser.save()
                #建立user和role的关系
                roles = k_role.objects.filter(name=request.POST['role'])
                for role in roles:
                    user.roles.add(role.id)
                server_msg = '添加用户成功！'
            elif len(user) == 1:
                user = user[0]
                cur_user_id = user.id
                user.password = request.POST['password']
                user.email = request.POST['email']
                user.name = request.POST['name']
                user.mobile = request.POST['mobile']
                user.gender = request.POST['gender']
                user.zipcode = request.POST['zipcode']
                user.address = request.POST['address']
                #user.birthday = request.POST['birthday']
                user.idcard = request.POST['idcard']
                user.idcardtype = request.POST['idcardtype']
                user.content = request.POST['content']
                user.memo = request.POST['memo']
                user.editorid = request.user.id
                user.editdatetime = get_current_date()
                tmp_urs = user.roles.filter(k_user = user.id)
                for ur in tmp_urs:
                    user.roles.remove(ur)
                #建立user和role的关系
                roles_name = request.POST.getlist('role')
                for r_name in roles_name:
                    roles = k_role.objects.filter(name=r_name)
                    for role in roles:
                        user.roles.add(role.id)
                user.editorid = request.user.id
                user.editdatetime=get_current_date()
                user.save()
                server_msg = '修改用户资料成功！'
                # 更新用户成功
            else:
                server_msg = "Error: user with the same username!"
        return HttpResponseRedirect('/user_operate/?id='+str(cur_user_id)+'&msg='+server_msg)
    else:
        return HttpResponseRedirect('/login/')


def userdel(request):
    if request.user.is_authenticated():
        _id = request.GET.get('id')
        if int(_id) == request.user.id:
            return HttpResponseRedirect('/user/?msg="不能删除用户本身"')
        if _id:
            users = k_user.objects.get(id=_id)
            users.delete()
        return HttpResponseRedirect('/user/')
    else:
        return HttpResponseRedirect('/login/')


def userset(request):
    if request.user.is_authenticated():
        #登陆成功
        #user = k_user.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables = RequestContext(request,{'username': user.username, 'clicked_item': 'user'})
        return render_to_response('userset.html', variables)
    else:
        return HttpResponseRedirect('/login/')

'''用户管理结束
'''

'''设备管理'''
def devicemgt(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device'})
        return render_to_response('device.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def operate_device(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        _id = request.GET.get('id')
        userdata = dict()
        class_list = list()
        classes = k_class.objects.all()
        for c in classes:
            class_list.append(c.name)

        userdata['class_list'] = class_list
        if _id:
            theuser = k_user.objects.filter(id = _id)[0]
            key_list = ['username', 'password', 'name', 'face', 'mobile', 'email', 'address', 'zipcode', 'birthday',
                        'idcard', 'idcardtype','contactmobile', 'content', 'memo','birthday']
            for key in key_list:
                userdata[key] = eval('theuser.'+key)
        else:
            userdata['isNew'] = True
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user', 'data': userdata})
        return render_to_response('deviceadd.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def deviceadd(request):
    if request.user.is_authenticated():
        user=User.objects.get(username=request.user.username)
        #返回class的信息
        #返回type的信息
        #生产厂商
        #供应商
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device'})
        return render_to_response('deviceadd.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def get_type_node(devicetypes, parent):
    datas = list()
    for type in devicetypes:
        if type.parentid == parent:
            cur_data = dict()
            cur_data['text'] = type.name
            tmp = get_type_node(devicetypes, type.name)
            if len(tmp) > 0:
                cur_data['nodes'] = tmp
            datas.append(cur_data)

    return datas

def device_type(request):
    if request.user.is_authenticated():
        user=User.objects.get(username=request.user.username)
        devicetypes = k_devicetype.objects.all()
        parents = 0
        datas = get_type_node(devicetypes, parents)

        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device', 'data':datas})
        return render_to_response('devicetype.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def device_type_add(request):
    if request.user.is_authenticated():
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        k_devicetypes = k_devicetype.objects.all()
        devicetypes = list()
        for k_type in k_devicetypes:
            devicetypes.append(k_type.name)
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device', 'devicetypes':devicetypes})
        return render_to_response('devicetypeadd.html',variables)
    else:
        return HttpResponseRedirect('/login/')

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

def add_supplier(request):
    if request.user.is_authenticated():
        user=User.objects.get(username=request.user.username)
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device'})
        return render_to_response('supplieradd.html',variables)
    else:
        return HttpResponseRedirect('/login/')


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
            return HttpResponseRedirect('/supplier/?msg="error1"')
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

def add_producer(request):
    if request.user.is_authenticated():
        user=User.objects.get(username=request.user.username)
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device'})
        return render_to_response('produceradd.html',variables)
    else:
        return HttpResponseRedirect('/login/')

@login_required
def submit_producer(request):
    if request.method == 'POST':
        #修改供应商
        _producer = k_producer.objects.filter(name = request.POST.get('name'))
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
#个人信息
def profile(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username})
        return render_to_response('profile.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def setting(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'setting'})
        return render_to_response('setting.html',variables)
    else:
        return HttpResponseRedirect('/login/')


#注册, 创建一个新用户
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


#处理登录请求
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            #user = k_user.objects.filter(username = username,password = password)
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return render_to_response('index.html', {'username': username})
            else:
                return HttpResponseRedirect('/login/')
    else:
        return render_to_response('login.html')


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
def save_schedule(request):
    error = []
    if request.method == 'POST':
        shifts = eval(request.POST["shifts"])
        try:
            k_schedule.objects.all().delete()
            for shift in shifts:
                for user in shift['users']:
                    u = k_user.objects.get(id=user)
                    route = k_route.objects.get(id=shift['route'])
                    c = k_class.objects.get(id=1)
                    s = k_schedule(route=route, user=u, date=shift['time'], classid=c)
                    s.save()
        except Exception, e:
            print e
    else:
        error.append("no data")
    return HttpResponse(json.dumps(error))


def get_schedule(request):
    routes = k_route.objects.all()
    route_data = [{'id': _r.id, 'name': _r.name, 'startTime': str(_r.starttime), 'period': _r.period} for _r in routes]
    available_shifts = k_schedule.objects.all()
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


def schedule(request):
    users = k_user.objects.all()
    user_data = [{'id':  user.id, 'name': user.name} for user in users]
    routes = k_route.objects.all()
    route_data = []
    for r in routes:
        route = {
            'id': r.id,
            'name': r.name,
            'startTime': r.starttime,
            'period': r.period
        }
        route_data.append(route)

    available_shifts = k_schedule.objects.filter(date__range=[date.today() - timedelta(days=10), date.today()])
    existed_dates = [_d['date'] for _d in available_shifts.values('date').distinct()]
    existed_routes = [_d['route'] for _d in available_shifts.values('route').distinct()]

    shift_data = {}
    for day in existed_dates:
        day_shifts = {}
        available_day_shifts = available_shifts.filter(date=day)
        for r in existed_routes:
            available_day_route_shifts = available_day_shifts.filter(route=r)
            if available_day_route_shifts.exists():
                day_shifts[str(r)] = [_d['user'] for _d in available_day_route_shifts.values('user').distinct()]
        shift_data[str(day)] = day_shifts

    return render_to_response('schedule.html', {'routes': route_data, 'shifts': shift_data, 'users': user_data})


@login_required
def view_role(request):
    user = k_user.objects.get(username=request.user.username)
    allrole = k_role.objects.all()
    roledata = []
    for p in allrole:
        onerole = {}
        theclass = k_class.objects.get(id=p.classid_id)
        onerole["id"] = p.id
        onerole["class"] = theclass.name
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

        all_purview = k_purview.objects.all()
        roledata["purviews"] = []
        for _purview in all_purview:
            roledata['purviews'].append({
                'id': _purview.id,
                'name': _purview.name + ', ' + _purview.item,
                'selected': _purview.id in purview_ids
            })
        return render_to_response('roleoperate.html', {'username':user.username,'isNew': False, 'data': roledata})
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

        return render_to_response('roleoperate.html', {'username':user.username,'isNew': True, 'data': data})


@login_required
def delete_role(request):
    _id = request.GET.get('id')
    if _id:
        _role = k_role.objects.get(id=_id)
        _role.delete()
    return HttpResponseRedirect('/view_role/')


@login_required
def submit_role(request, _id):
    _name = request.GET.get('name')
    _editdatetime = get_current_date()
    # 编辑者
    _user = k_user.objects.get(username=request.user.username)
    _editor = _user.id
    _purviews = request.GET.getlist('duallistbox')
    _memo = request.GET.get('memo')

    if _id:
        _role = k_role.objects.get(id=_id)
    else:
        _role = k_role.objects.create(classid=_user.classid)
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
        route['forms'] = ', '.join('form' + _form_id for _form_id in r.formid.split(','))
        route['name'] = r.name
        route['startTime'] = r.starttime
        route['period'] = r.period
        route['creator'] = k_user.objects.get(id=r.creatorid).username
        route['createTime'] = r.createdatetime
        route['editor'] = k_user.objects.get(id=r.editorid).username
        route['editTime'] = r.editdatetime
        route['auditor'] = k_user.objects.get(id=r.auditorid).username
        route['auditTime'] = r.auditdatetime
        route['status'] = r.status
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
        data['forms'] = []
        for _form in all_form:
            data['forms'].append({
                'id': _form.id,
                'brief': _form.brief,
                'selected': str(_form.id) in _forms
            })

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
def submit_route(request, _id):
    _user = k_user.objects.get(username=request.user.username)
    _editor = _user.id
    _forms = request.GET.getlist('duallistbox')
    _name = request.GET.get('name')
    _period = request.GET.get('period')
    _start_time = request.GET.get('startTime')
    _edit_time = get_current_date()
    if _id:
        route = k_route.objects.get(id=_id)
    else:
        route = k_route.objects.create(
            classid=_user.classid,
            starttime=datetime.strptime('08:00', '%H:%M').time(),
            period=0,
            # audition not discussed
            auditorid=1
        )
        route.creatorid = _editor
    route.name = _name
    route.formid = ','.join(_forms)
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
    _brief = request.GET.get('brief')
    _form = k_form.objects.get(brief=_brief)
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
        _formitem = k_formitem.objects.create(classid=_user.classid, formid_id=_formid)
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
def view_maintaining(request):
    _maintainings = k_maintenance.objects.filter(mtype=2, state__lte=3)
    data = []
    for _maintaining in _maintainings:
        _device = _maintaining.deviceid
        _creator = k_user.objects.get(id=_maintaining.creatorid)
        if _maintaining.assignorid == 0:
            data.append({
                'id': _maintaining.id,
                'title': _maintaining.title,
                'brief': _device.brief,
                'name': _device.name,
                'position': _device.position,
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
                'brief': _device.brief,
                'name': _device.name,
                'position': _device.position,
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
    _users = k_user.objects.all()
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    return render_to_response('maintainingview.html', {'data': data, 'maintainers': _maintainers})


@login_required
def view_maintained(request):
    _maintaineds = k_maintenance.objects.filter(mtype=2, state__gte=4)
    data = []
    for _maintained in _maintaineds:
        _device = _maintained.deviceid
        _creator = k_user.objects.get(id=_maintained.creatorid)
        _assignor = k_user.objects.get(id=_maintained.assignorid)
        _editor = k_user.objects.get(id=_maintained.editorid)
        if _maintained.auditorid == 0:
            data.append({
                'id': _maintained.id,
                'title': _maintained.title,
                'brief': _device.brief,
                'name': _device.name,
                'position': _device.position,
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
                'brief': _device.brief,
                'name': _device.name,
                'position': _device.position,
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
    return render_to_response('maintainedview.html', {'data': data})


@login_required
def add_maintenance(request):
    _users = k_user.objects.all()
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    _devices = k_device.objects.all()
    _briefs = []
    for _device in _devices:
        _briefs.append(_device.brief)
    return render_to_response('maintenanceadd.html', {'maintainers': _maintainers, 'briefs': _briefs})


@login_required
def submit_maintenance(request):
    _title = request.GET.get('title')
    _brief = request.GET.get('brief')
    _editor = request.GET.get('editor')
    _createcontent = request.GET.get('createcontent')
    _priority = request.GET.get('priority')
    _memo = request.GET.get('memo')

    _id = request.GET.get('id')

    _factor = request.GET.get('factor')

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
        _maintainer = k_user.objects.get(name=_editor)
        _maintenance.title = _title
        _maintenance.createcontent = _createcontent
        _maintenance.priority = _priority
        _maintenance.memo = _memo
        _maintenance.assignorid = _user.id
        _maintenance.assigndatetime = get_current_date()
        _maintenance.editorid = _maintainer.id
        _maintenance.state = 2
    else:
        _device = k_device.objects.filter(brief=_brief)

        _maintenance = k_maintenance.objects.create(
            title=_title,
            deviceid=_device[0],
            createcontent=_createcontent,
            priority=_priority,
            memo=_memo,
            creatorid=_user.id,
            createdatetime=get_current_date(),
            state=1,
            mtype=2
        )
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
    _id = request.GET.get('id')
    _type = request.GET.get('type')
    if _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.delete()
    if _type == 1:
        return HttpResponseRedirect('/view_maintained/')
    else:
        return HttpResponseRedirect('/view_maintaining/')


@login_required
def view_upkeeping(request):
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
    _users = k_user.objects.all()
    _maintainers = []
    for _user in _users:
        _maintainers.append(_user.name)
    return render_to_response('upkeepingview.html', {'data': data, 'maintainers': _maintainers})

@login_required
def view_upkeeped(request):
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
    return render_to_response('upkeepedview.html', {'data': data})


@login_required
def submit_upkeep(request):
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
    _id = request.GET.get('id')
    if _id:
        _maintenance = k_maintenance.objects.get(id=_id)
        _maintenance.delete()
    return HttpResponseRedirect('/view_upkeeped/')


@login_required
def view_tasking(request):
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
    return render_to_response('taskingview.html', {'data': data})


@login_required
def view_tasked(request):
    _maintaineds = k_task.objects.filter(state__gte=3)
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
    return render_to_response('taskedview.html', {'data': data})


@login_required
def add_task(request):
    return render_to_response('taskadd.html')


@login_required
def submit_task(request):
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
    if _id:
        _maintenance = k_task.objects.get(id=_id)
        _maintenance.delete()
    if _type == "1":
        return HttpResponseRedirect('/view_tasked/')
    else:
        return HttpResponseRedirect('/view_tasking/')


@login_required
def view_taskitem(request):
    _id = request.GET.get('id')
    _task = k_task.objects.get(id=_id)
    _taskitems = k_taskitem.objects.filter(taskid_id=_task.id)
    data = []
    for _taskitem in _taskitems:
        dataitem = {}

        _creator = k_user.objects.get(id=_taskitem.creatorid)
        _editor = k_user.objects.get(id=_taskitem.editorid)
        dataitem['id'] = _taskitem.id
        dataitem['title'] = _taskitem.title
        dataitem['createcontent'] = _taskitem.createcontent
        dataitem['creator'] = _creator.name
        dataitem['createdatetime'] = _taskitem.createdatetime
        dataitem['priority'] = _taskitem.get_priority_display()
        dataitem['memo'] = _taskitem.memo
        dataitem['editor'] = _editor.name
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

    _taskers = []
    _users = k_user.objects.all()
    for _user in _users:
        _taskers.append(_user.name)
    return render_to_response('taskitemview.html', {'title': _task.title, 'taskers': _taskers, 'taskid': _task.id, 'data': data})


@login_required
def submit_taskitem(request):
    _title = request.GET.get('title')
    _createcontent = request.GET.get('createcontent')
    _priority = request.GET.get('priority')
    _memo = request.GET.get('memo')
    _editor = request.GET.get('editor')

    _factor = request.GET.get('factor')

    _id = request.GET.get('id')
    _taskid = request.GET.get('taskid')
    _user = k_user.objects.get(username=request.user.username)

    _submittype = request.GET.get('submittype')

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

    _taskitem.save()
    return HttpResponseRedirect('/view_taskitem?id='+_taskid)


@login_required
def delete_taskitem(request):
    _id = request.GET.get('id')
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
    _spares = k_spare.objects.all()
    data = []
    for _spare in _spares:
        dataitem = {}

        _creator = k_user.objects.get(id=_spare.creatorid)
        dataitem['id'] = _spare.id
        dataitem['brand'] = _spare.brand
        dataitem['producer'] = _spare.producerid.name
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

    return render_to_response('spare.html', {"data": data})

def operate_spare(request):
    _id = request.GET.get('id')
    _data = {}
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _data["id"] = _id
        _data["isNew"] = False
        _data["brand"] = _spare.brand
        _data["producer"] = _spare.producerid.name
        _data["supplier"] = _spare.supplierid.name
        _data["name"] = _spare.name
        _data["brief"] = _spare.brief
        _data["model"] = _spare.model
        _data["minimum"] = _spare.minimum
        _data["content"] = _spare.content
        _data["memo"] = _spare.memo
    else:
        _data["isNew"] = True
    _producers = []
    _allproducers = k_producer.objects.all()
    for _producer in _allproducers:
        _producers.append(_producer.name)
    _suppliers = []
    _allsuppliers = k_supplier.objects.all()
    for _supplier in _allsuppliers:
        _suppliers.append(_supplier.name)
    return render_to_response('spareoperate.html', {"data": _data, "producers": _producers, "suppliers": _suppliers})

def submit_spare(request):
    _brand = request.GET.get('brand')
    _producer = request.GET.get('producer')
    _supplier = request.GET.get('supplier')
    _name = request.GET.get('name')
    _brief = request.GET.get('brief')
    _model = request.GET.get('model')
    _minimum = request.GET.get('minimum')
    _content = request.GET.get('content')
    _memo = request.GET.get('memo')

    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
    _user = k_user.objects.get(username=request.user.username)
    if _audit:
        _spare = k_spare.objects.get(id=_id)
        _spare.auditorid = _user.id
        _spare.auditdatetime = get_current_date()
        _spare.save()
        return HttpResponseRedirect('/view_spare')
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _spare.editorid = _user.id
        _spare.editdatetime = get_current_date()
        _spare.auditorid = 0
        _producer = k_producer.objects.get(name=_producer)
        _supplier = k_supplier.objects.get(name=_supplier)
        _spare.producerid = _producer
        _spare.supplierid = _supplier
    else:
        _producer = k_producer.objects.get(name=_producer)
        _supplier = k_supplier.objects.get(name=_supplier)
        _spare = k_spare.objects.create(classid=_user.classid, producerid=_producer, supplierid=_supplier)
        _spare.creatorid = _user.id
        _spare.createdatetime = get_current_date()
    _spare.brand = _brand
    _spare.name = _name
    _spare.brief = _brief
    _spare.model = _model
    _spare.minimum = int(_minimum)
    _spare.content = _content
    _spare.memo = _memo
    _spare.save()

    return HttpResponseRedirect('/view_spare')

def delete_spare(request):
    _id = request.GET.get('id')
    if _id:
        _spare = k_spare.objects.get(id=_id)
        _sparebills = k_sparebill.objects.filter(spareid=_spare)
        _sparecounts = k_sparecount.objects.filter(spareid=_spare)
        _spare.delete()
        _sparebills.delete()
        _sparecounts.delete()
    return HttpResponseRedirect('/view_spare')

def view_sparebill(request):
    _sparebills = k_sparebill.objects.all()
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

    return render_to_response('sparebill.html', {'data': data})

def submit_sparebill(request):
    _using = request.GET.get('using')
    _returned = request.GET.get('returned')
    _depleted = request.GET.get('depleted')
    _damaged = request.GET.get('damaged')
    _rejected = request.GET.get('rejected')
    _memo = request.GET.get('memo')
    _name = request.GET.get('user')

    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
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

    if _sparebill.using != int(_using):
        _sparecount = k_sparecount.objects.get(sparebillid=_id, state="5")
        _sparecount.count = -int(_using)
        _sparecount.editorid = _user.id
        _sparecount.editdatetime = get_current_date()
        _sparecount.auditorid = 0
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.eligiblestock = _spare.eligiblestock + _sparebill.using - int(_using)
        _spare.save()
        _sparecount.save()

    if _sparebill.returned != int(_returned):
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.eligiblestock = _spare.eligiblestock - _sparebill.returned + int(_returned)
        _sparecount = k_sparecount.objects.create(classid=_user.classid, sparebillid=_id, spareid=_spare)
        _sparecount.count = int(_returned) - _sparebill.returned
        _sparecount.state = "2"
        _sparecount.iseligible = "1"
        _sparecount.memo = _sparebill.memo
        _sparecount.creatorid = _user.id
        _sparecount.createdatetime = get_current_date()
        _spare.save()
        _sparecount.save()

    if _sparebill.rejected != int(_rejected):
        _spare = k_spare.objects.get(id=_sparebill.spareid_id)
        _spare.ineligiblestock = _spare.ineligiblestock - _sparebill.rejected + int(_rejected)
        _sparecount = k_sparecount.objects.create(classid=_user.classid, sparebillid=_id, spareid=_spare)
        _sparecount.count = int(_rejected) - _sparebill.rejected
        _sparecount.state = "2"
        _sparecount.iseligible = "2"
        _sparecount.memo = _sparebill.memo
        _sparecount.creatorid = _user.id
        _sparecount.createdatetime = get_current_date()
        _spare.save()
        _sparecount.save()

    _sparebill.using = int(_using)
    _sparebill.returned = int(_returned)
    _sparebill.depleted = int(_depleted)
    _sparebill.damaged = int(_damaged)
    _sparebill.rejected = int(_rejected)
    _sparebill.user = _name
    _sparebill.memo = _memo

    _sparebill.save()
    return HttpResponseRedirect('/view_sparebill')

def delete_sparebill(request):
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
    _sparecounts = k_sparecount.objects.all()
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

    _spares = k_spare.objects.all()
    _briefs = []
    for _spare in _spares:
        _briefs.append(_spare.brief)

    return render_to_response('sparecount.html', {'data': data, 'briefs': _briefs})

def submit_sparecount(request):
    _brief = request.GET.get('brief')
    _state = request.GET.get('state')
    _iseligible = request.GET.get('iseligible')
    _count = request.GET.get('count')
    _memo = request.GET.get('memo')
    _name = request.GET.get('user')

    _id = request.GET.get('id')
    _audit = request.GET.get('audit')
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
            _sparebill.using = -int(_count)
            _sparebill.user = _name
            _sparebill.memo = _memo
            _sparebill.creatorid = _user.id
            _sparebill.createdatetime = get_current_date()
            _sparecount.sparebillid = _sparebill.id

    _spare = k_spare.objects.get(id=_sparecount.spareid_id)
    if _iseligible == _sparecount.iseligible:
        if _iseligible == "1":
            _spare.eligiblestock = _spare.eligiblestock - _sparecount.count + int(_count)
        else:
            _spare.ineligiblestock = _spare.ineligiblestock - _sparecount.count + int(_count)
    else:
        if _iseligible == "1":
            _spare.ineligiblestock = _spare.ineligiblestock - _sparecount.count
            _spare.eligiblestock = _spare.eligiblestock + int(_count)
        else:
            _spare.eligiblestock = _spare.eligiblestock - _sparecount.count
            _spare.ineligiblestock = _spare.ineligiblestock + int(_count)

    _spare.save()

    _sparecount.state = _state
    _sparecount.iseligible = _iseligible
    _sparecount.count = int(_count)
    _sparecount.memo = _memo

    _sparecount.save()
    
    _sparebill.save()
    return HttpResponseRedirect('/view_sparecount')

def delete_sparecount(request):
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


def view_tool(request):
    return render_to_response('tool.html', {})

def operate_tool(request):
    return render_to_response('tooloperate.html', {})

def submit_tool(request):
    return render_to_response('tool.html', {})

def delete_tool(request):
    return render_to_response('tool.html', {})

def view_tooluse(request):
    return render_to_response('tooluse.html', {})

def submit_tooluse(request):
    return render_to_response('tooluse.html', {})

def delete_tooluse(request):
    return render_to_response('tooluse.html', {})

def view_toolcount(request):
    return render_to_response('toolcount.html', {})

def submit_toolcount(request):
    return render_to_response('toolcount.html', {})

def delete_toolcount(request):
    return render_to_response('toolcount.html', {})


@login_required
def department(request):
    return render_to_response('department.html', {})


@login_required
def score(request):
    return render_to_response('score.html', {})
