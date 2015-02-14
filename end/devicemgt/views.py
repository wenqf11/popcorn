__author__ = 'LY'
# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from models import k_user
from forms import *

#首页
def index(request):
    if request.user.is_authenticated():
        #登陆成功
        #读取权限，显示内容
        variables=RequestContext(request,{'test':'hello'})
        return render_to_response('index.html',variables)
    else:
        return HttpResponseRedirect('/login/')

#注册,
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
            user = k_user.objects.filter(username__exact = username,password__exact = password)
            if user:
                return render_to_response('index.html',{'username':username})
            else:
                return HttpResponseRedirect('/login/')
    else:
        return render_to_response('login.html')