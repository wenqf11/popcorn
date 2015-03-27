__author__ = 'LY'
# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from models import k_user
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
            user = k_user.objects.create(username= username,password=password, classid_id=1, permission_id = 1)
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
    #if request.method != 'POST':
    response = {
    "data": [
    {
    "classid": "2",
    "name": "无油螺杆空气压缩机",
    "brief": "SZ012012GC120",
    "brand": "unknown",
    "producer": "日本KOBELCO",
    "supplier": "盛世神钢压缩机（北京）有限公司",
    "typeid": "6",
    "state": "锁定",
    "serial": "6216610100000000000",
    "model": "大型设备",
    "buytime": "2015/03/21",
    "content": "unknown",
    "memo": "unknown"
    }
    ],
    "options": []
    };
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(json.dumps(response))
