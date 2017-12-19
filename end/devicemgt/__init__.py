from models import *
from helper import get_current_time
from datetime import datetime, timedelta, time
import time, os, sched, threading  

def get_endday(st, prd):
	if prd == "day":
		return st + timedelta(days=1)
	elif prd == "week":
		return st + timedelta(days=7)
	elif prd == "halfmonth":
		return st + timedelta(days=15)
	elif prd == "month":
		return st + timedelta(days=30)
	elif prd == "twomonth":
		return st + timedelta(days=61)
	elif prd == "threemonth":
		return st + timedelta(days=91)
	elif prd == "fourmonth":
		return st + timedelta(days=121)
	elif prd == "halfyear":
		return st + timedelta(days=182)
	elif prd == "year":
		return st + timedelta(days=365)
	elif prd == "twoyear":
		return st + timedelta(days=730)

def perform_command(cmd, inc):
    print "haha"
    _deviceplans = k_deviceplan.objects.all()
    _today = date.today()
    for _dp in _deviceplans:
    	_maintenance = k_maintenance.objects.get(id=_dp.maintenanceid_id)
    	_startday = _maintenance.assigndatetime.date()
    	_endday = get_endday(_startday, _dp.period)
    	if _today < _endday:
    		if _maintenance.state == '4' or _maintenance.state == '5':
    			_newmaintenance = k_maintenance.objects.create(mtype=1,classid=_maintenance.classid,deviceid_id=_maintenance.deviceid_id,state=2)
    			_newmaintenance.creatorid = _maintenance.creatorid
    			_newmaintenance.assignorid = _maintenance.assignorid
    			_newmaintenance.assigndatetime = get_current_time()
    			_newmaintenance.title = _maintenance.title
    			_newmaintenance.createcontent = _maintenance.createcontent
    			_newmaintenance.editorid = _maintenance.editorid
    			_newmaintenance.memo = _maintenance.memo
    			_newmaintenance.state = 2
    			_newmaintenance.save()
    			_dp.maintenanceid_id = _newmaintenance.id
    			_dp.save()
        else:
            if _maintenance.state != '4' and _maintenance.state != '5':
                _maintenance.createdatetime = get_current_time()
                _maintenance.assigndatetime = get_current_time()
                _maintenance.save()
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    schedule.run()
        
def timming_exe(cmd, inc):
    schedule.enter(inc, 0, perform_command, (cmd, 86400))
    schedule.run()

def thread_fun(remainedsec):
    timming_exe("123", remainedsec)

print "123"
schedule = sched.scheduler(time.time, time.sleep)
print "123"
nowtime = time.localtime(time.time())
print "123"
remainedsec = 86400-(nowtime.tm_hour*3600+nowtime.tm_min*60+nowtime.tm_sec)-60
print "123"
thread = threading.Thread(target = thread_fun, args = (remainedsec,))
print "123"
thread.start()
print "123"