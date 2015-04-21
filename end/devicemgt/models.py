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
from datetime import date
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)

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

    def create_user(self, classid, state, username, password, name, face, mobile, email, address, zipcode, birthday,
                    idcard, idcardtype, content, memo, contact, contactmobile, creatorid, createdatetime, editorid,
                    editdatetime, auditorid, auditdatetime, status ):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(classid=classid, state=state, username=username,
            password=password, name=name, face=face, mobile = mobile, email=email, address=address, zipcode=zipcode,
            birthday=birthday, idcard=idcard, idcardtype=idcardtype, content=content, memo=memo, contact=contact, contactmobile=contactmobile,
            creatorid=creatorid, createdatetime=createdatetime, editorid=editorid, editdatetime=editdatetime,
            auditorid=auditorid, auditdatetime=auditdatetime, status=status)
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
    depth = models.PositiveIntegerField() #such as "3", means "班组"
    depthname = models.CharField(max_length=50) #such as "班组"
    # roles = models.ManyToManyField(k_role) #absorbed to k_classrole
    name = models.CharField(max_length=30) #such as "空调组"
    code = models.CharField(max_length=5) #4 digits, globally unique
    logo = models.CharField(max_length=30)
    address = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=30)
    phone = models.CharField(max_length=50, default='0')
    license = models.CharField(max_length=30)
    licensetype = models.CharField(max_length=30, default='企业营业执照')
    content = models.CharField(max_length=200)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField()
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField()
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_purview(models.Model):
    classid = models.ForeignKey(k_class, related_name='purview_set')
    name = models.CharField(max_length=20) #such as "设备"
    item = models.CharField(max_length=20) #such as "查看"、"添加"、"编辑"、"审核"、"删除"
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_role(models.Model):
    classid = models.ForeignKey(k_class, related_name='role_set')
    name = models.CharField(max_length=30) #such as "权限设计", "维修记录", etc.
    purviews = models.ManyToManyField(k_purview)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_classrole(models.Model):
    classid = models.ForeignKey(k_class, related_name='classrole_set')
    roleid = models.ForeignKey(k_role, related_name='classrole_set')

class k_user(models.Model):
    USER_STATUS = (
        ('0', '锁定'),
        ('1', '在岗'),
        ('2', '长假'),
        ('3', '离职'),
    )
    GENDER_CHOICES = (
        ('0', '女'),
        ('1', '男'),
    )
    CARD_TYPE = (
        ('1','身份证'),
    )
    classid = models.ForeignKey(k_class, related_name='user_set')
    roles = models.ManyToManyField(k_role)
    state = models.CharField(max_length=1, choices=USER_STATUS, default='0')
    username = models.CharField(max_length=30)
    password = models.CharField(_('password'), max_length=128)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='1')
    face = models.CharField(max_length=30)
    mobile = models.CharField(max_length=50, default='0')
    email = models.EmailField(_('e-mail address'))
    address = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=30)
    birthday = models.DateField(blank=True, default=date.today)
    idcard = models.CharField(max_length=30)
    idcardtype = models.CharField(max_length=1, choices=CARD_TYPE, default='1')
    content = models.CharField(max_length=200)
    memo = models.CharField(max_length=100)
    contact = models.CharField(max_length=30)
    contactmobile = models.CharField(max_length=30)
    objects = UserManager()
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    #? loginlog = models.CharField(max_length=100)
    todo = models.PositiveIntegerField(default=0)
    onlinetime = models.PositiveIntegerField(default=0)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)



"""
Device Management
"""
class k_devicetype(models.Model):
    parentid = models.PositiveIntegerField()
    depth = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_supplier(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    addr = models.CharField(max_length=80)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)

class k_producer(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    addr = models.CharField(max_length=80)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)

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
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
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
    qrcode = models.CharField(max_length=625)
    position = models.CharField(max_length=80)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    lastmaintenance = models.DateField(blank=True, default=date.today)
    nextmaintenance = models.DateField(blank=True, default=date.today)
    maintenanceperiod = models.PositiveIntegerField()
    lastrepaire = models.DateField(blank=True, default=date.today)
    spare = models.ManyToManyField(k_spare)
    lastmeter = models.DateField(blank=True, default=date.today)
    notice = models.CharField(max_length=100)
    #? statelog = models.CharField(max_length=100)
    ownerid = models.PositiveIntegerField()

class k_form(models.Model):
    classid = models.ForeignKey(k_class, related_name='form_set')
    content = models.CharField(max_length=200)
    brief = models.CharField(max_length=30)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_formitem(models.Model):
    classid = models.ForeignKey(k_class, related_name='formitem_set')
    formid = models.ForeignKey(k_form, related_name='formitem_set')
    name = models.CharField(max_length=30)
    threshold = models.CharField(max_length=30)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')



"""
Route, Meter, Maintenance, Task
"""
class k_route(models.Model):
    classid = models.ForeignKey(k_class, related_name='route_set')
    name = models.CharField(max_length=80)
    formid = models.CharField(max_length=80)
    starttime = models.TimeField()
    period = models.PositiveIntegerField()
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_meter(models.Model):
    METER_STATUS = (
        ('0', '不正常'),
        ('1', '正常'),
        ('2', '引起注意'),
    )
    deviceid = models.ForeignKey(k_device, related_name='meter_set')
    state = models.CharField(max_length=1, choices=METER_STATUS, default='0')
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    memo = models.CharField(max_length=100)
    orderedtime = models.TimeField()
    metertime = models.DateTimeField(auto_now=True)
    routeid = models.ForeignKey(k_route, related_name='meter_set')
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
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
    image = models.CharField(max_length=30)
    factor = models.PositiveIntegerField()
    memo = models.CharField(max_length=100)
    mtype = models.CharField(max_length=1, choices=MAINTENANCE_TYPE, default='1')
    priority = models.CharField(max_length=1, choices=MAINTENANCE_PRIORITY, default='1')
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    #? statelog = models.CharField(max_length=100)

class k_task(models.Model):
    TASK_STATUS = (
        ('1', '计划'),
        ('2', '执行中'),
        ('3', '执行完成'),
        ('4', '审核完成'),
    )
    TASK_PRIORITY = (
        ('1', '一般'),
        ('2', '重要'),
        ('3', '紧急'),
    )
    state = models.CharField(max_length=1, choices=TASK_STATUS, default='1')
    title = models.CharField(max_length=50)
    createcontent = models.CharField(max_length=100)
    editcontent = models.CharField(max_length=100)
    auditcontent = models.CharField(max_length=100)
    memo = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=TASK_PRIORITY, default='1')
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

class k_taskitem(models.Model):
    TASK_STATUS = (
        ('1', '计划'),
        ('2', '执行中'),
        ('3', '执行完成'),
        ('4', '审核完成'),
    )
    TASK_PRIORITY = (
        ('1', '一般'),
        ('2', '重要'),
        ('3', '紧急'),
    )
    state = models.CharField(max_length=1, choices=TASK_STATUS, default='1')
    title = models.CharField(max_length=50)
    taskid = models.ForeignKey(k_task, related_name='taskitem_set')
    createcontent = models.CharField(max_length=100)
    editcontent = models.CharField(max_length=100)
    auditcontent = models.CharField(max_length=100)
    factor = models.PositiveIntegerField()
    memo = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=TASK_PRIORITY, default='1')
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')



"""
Stock Management
"""
class k_sparebill(models.Model):
    BILL_STATUS = (
        ('1', '采购入库'),
        ('2', '领用退回'),
        ('3', '对账入库'),
        ('4', '采购退货'),
        ('5', '领用出库'),
        ('6', '对账出库'),
    )
    classid = models.ForeignKey(k_class, related_name='sparebill_set')
    state = models.CharField(max_length=1, choices=BILL_STATUS, default='1')
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
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
    billid = models.ForeignKey(k_sparebill)
    maintenanceid = models.ManyToManyField(k_maintenance)
    deviceid = models.ForeignKey(k_device)
    spareid = models.ForeignKey(k_spare)
    count = models.IntegerField()
    state = models.CharField(max_length=1, choices=SPARECOUNT_STATUS, default='1')
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

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
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
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
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
    editorid = models.PositiveIntegerField(default=0)
    editdatetime = models.DateField(blank=True, default=date.today)
    auditorid = models.PositiveIntegerField(default=0)
    auditdatetime = models.DateField(blank=True, default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')



"""
Others
"""
class k_project(models.Model):
    classid = models.ForeignKey(k_class, related_name='project_set')
    meterscore = models.PositiveIntegerField()
    maintenancescore = models.PositiveIntegerField()
    taskscore = models.PositiveIntegerField()
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)

class k_schedule(models.Model):
    classid = models.ForeignKey(k_class, related_name='schedule_set')
    range = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    memo = models.CharField(max_length=100)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)

class k_staffworkinfo(models.Model):
    userid = models.ForeignKey(k_user, related_name='staffworkinfo_set')
    checkin = models.DateField(blank=True, default=date.today)
    checkout = models.DateField(blank=True, default=date.today)
    shifting = models.CharField(max_length=1) #1 yes, 0 no

class k_staffscoreinfo(models.Model):
    userid = models.ForeignKey(k_user, related_name='staffscoreinfo_set')
    score = models.PositiveIntegerField()
    content = models.CharField(max_length=80)
    time = models.DateField(blank=True, default=date.today)

class k_staffegginfo(models.Model):
    userid = models.ForeignKey(k_user, related_name='staffegginfo_set')
    time = models.DateField(blank=True, default=date.today)
    state = models.CharField(max_length=1) #1 yes, 0 no

class k_feedback(models.Model):
    feedback = models.CharField(max_length=200)
    creatorid = models.PositiveIntegerField(default=0)
    createdatetime = models.DateField(blank=True, default=date.today)
