__author__ = 'LY'
# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)

# Create your models here.
class UserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def create_user(self, StudentNumber, username,department, Graduation_Date, phone_num, IsEmail, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, department=department, email=email,
            StudentNumber=StudentNumber, Graduation_Date=Graduation_Date, phone_num=phone_num, IsEmail = IsEmail)
        user.set_password(password)
        return user

    def create_superuser(self, username, email, password):
        u = self.create_user(username, email, password)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(username=username)

# status: 0删除，1有效，2审核未通过，3审核通过
STATUS_CHOICES =  (
        ('0', '删除'),
        ('1', '有效'),
        ('2', '审核未通过'),
        ('3', '审核通过'),
        )

class k_class(models.Model):
    parentid = models.PositiveIntegerField()
    depth = models.PositiveIntegerField()
    depthname = models.CharField(max_length=50)
    depthnumber = models.PositiveIntegerField()
    purview = models.PositiveIntegerField()
    role = models.PositiveIntegerField()
    name = models.CharField(max_length=30)

class k_role(models.Model):
    classid = models.ForeignKey(k_class, related_name='role_set')
    name = models.CharField(max_length=30)
    item = models.CharField(max_length=30) # ???
    memo = models.CharField(max_length=300)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_user(models.Model):
    USER_STATUS = (
        ('0', '锁定'),
        ('1', '在岗'),
        ('2', '长假'),
        ('3', '离职'),
    )
    CARD_TYPE = (
        ('1','身份证'),
    )
    classid = models.ForeignKey(k_class, related_name='user_set')
    permission = models.ForeignKey(k_role, related_name='user_set')
    state = models.CharField(max_length=1, choices=USER_STATUS, default='0')
    username = models.CharField(max_length=30)
    password = models.CharField(_('password'), max_length=128)
    name = models.CharField(max_length=30)
    face = models.CharField(max_length=30)
    mobile = models.CharField(max_length=50, default='0')
    email = models.EmailField(_('e-mail address'))
    address = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=30)
    birthday = models.DateField()
    idcard = models.CharField(max_length=30)
    idcardtype = models.CharField(max_length=1, choices=CARD_TYPE, default='1')
    content = models.CharField(max_length=200)
    memo = models.CharField(max_length=100)
    contact = models.CharField(max_length=30)
    contactmobile = models.CharField(max_length=30)
    objects = UserManager()
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    #loginlog = models.CharField(max_length=100)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)







