# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'k_class'
        db.create_table(u'devicemgt_k_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parentid', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('depthname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('logo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='0', max_length=50)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('licensetype', self.gf('django.db.models.fields.CharField')(default='\xe4\xbc\x81\xe4\xb8\x9a\xe8\x90\xa5\xe4\xb8\x9a\xe6\x89\xa7\xe7\x85\xa7', max_length=50)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_class'])

        # Adding model 'k_purview'
        db.create_table(u'devicemgt_k_purview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purview_set', to=orm['devicemgt.k_class'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('item', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_purview'])

        # Adding model 'k_role'
        db.create_table(u'devicemgt_k_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='role_set', to=orm['devicemgt.k_class'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_role'])

        # Adding M2M table for field purviews on 'k_role'
        m2m_table_name = db.shorten_name(u'devicemgt_k_role_purviews')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('k_role', models.ForeignKey(orm[u'devicemgt.k_role'], null=False)),
            ('k_purview', models.ForeignKey(orm[u'devicemgt.k_purview'], null=False))
        ))
        db.create_unique(m2m_table_name, ['k_role_id', 'k_purview_id'])

        # Adding model 'k_classrole'
        db.create_table(u'devicemgt_k_classrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classrole_set', to=orm['devicemgt.k_class'])),
            ('roleid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classrole_set', to=orm['devicemgt.k_role'])),
        ))
        db.send_create_signal(u'devicemgt', ['k_classrole'])

        # Adding model 'k_user'
        db.create_table(u'devicemgt_k_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('face', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avatar', self.gf('django.db.models.fields.files.FileField')(default='user_avatar/undefined.png', max_length=100)),
            ('mobile', self.gf('django.db.models.fields.CharField')(default='0', max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('birthday', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('idcard', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('idcardtype', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contactmobile', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('todo', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('onlinetime', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'devicemgt', ['k_user'])

        # Adding M2M table for field roles on 'k_user'
        m2m_table_name = db.shorten_name(u'devicemgt_k_user_roles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('k_user', models.ForeignKey(orm[u'devicemgt.k_user'], null=False)),
            ('k_role', models.ForeignKey(orm[u'devicemgt.k_role'], null=False))
        ))
        db.create_unique(m2m_table_name, ['k_user_id', 'k_role_id'])

        # Adding model 'k_devicetype'
        db.create_table(u'devicemgt_k_devicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parentid', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_devicetype'])

        # Adding model 'k_supplier'
        db.create_table(u'devicemgt_k_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('addr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('linkman', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
        ))
        db.send_create_signal(u'devicemgt', ['k_supplier'])

        # Adding model 'k_producer'
        db.create_table(u'devicemgt_k_producer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('addr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('linkman', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
        ))
        db.send_create_signal(u'devicemgt', ['k_producer'])

        # Adding model 'k_spare'
        db.create_table(u'devicemgt_k_spare', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='spare_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('producerid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='spare_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_producer'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('supplierid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='spare_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_supplier'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('minimum', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('eligiblestock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ineligiblestock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_spare'])

        # Adding model 'k_device'
        db.create_table(u'devicemgt_k_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('producerid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_producer'])),
            ('typeid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_devicetype'])),
            ('supplierid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='device_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_supplier'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('buytime', self.gf('django.db.models.fields.DateField')()),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('qrcode', self.gf('django.db.models.fields.CharField')(max_length=625)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('lastmaintenance', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nextmaintenance', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('maintenanceperiod', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('lastrepaire', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('spare', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('lastmeter', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notice', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('statelog', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('ownerid', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'devicemgt', ['k_device'])

        # Adding model 'k_form'
        db.create_table(u'devicemgt_k_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='form_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_form'])

        # Adding model 'k_formitem'
        db.create_table(u'devicemgt_k_formitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='formitem_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('formid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='formitem_set', to=orm['devicemgt.k_form'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datatype', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lowerthreshold', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('upperthreshold', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('choices', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_formitem'])

        # Adding model 'k_route'
        db.create_table(u'devicemgt_k_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='route_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('formid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('starttime', self.gf('django.db.models.fields.TimeField')()),
            ('period', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_route'])

        # Adding model 'k_meter'
        db.create_table(u'devicemgt_k_meter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('routeid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='meter_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_route'])),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='meter_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_user'])),
            ('metertime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'devicemgt', ['k_meter'])

        # Adding model 'k_maintenance'
        db.create_table(u'devicemgt_k_maintenance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='maintenance_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('deviceid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='maintenance_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_device'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('createcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('editcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('factor', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mtype', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('assignorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('assigndatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_maintenance'])

        # Adding model 'k_deviceplan'
        db.create_table(u'devicemgt_k_deviceplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deviceid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deviceplan_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_device'])),
            ('maintenanceid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deviceplan_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_maintenance'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('period', self.gf('django.db.models.fields.CharField')(default='0', max_length=15)),
            ('createcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('assignorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('assigndatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_deviceplan'])

        # Adding model 'k_task'
        db.create_table(u'devicemgt_k_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('createcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('editcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('auditcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_task'])

        # Adding model 'k_taskitem'
        db.create_table(u'devicemgt_k_taskitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('taskid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='taskitem_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_task'])),
            ('createcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('editcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('helpersid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('auditcontent', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('factor', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_taskitem'])

        # Adding model 'k_sparebill'
        db.create_table(u'devicemgt_k_sparebill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sparebill_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('spareid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sparebill_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_spare'])),
            ('using', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('returned', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('depleted', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('damaged', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('rejected', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_sparebill'])

        # Adding model 'k_sparecount'
        db.create_table(u'devicemgt_k_sparecount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sparecount_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('sparebillid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('spareid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sparecount_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_spare'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('state', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('iseligible', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_sparecount'])

        # Adding model 'k_tool'
        db.create_table(u'devicemgt_k_tool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='toolclass_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('producerid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tool_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_producer'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('supplierid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tool_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_supplier'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('minimum', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('eligiblestock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ineligiblestock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('ownerid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='toolowner_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
        ))
        db.send_create_signal(u'devicemgt', ['k_tool'])

        # Adding model 'k_tooluse'
        db.create_table(u'devicemgt_k_tooluse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tooluse_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('toolid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tooluse_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_tool'])),
            ('using', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('returned', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('depleted', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('damaged', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('rejected', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_tooluse'])

        # Adding model 'k_toolcount'
        db.create_table(u'devicemgt_k_toolcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='toolcount_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('tooluseid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('toolid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='toolcount_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_tool'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('state', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('iseligible', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('editorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('editdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('auditorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('auditdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_toolcount'])

        # Adding model 'k_project'
        db.create_table(u'devicemgt_k_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='project_set', null=True, on_delete=models.SET_NULL, to=orm['devicemgt.k_class'])),
            ('meterscore', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('maintenancescore', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('taskscore', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
        ))
        db.send_create_signal(u'devicemgt', ['k_project'])

        # Adding model 'k_schedule'
        db.create_table(u'devicemgt_k_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedule_set', to=orm['devicemgt.k_class'])),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedule_set', to=orm['devicemgt.k_route'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='schedule_set', to=orm['devicemgt.k_user'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'devicemgt', ['k_schedule'])

        # Adding model 'k_staffworkinfo'
        db.create_table(u'devicemgt_k_staffworkinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='staffworkinfo_set', to=orm['devicemgt.k_user'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('checkin', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('checkout', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shifting', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_staffworkinfo'])

        # Adding model 'k_staffscoreinfo'
        db.create_table(u'devicemgt_k_staffscoreinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='staffscoreinfo_set', to=orm['devicemgt.k_user'])),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('time', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
        ))
        db.send_create_signal(u'devicemgt', ['k_staffscoreinfo'])

        # Adding model 'k_staffegginfo'
        db.create_table(u'devicemgt_k_staffegginfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='staffegginfo_set', to=orm['devicemgt.k_user'])),
            ('time', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('bonus', self.gf('django.db.models.fields.FloatField')()),
            ('probability', self.gf('django.db.models.fields.FloatField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'devicemgt', ['k_staffegginfo'])

        # Adding model 'k_feedback'
        db.create_table(u'devicemgt_k_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('creatorid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('createdatetime', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
        ))
        db.send_create_signal(u'devicemgt', ['k_feedback'])

        # Adding model 'k_config'
        db.create_table(u'devicemgt_k_config', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eggbonus', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('eggprobability', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'devicemgt', ['k_config'])


    def backwards(self, orm):
        # Deleting model 'k_class'
        db.delete_table(u'devicemgt_k_class')

        # Deleting model 'k_purview'
        db.delete_table(u'devicemgt_k_purview')

        # Deleting model 'k_role'
        db.delete_table(u'devicemgt_k_role')

        # Removing M2M table for field purviews on 'k_role'
        db.delete_table(db.shorten_name(u'devicemgt_k_role_purviews'))

        # Deleting model 'k_classrole'
        db.delete_table(u'devicemgt_k_classrole')

        # Deleting model 'k_user'
        db.delete_table(u'devicemgt_k_user')

        # Removing M2M table for field roles on 'k_user'
        db.delete_table(db.shorten_name(u'devicemgt_k_user_roles'))

        # Deleting model 'k_devicetype'
        db.delete_table(u'devicemgt_k_devicetype')

        # Deleting model 'k_supplier'
        db.delete_table(u'devicemgt_k_supplier')

        # Deleting model 'k_producer'
        db.delete_table(u'devicemgt_k_producer')

        # Deleting model 'k_spare'
        db.delete_table(u'devicemgt_k_spare')

        # Deleting model 'k_device'
        db.delete_table(u'devicemgt_k_device')

        # Deleting model 'k_form'
        db.delete_table(u'devicemgt_k_form')

        # Deleting model 'k_formitem'
        db.delete_table(u'devicemgt_k_formitem')

        # Deleting model 'k_route'
        db.delete_table(u'devicemgt_k_route')

        # Deleting model 'k_meter'
        db.delete_table(u'devicemgt_k_meter')

        # Deleting model 'k_maintenance'
        db.delete_table(u'devicemgt_k_maintenance')

        # Deleting model 'k_deviceplan'
        db.delete_table(u'devicemgt_k_deviceplan')

        # Deleting model 'k_task'
        db.delete_table(u'devicemgt_k_task')

        # Deleting model 'k_taskitem'
        db.delete_table(u'devicemgt_k_taskitem')

        # Deleting model 'k_sparebill'
        db.delete_table(u'devicemgt_k_sparebill')

        # Deleting model 'k_sparecount'
        db.delete_table(u'devicemgt_k_sparecount')

        # Deleting model 'k_tool'
        db.delete_table(u'devicemgt_k_tool')

        # Deleting model 'k_tooluse'
        db.delete_table(u'devicemgt_k_tooluse')

        # Deleting model 'k_toolcount'
        db.delete_table(u'devicemgt_k_toolcount')

        # Deleting model 'k_project'
        db.delete_table(u'devicemgt_k_project')

        # Deleting model 'k_schedule'
        db.delete_table(u'devicemgt_k_schedule')

        # Deleting model 'k_staffworkinfo'
        db.delete_table(u'devicemgt_k_staffworkinfo')

        # Deleting model 'k_staffscoreinfo'
        db.delete_table(u'devicemgt_k_staffscoreinfo')

        # Deleting model 'k_staffegginfo'
        db.delete_table(u'devicemgt_k_staffegginfo')

        # Deleting model 'k_feedback'
        db.delete_table(u'devicemgt_k_feedback')

        # Deleting model 'k_config'
        db.delete_table(u'devicemgt_k_config')


    models = {
        u'devicemgt.k_class': {
            'Meta': {'object_name': 'k_class'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'depthname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'licensetype': ('django.db.models.fields.CharField', [], {'default': "'\\xe4\\xbc\\x81\\xe4\\xb8\\x9a\\xe8\\x90\\xa5\\xe4\\xb8\\x9a\\xe6\\x89\\xa7\\xe7\\x85\\xa7'", 'max_length': '50'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parentid': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_classrole': {
            'Meta': {'object_name': 'k_classrole'},
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classrole_set'", 'to': u"orm['devicemgt.k_class']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roleid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classrole_set'", 'to': u"orm['devicemgt.k_role']"})
        },
        u'devicemgt.k_config': {
            'Meta': {'object_name': 'k_config'},
            'eggbonus': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'eggprobability': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'devicemgt.k_device': {
            'Meta': {'object_name': 'k_device'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'buytime': ('django.db.models.fields.DateField', [], {}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastmaintenance': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lastmeter': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lastrepaire': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'maintenanceperiod': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nextmaintenance': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'notice': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'ownerid': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'producerid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_producer']"}),
            'qrcode': ('django.db.models.fields.CharField', [], {'max_length': '625'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'spare': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'statelog': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'supplierid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_supplier']"}),
            'typeid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'device_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_devicetype']"})
        },
        u'devicemgt.k_deviceplan': {
            'Meta': {'object_name': 'k_deviceplan'},
            'assigndatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'assignorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'createcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'deviceid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deviceplan_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_device']"}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintenanceid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deviceplan_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_maintenance']"}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'period': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '15'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_devicetype': {
            'Meta': {'object_name': 'k_devicetype'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parentid': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'devicemgt.k_feedback': {
            'Meta': {'object_name': 'k_feedback'},
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'devicemgt.k_form': {
            'Meta': {'object_name': 'k_form'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'form_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'devicemgt.k_formitem': {
            'Meta': {'object_name': 'k_formitem'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'formitem_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'datatype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'formid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'formitem_set'", 'to': u"orm['devicemgt.k_form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowerthreshold': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'upperthreshold': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_maintenance': {
            'Meta': {'object_name': 'k_maintenance'},
            'assigndatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'assignorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'maintenance_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'deviceid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'maintenance_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_device']"}),
            'editcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mtype': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_meter': {
            'Meta': {'object_name': 'k_meter'},
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'metertime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'routeid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'meter_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_route']"}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'meter_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_user']"})
        },
        u'devicemgt.k_producer': {
            'Meta': {'object_name': 'k_producer'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkman': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_project': {
            'Meta': {'object_name': 'k_project'},
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintenancescore': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'meterscore': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'taskscore': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'devicemgt.k_purview': {
            'Meta': {'object_name': 'k_purview'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purview_set'", 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'devicemgt.k_role': {
            'Meta': {'object_name': 'k_role'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'role_set'", 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'purviews': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['devicemgt.k_purview']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'devicemgt.k_route': {
            'Meta': {'object_name': 'k_route'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'route_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'formid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'starttime': ('django.db.models.fields.TimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'devicemgt.k_schedule': {
            'Meta': {'object_name': 'k_schedule'},
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_set'", 'to': u"orm['devicemgt.k_class']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_set'", 'to': u"orm['devicemgt.k_route']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_set'", 'to': u"orm['devicemgt.k_user']"})
        },
        u'devicemgt.k_spare': {
            'Meta': {'object_name': 'k_spare'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'spare_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'eligiblestock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ineligiblestock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'minimum': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'producerid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'spare_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_producer']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'supplierid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'spare_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_supplier']"})
        },
        u'devicemgt.k_sparebill': {
            'Meta': {'object_name': 'k_sparebill'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sparebill_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'damaged': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'depleted': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rejected': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'returned': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'spareid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sparebill_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_spare']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'using': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'devicemgt.k_sparecount': {
            'Meta': {'object_name': 'k_sparecount'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sparecount_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iseligible': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sparebillid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'spareid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sparecount_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_spare']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'devicemgt.k_staffegginfo': {
            'Meta': {'object_name': 'k_staffegginfo'},
            'bonus': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'probability': ('django.db.models.fields.FloatField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'time': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staffegginfo_set'", 'to': u"orm['devicemgt.k_user']"})
        },
        u'devicemgt.k_staffscoreinfo': {
            'Meta': {'object_name': 'k_staffscoreinfo'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staffscoreinfo_set'", 'to': u"orm['devicemgt.k_user']"})
        },
        u'devicemgt.k_staffworkinfo': {
            'Meta': {'object_name': 'k_staffworkinfo'},
            'checkin': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'checkout': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shifting': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staffworkinfo_set'", 'to': u"orm['devicemgt.k_user']"})
        },
        u'devicemgt.k_supplier': {
            'Meta': {'object_name': 'k_supplier'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkman': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_task': {
            'Meta': {'object_name': 'k_task'},
            'auditcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_taskitem': {
            'Meta': {'object_name': 'k_taskitem'},
            'auditcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'createcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editcontent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'factor': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'helpersid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'taskid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskitem_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_task']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'devicemgt.k_tool': {
            'Meta': {'object_name': 'k_tool'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'toolclass_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'eligiblestock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ineligiblestock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'minimum': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ownerid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'toolowner_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'producerid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tool_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_producer']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'supplierid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tool_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_supplier']"})
        },
        u'devicemgt.k_toolcount': {
            'Meta': {'object_name': 'k_toolcount'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'toolcount_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iseligible': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'toolid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'toolcount_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_tool']"}),
            'tooluseid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'devicemgt.k_tooluse': {
            'Meta': {'object_name': 'k_tooluse'},
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tooluse_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'damaged': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'depleted': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rejected': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'returned': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'toolid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tooluse_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_tool']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'using': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'devicemgt.k_user': {
            'Meta': {'object_name': 'k_user'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'auditdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'auditorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'avatar': ('django.db.models.fields.files.FileField', [], {'default': "'user_avatar/undefined.png'", 'max_length': '100'}),
            'birthday': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'classid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['devicemgt.k_class']"}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contactmobile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'createdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'creatorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'editdatetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'editorid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'face': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcard': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'idcardtype': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'onlinetime': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['devicemgt.k_role']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'todo': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['devicemgt']