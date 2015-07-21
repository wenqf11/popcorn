# -*- coding: utf-8 -*-
__author__ = 'LY'


from django import forms

#定义表单模型

#用户表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
