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
# from django.contrib.auth.hashers import (
#    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)

# Create your models here.



"""
Authority Management
"""
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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    #loginlog = models.CharField(max_length=100)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)



"""
Device Management
"""
class k_devicetype(models.Model):
    parentid = models.PositiveIntegerField()
    depthnumber = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_supplier(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    addr = models.CharField(max_length=80)
    memo = models.CharField(max_length=100)
    creator = models.CharField(max_length=30)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()

class k_producer(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    addr = models.CharField(max_length=80)
    memo = models.CharField(max_length=100)
    creator = models.CharField(max_length=30)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()

class k_spare(models.Model):
    classid = models.ForeignKey(k_class, related_name='spare_set')
    name = models.CharField(max_length=30) #项目本级内唯一
    brief = models.CharField(max_length=30) #编号，项目内本级唯一
    brand = models.CharField(max_length=30)
    producerid = models.ForeignKey(k_producer, related_name='spare_set')
    typeid = models.ForeignKey(k_devicetype, related_name='spare_set')
    model = models.CharField(max_length=30)
    supplierid = models.ForeignKey(k_supplier, related_name='spare_set')
    content = models.CharField(max_length=200)
    memo = models.CharField(max_length=100)
    minimum = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    ownerid = models.PositiveIntegerField()

class k_device(models.Model):
    DEVICE_STATUS = (
        ('0', '锁定'),
        ('1', '正常'),
        ('2', '停用'),
        ('3', '故障'),
        ('4', '维修'),
        ('5', '保养'),
    )
    classid = models.ForeignKey(k_class, related_name='device_set')
    brand = models.CharField(max_length=30)
    producerid = models.ForeignKey(k_producer, related_name='device_set')
    typeid = models.ForeignKey(k_devicetype, related_name='device_set')
    supplierid = models.ForeignKey(k_supplier, related_name='device_set')
    state = models.CharField(max_length=1, choices=DEVICE_STATUS, default='0')
    name = models.CharField(max_length=30) #分类内唯一
    brief = models.CharField(max_length=30) #编号，项目内唯一
    serial = models.CharField(max_length=80)
    model = models.CharField(max_length=30)
    buytime = models.DateField()
    content = models.CharField(max_length=200)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    lastmaintenance = models.DateField()
    nextmaintenance = models.DateField()
    maintenanceperiod = models.PositiveIntegerField()
    lastrepaire = models.DateField()
    spare = models.ManyToManyField(k_spare)
    lastmeter = models.DateField()
    notice = models.CharField(max_length=100)
    #statelog = models.CharField(max_length=100)
    ownerid = models.PositiveIntegerField()



"""
Meter, Maintenance
"""
class k_formitem(models.Model):
    classid = models.ForeignKey(k_class, related_name='formitem_set')
    name = models.CharField(max_length=30)
    threshold = models.CharField(max_length=30)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_form(models.Model):
    classid = models.ForeignKey(k_class, related_name='form_set')
    content = models.CharField(max_length=200)
    formitemid = models.ManyToManyField(k_formitem)
    period = models.PositiveIntegerField()
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_route(models.Model):
    classid = models.ForeignKey(k_class, related_name='route_set')
    formid = models.CharField(max_length=80)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_maintenance(models.Model):
    MAINTENANCE_STATUS = (
        ('1', '计划'),
        ('2', '维修中'),
        ('3', '维修完成'),
        ('4', '审核完成'),
    )
    MAINTENANCE_TYPE = (
        ('1', '保养'),
        ('2', '维修'),
    )
    MAINTENANCE_PRIORITY = (
        ('1', '一般'),
        ('2', '重要'),
        ('3', '紧急'),
    )
    deviceid = models.ForeignKey(k_device, related_name='maintenance_set')
    state = models.CharField(max_length=1, choices=MAINTENANCE_STATUS, default='1')
    title = models.CharField(max_length=50)
    createcontent = models.CharField(max_length=100)
    editcontent = models.CharField(max_length=100)
    auditcontent = models.CharField(max_length=100)
    memo = models.CharField(max_length=100)
    mtype = models.CharField(max_length=1, choices=MAINTENANCE_TYPE, default='1')
    priority = models.CharField(max_length=1, choices=MAINTENANCE_PRIORITY, default='1')
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    #statelog = models.CharField(max_length=100)

class k_bill(models.Model):
    BILL_STATUS = (
        ('1', '采购入库'),
        ('2', '领用退回'),
        ('3', '对账入库'),
        ('4', '采购退货'),
        ('5', '领用出库'),
        ('6', '对账出库'),
    )
    classid = models.ForeignKey(k_class, related_name='bill_set')
    state = models.CharField(max_length=1, choices=BILL_STATUS, default='1')
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_sparecount(models.Model):
    SPARECOUNT_STATUS = (
        ('1', '采购入库'),
        ('2', '领用退回'),
        ('3', '对账入库'),
        ('4', '采购退货'),
        ('5', '领用出库'),
        ('6', '对账出库'),
    )
    billid = models.ForeignKey(k_bill)
    maintenanceid = models.ManyToManyField(k_maintenance)
    deviceid = models.ForeignKey(k_device)
    spareid = models.ForeignKey(k_spare)
    count = models.IntegerField()
    state = models.CharField(max_length=1, choices=SPARECOUNT_STATUS, default='1')
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')



"""
Tool Management
"""
class k_tool(models.Model):
    classid = models.ForeignKey(k_class, related_name='tool_set')
    name = models.CharField(max_length=30) #项目本级内唯一
    brief = models.CharField(max_length=30) #编号，项目内本级唯一
    brand = models.CharField(max_length=30)
    producerid = models.ForeignKey(k_producer, related_name='tool_set')
    typeid = models.ForeignKey(k_devicetype, related_name='tool_set')
    model = models.CharField(max_length=30)
    supplierid = models.ForeignKey(k_supplier, related_name='tool_set')
    content = models.CharField(max_length=200)
    memo = models.CharField(max_length=100)
    minimum = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_tooluse(models.Model):
    parentid = models.PositiveIntegerField() #领用0，归还大于0
    toolid = models.ForeignKey(k_tool, related_name='tooluse_set')
    number = models.PositiveIntegerField()
    ownerid = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

class k_toolcount(models.Model):
    TOOLCOUNT_STATUS = (
        ('1', '采购入库'),
        ('2', '领用退回'),
        ('3', '对账入库'),
        ('4', '采购退货'),
        ('5', '领用出库'),
        ('6', '对账出库'),
    )
    toolid = models.ForeignKey(k_tool, related_name='toolcount_set')
    tooluseid = models.ForeignKey(k_tooluse, related_name='toolcount_set') #不是领用或归还为0
    count = models.IntegerField()
    state = models.CharField(max_length=1, choices=TOOLCOUNT_STATUS, default='1')
    memo = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    creatorid = models.PositiveIntegerField()
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField()
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField()
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')