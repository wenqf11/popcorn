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
from datetime import datetime
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

def get_node(child_list):
    result = list()
    for c in child_list:
        userdata = dict()
        userdata["text"] = c.name.encode('utf8')
        sub_child_list = k_class.objects.filter(parentid = c.id)
        if sub_child_list:
            userdata["node"] = get_node(sub_child_list)
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

        if current_class:
            userdatas = list()

            class_set = k_class.objects.filter(parentid = current_class_id)
            for c in class_set:
                userdata = dict()
                userdata["text"] = c.name.encode('utf8')
                child_list = k_class.objects.filter(parentid = c.id)
                if child_list:
                    userdata["nodes"] = get_node(child_list)
                userdatas.append(userdata)

            cur_datas = dict()
            datas = list()
            cur_datas["text"] = current_class.name.encode('utf8')
            cur_datas['nodes'] = userdatas
            datas.append(cur_datas)

            '''
        userdatas1 = list()
        userdata = dict()
        userdata["text"] = "Parent 2"
        userdata["href"] = "./?id=1"
        userdatas1.append(userdata)
        userdata = dict()
        userdata["text"] = "Parent 4"
        userdata["href"] = "#parent4"
        userdatas1.append(userdata)
        userdata1 = dict()
        tmp = list()
        tmp.append(userdata)
        userdata1["text"] = "Parent 3"
        userdata1["nodes"] = tmp
        userdata1["href"] = "#"
        userdatas1.append(userdata1)
        '''

        #userdata = json.dumps(userdata)
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user', 'data': datas})
        return render_to_response('user.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def user_operate(request):
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
            userdata['username'] = theuser.username
            userdata['name'] = theuser.name
            userdata['face'] = theuser.face
            userdata['mobile'] = theuser.mobile
            userdata['email'] = theuser.email
            userdata['address'] = theuser.address
            userdata['zipcode'] = theuser.zipcode
            userdata['birthday'] = theuser.birthday
            userdata['idcard'] = theuser.idcard
            userdata['idcardtype'] = theuser.idcardtype
            userdata['contactmobile'] = theuser.contactmobile
            userdata['content'] = theuser.content
            userdata['memo'] = theuser.memo
        else:
            userdata['isNew'] = True
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
            #print face
            #如果错误，要把已经填写的信息给返回回去
            #排除用户名相同的情况
            #总共要有26项信息
            classid = k_class.objects.filter(id=1)[0]
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
            user.roles.add(1)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        class_list = ['class1', 'class2']
        role_list = ['tmp1', 'tmp2']
        variables=RequestContext(request, {'username': user.username, 'clicked_item': 'user',
                                          'class_list': class_list, 'role_list': role_list})
        return HttpResponseRedirect('/user_operate/')
    else:
        return HttpResponseRedirect('/login/')


def userdel(request):
    if request.user.is_authenticated():
        #登陆成功
        #user = k_user.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables = RequestContext(request, {'username': user.username, 'clicked_item': 'user'})
        return render_to_response('userdel.html', variables)
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

#设备管理
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


def deviceadd(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'device'})
        return render_to_response('deviceadd.html',variables)
    else:
        return HttpResponseRedirect('/login/')


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


def front(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user = User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables = RequestContext(request, {'username': user.username, 'clicked_item': 'front'})
        return render_to_response('front.html', variables)
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


def unmain(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'maintenance'})
        return render_to_response('unmain.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def mainhist(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'maintenance'})
        return render_to_response('mainhist.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def spare(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'stock'})
        return render_to_response('spare.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def sparetype(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'stock'})
        return render_to_response('sparetype.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def sparebrand(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'stock'})
        return render_to_response('sparebrand.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def sparehist(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'stock'})
        return render_to_response('sparehist.html',variables)
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
def delete_form(request):
    _id = request.GET.get('id')
    _brief = request.GET.get('brief')
    if _id:
        _formitem = k_formitem.objects.get(id=_id)
        _formitem.delete()
    return HttpResponseRedirect('/view_form/?brief='+_brief)


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