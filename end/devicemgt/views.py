__author__ = 'LY'
# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from models import *
from forms import *
from helper import handle_uploaded_file
import json

#首页
def index(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'index'})
        return render_to_response('index.html',variables)
    else:
        return HttpResponseRedirect('/login/')

#用户管理
def usermgt(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user'})
        return render_to_response('user.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def useradd(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        if request.method == 'POST':
            face = handle_uploaded_file(request.POST['username'],request.FILES['face'])
            print face
            #如果错误，要把已经填写的信息给返回回去
            #总共要有26项信息
            user = k_user.objects.create_user(username = request.POST['username'],
                password=request.POST['password'],
                name=request.POST['name'],
                face=face,
                mobile=request.POST['mobile'],
                email=request.POST['email'],
                address=request.POST['address'],
                zipcode=request.POST['zipcode'],
                birthday=request.POST['birthday'],
                idcard=request.POST['idcard'],
                content=request.POST['content'],
                memo=request.POST['memo'],
                contact=request.POST['contact'],
                contactmobile=request.POST['contactmobile']
            )
            #保存
            #user.save()
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        class_list = ['class1', 'class2']
        role_list = ['tmp1', 'tmp2']
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user',
                                          'class_list':class_list, 'role_list':role_list})
        return render_to_response('useradd.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def userdel(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user'})
        return render_to_response('userdel.html',variables)
    else:
        return HttpResponseRedirect('/login/')


def userset(request):
    if request.user.is_authenticated():
        #登陆成功
        #user=k_user.objects.get(username=request.user.username)
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'user'})
        return render_to_response('userset.html',variables)
    else:
        return HttpResponseRedirect('/login/')


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
    print "profile"
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
        user=User.objects.get(username=request.user.username)
        #读取权限，显示内容
        variables=RequestContext(request,{'username':user.username, 'clicked_item': 'front'})
        return render_to_response('front.html',variables)
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
            user = k_user.objects.create(username= username,password=password, classid_id=1, roles=1)
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
    return render_to_response('register.html',{'uf':uf}, context_instance=RequestContext(req))

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
                return render_to_response('index.html',{'username':username})
            else:
                return HttpResponseRedirect('/login/')
    else:
        return render_to_response('login.html')

def form(request):
    if request.method == 'POST':
        response = {
        "data": [
        {
        "table_item": "row_1",
        "unit": "Tiger",
        "lower_shreshold": "Nixon",
        "upper_threshold": "System Architect"
        },
        {
        "table_item": "row_1",
        "unit": "Tiger",
        "lower_shreshold": "Nixon",
        "upper_threshold": "System Architect"
        },
        {
        "table_item": "row_1",
        "unit": "Tiger",
        "lower_shreshold": "Nixon",
        "upper_threshold": "System Architect"
        }
        ],
        "options": []
        };
        response['Access-Control-Allow-Origin'] = '*'
        return HttpResponse(json.dumps(response))
    else:
        response = {
        "data": [
        {
        "table_item": "row_1",
        "unit": "Tiger",
        "lower_shreshold": "Nixon",
        "upper_threshold": "System Architect"
        },
        {
        "table_item": "row_1",
        "unit": "Tiger",
        "lower_shreshold": "Nixon",
        "upper_threshold": "System Architect"
        }
        ],
        "options": []
        };
        response['Access-Control-Allow-Origin'] = '*'
        return HttpResponse(json.dumps(response))

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

def purview(request):
    allpurview = k_purview.objects.all()
    purviewdata = []
    for p in allpurview:
        onepurview = dict()
        theclass = k_class.objects.filter(id = p.classid_id)
        onepurview["class"] = theclass[0].name
        onepurview["name"] = p.name
        onepurview["item"] = p.item
        onepurview["memo"] = p.memo
        thecreator = k_user.objects.filter(id = p.creatorid)
        onepurview["creator"] = thecreator[0].username
        onepurview["createdatetime"] = '2015/4/12'
        theeditor = k_user.objects.filter(id = p.editorid)
        onepurview["editor"] = theeditor[0].username
        onepurview["editdatetime"] = '2015/4/13'
        purviewdata.append(onepurview)
    response = {}
    response["aaData"] = purviewdata
    #response["sInfo"] = ""
    #response["iTotalRecords"] = 11
    #response["iTotalDisplayRecords"] = 11
    response["options"] = []
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(json.dumps(response))

def view_role(request):
    allrole = k_role.objects.all()
    roledata = []
    for p in allrole:
        onerole = dict()
        theclass = k_class.objects.filter(id=p.classid_id)
        onerole["id"] = p.id
        onerole["class"] = theclass[0].name
        onerole["name"] = p.name
        onerole["purviews"] = []
        therolepurviews = p.purviews.all()
        lastname = ""
        nowitem = ""
        for i in range(0,len(therolepurviews)):
            q = therolepurviews[i]
            if q.name == lastname:
                nowitem += ", "+q.item
            elif q.name != lastname:
                if lastname != "":
                    onepurview = dict()
                    onepurview["name"] = lastname
                    onepurview["item"] = nowitem
                    onerole["purviews"].append(onepurview)
                lastname = q.name
                nowitem = q.item
            if i == len(therolepurviews) - 1:
                onepurview = dict()
                onepurview["name"] = lastname
                onepurview["item"] = nowitem
                onerole["purviews"].append(onepurview)
        onerole["memo"] = p.memo
        thecreator = k_user.objects.filter(id=p.creatorid)
        onerole["creator"] = thecreator[0].username
        onerole["createdatetime"] = '2015/4/12'
        theeditor = k_user.objects.filter(id=p.editorid)
        onerole["editor"] = theeditor[0].username
        onerole["editdatetime"] = '2015/4/13'
        roledata.append(onerole)
    return render_to_response('roleview.html',{'data':roledata})

def operate_role(request):
    theid = request.GET.get("id")
    if theid:
        roledata = dict()
        therole = k_role.objects.filter(id=theid)
        therole = therole[0]
        roledata["id"] = therole.id
        roledata["name"] = therole.name
        roledata["purviews"] = []
        therolepurviews = therole.purviews.all()
        for q in therolepurviews:
            roledata["purviews"].append(q.name+", "+q.item)
        roledata["memo"] = therole.memo
        thecreator = k_user.objects.filter(id=therole.creatorid)
        roledata["creator"] = thecreator[0].username
        roledata["createdatetime"] = '2015/4/12'
        theeditor = k_user.objects.filter(id=therole.editorid)
        roledata["editor"] = theeditor[0].username
        roledata["editdatetime"] = '2015/4/13'
        return render_to_response('roleoperate.html', {'isNew':False, 'data':roledata})
    else:
        return render_to_response('roleoperate.html', {'isNew':True})

def delete_role(request):
    #delete to db
    return render_to_response('roledelete.html', {'isNew':True})