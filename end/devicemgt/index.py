__author__ = 'LY'
import time
from models import *


def get_user_num(parentid):
    users = k_user.objects.filter(classid_id=parentid)
    return len(users)


def get_device_num(parentid):
    devices = k_device.objects.filter(classid_id=parentid)
    return len(devices)

def get_user_score(userid):
    userscores = k_staffscoreinfo.objects.filter(userid=userid)
    sum = 0
    month = int(time.strftime('%m',time.localtime(time.time())))
    for userscore in userscores:
        scoremonth = userscore.time.month
        if scoremonth == month:
            sum += userscore.score
    return sum


def get_user_rank(userid, parentid):
    users = k_user.objects.filter(classid_id=parentid)
    score = dict()
    for user in users:
        score[user.id] = get_user_score(user.id)
    rank = sorted(score.items(), key=lambda d:d[1], reverse=True)
    for i in xrange(0,len(rank)):
        if rank[i][0] == userid:
            return i + 1
    return len(rank) + 1

def get_user_unmaintenance(userid, mtype):
    unmains = k_maintenance.objects.filter(state__gte=2,state__lte=3,mtype=mtype, editorid=userid)
    return len(unmains)


def get_user_unfinishedtask(userid):
    tasks = k_taskitem.objects.filter(state__gte=1,state__lte=2, editorid=userid)
    return len(tasks)

def get_using_spare(parentid):
    spares = k_sparebill.objects.filter(classid_id=parentid)
    sum = 0
    for s in spares:
        using = s.using - s.returned - s.depleted - s.damaged - s.rejected
        if using > 0:
            sum += using
    return sum

def get_using_tool(parentid):
    tools = k_tooluse.objects.filter(classid_id=parentid)
    sum = 0
    for s in tools:
        using = s.using - s.returned - s.depleted - s.damaged - s.rejected
        if using > 0:
            sum += using
    return 0


def get_attendence_stat(parentid):
    week=int(time.strftime("%w"))
    stat = [0,0,0,0,0,0,0]
    for i in xrange(0,week):
        day = time.strftime('%Y-%m-%d',time.localtime(time.time()-i*24*60*60))
        allusers = k_staffworkinfo.objects.filter(date=day)
        usernum = 0
        for u in allusers:
            users = k_user.objects.filter(id=u.userid_id)
            if len(users) == 1:
                if users[0].classid_id == parentid:
                    usernum += 1
        stat[week-i-1] = usernum
    return stat


def get_task_num_by_class(tasks, parentid):
    num = 0
    for t in tasks:
        tmp = k_task.objects.filter(id=t.taskid_id)
        if len(tmp) == 1:
            if tmp[0].classid_id == parentid:
                num+=1
    return num


def get_task_stat(parentid):
    stat = [0,0,0,0]
    month = int(time.strftime('%m',time.localtime(time.time())))
    for i in xrange(0,3):
        tasks = k_taskitem.objects.filter(state=i+1)
        stat[i] = get_task_num_by_class(tasks, parentid)
    tasks = k_taskitem.objects.filter(state=4,auditdatetime__month=month)
    stat[3] = get_task_num_by_class(tasks, parentid)
    return stat


def get_maintenace_stat(parentid, mtype):
    stat = [0,0,0,0,0]
    month = int(time.strftime('%m',time.localtime(time.time())))
    for i in xrange(0,4):
        tasks = k_maintenance.objects.filter(classid_id=parentid,state=i+1,mtype=mtype)
        stat[i] = len(tasks)
    tasks = k_maintenance.objects.filter(classid_id=parentid,state=4,mtype=mtype,auditdatetime__month=month)
    stat[4] = len(tasks)
    return stat