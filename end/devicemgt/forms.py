__author__ = 'LY'
# -*- coding: utf-8 -*-

from django import forms

#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
