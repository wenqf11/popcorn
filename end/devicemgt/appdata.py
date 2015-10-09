# -*- encoding=UTF-8 -*-
__author__ = 'SYB'

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import *
from models import *
from datetime import date, datetime, time, timedelta
from django.contrib.auth.hashers import make_password, check_password
import json, random


# wrapper that require the request to be GET type
def get_required(func):
    def checker(request):
        if not request.method == 'GET':
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'GET request required'
            }))
        else:
            return func(request)
    return checker


# wrapper that require the request to be POST type
def post_required(func):
    def checker(request):
        if not request.method == 'POST':
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'POST request required'
            }))
        else:
            return func(request)
    return checker


# wrapper that require correct token
# passing 'para'
# passing 'user'
def token_required(func):
    def checker(request):
        body = request.GET if request.method == 'GET' else request.POST
        para = {
            'username': body.get('username'),
            'token': body.get('access_token'),
            'timestamp': body.get('timestamp')
        }

        try:
            user = k_user.objects.get(username=para['username'])
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'user not exists'
            }))
        except Exception:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': "can't connect to database"
            }))

        # if not para['token'] == user.token
        if not para['token'] == 'hello_world':
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'unauthorized user'
            }))

        return func(request, user=user, para=para)
    return checker


# test view, a html page
def app_test(request):
    return render_to_response('apptest.html')


@get_required
def app_login(request):
    para = {
        'username': request.GET.get('username'),
        'password': request.GET.get('password'),
        'timestamp': request.GET.get('timestamp')
    }

    try:
        user = k_user.objects.get(username=para['username'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'user not exists'
        }))
    except Exception:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'unknown user query error'
        }))

    if check_password(para['password'], user.password):
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'hello_world'
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'wrong password'
        }))


@post_required
@token_required
def app_password(request, para, user):
    para['password'] = request.POST.get('password')
    para['new_password'] = request.POST.get('new_password')

    if not user.password == para['password']:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'wrong password'
        }))

    if not para['new_password']:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'new password required'
        }))

    user.password = make_password(para['new_password'])
    user.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'password changed'
    }))


@get_required
@token_required
def app_userinfo(request, para, user):
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': {
            'username': user.username,
            'name': user.name,
            'department': user.classid.name,
            'state': user.state,
            'gender': user.gender,
            'avatar': user.avatar.url,
            'mobile': user.mobile,
            'email': user.email,
            'address': user.address,
            'zipcode': user.zipcode,
            'birthday': user.birthday.strftime('%Y-%m-%d'),
            'id_card': user.idcard,
            'card_type': user.idcardtype,
            'content': user.content,
            'memo': user.memo,
            'contact': user.contact,
            'contact_mobile': user.contactmobile,
            'status': user.status,
            'todo': user.todo
        }
    }))


@post_required
@token_required
def app_userinfo_submit(request, para, user):
    _d = request.POST

    for _k in ['name', 'gender', 'mobile', 'email', 'address',
               'zipcode', 'id_card', 'memo', 'contact', 'contact_mobile']:
        if _k in _d:
            setattr(user, _k, _d[_k])

    if 'birthday' in _d:
        user.birthday = datetime.strptime(_d['birthday'], '%Y-%m-%d').date()

    user.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'user info modified'
    }))


@get_required
@token_required
def app_score(request, para, user):
    para['year'] = request.GET.get('year')
    para['month'] = request.GET.get('month')

    scores = k_staffscoreinfo.objects.filter(userid=user.id)

    if len(scores) == 0:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'score not exist for this user'
        }))

    score = -1
    for _s in scores:
        _y = _s.time.year
        _m = _s.time.month
        if str(_y) == para['year'] and str(_m) == para['month']:
            score = _s.score

    if score == -1:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'score not exist for this month'
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': int(score.score)
        }))


@get_required
@token_required
def app_score_rank(request, para, user):
    para['year'] = request.GET.get('year')
    para['month'] = request.GET.get('month')

    scores = k_staffscoreinfo.objects.filter(time__year=int(para['year']), time__month=int(para['month']))
    scores = scores.order_by('-score')

    result = [{'username': _s.userid.username, 'name': _s.userid.name, 'score': _s.score} for _s in scores]

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': result
    }))


@get_required
@token_required
def app_route(request, para, user):
	now_time = datetime.now().time()
	schedules = k_schedule.objects.filter(user=user,date=date.today())
	if not schedules.exists():
		return HttpResponse(json.dumps({
			'status': 'ok',
			'data': []
		}))

	routes = [_s.route for _s in schedules]
	return HttpResponse(json.dumps({
        'status': 'ok',
        'data': [{
                     'id': _r.id,
                     'name': _r.name,
                     'start_time': _r.starttime.strftime('%H:%M'),
                     'end_time':_r.endtime.strftime('%H:%M'),
                     'interval': _r.period,
                     'checked': 0
                 } for _r in routes if _r.starttime <= now_time and _r.endtime >= now_time]
    }))


@get_required
@token_required
def app_form(request, para, user):
    try:
        route = k_route.objects.get(id=int(request.GET.get('route_id')))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'route not exists'
        }))

    if route.formid:
        forms = [k_form.objects.get(id=int(_r)) for _r in route.formid.split(',')]
    else:
        forms = []

    for _f in forms:
        _items = k_formitem.objects.filter(formid=_f)
        _f.content = [{
            'name': _item.name,
            'choice': True,
            'choices': _item.choices.split('/'),
            'memo': _item.memo
        } if int(_item.datatype) == 1 else {
            'name': _item.name,
            'choice': False,
            'unit': _item.unit,
            'min': _item.lowerthreshold,
            'max': _item.upperthreshold,
            'memo': _item.memo
        } for _item in _items]

        _f.new_content = dict()
        for _item_id in xrange(0, len(_f.content)):
            c = _f.content[_item_id]
            _tmp_item = dict()
            _tmp_content = dict()
            _tmp_content["id"] = str(_item_id)
            _tmp_content["default"] = ""
            _tmp_content["priority"] = 0
            _tmp_content["max"] = c['max']
            _tmp_content["min"] = c['min']
            if c['choice']:
                _tmp_content["type"] = "integer"
                _tmp_content["options"] = dict()
                for i in xrange(0, len(c['choices'])):
                    _tmp_content["options"][str(i)] = c['choices'][i]
            else:
                _tmp_content["type"] = "integer"
                _tmp_content["hint"] = ""
                if c['min'] and not c['max']:
                    _tmp_content["hint"] = "正常值大于" + str(c['min'])
                if not c['min'] and c['max']:
                    _tmp_content["hint"] = "正常值小于" + str(c['max'])
                if c['min'] and c['max']:
                    _tmp_content["hint"] = "正常值在" + str(c['min']) + "和" + str(c['max']) + "之间"
            if c.has_key('unit') and c['unit']:
                _f.new_content[c['name']+" "+c['unit']] = _tmp_content
            else:
                _f.new_content[c['name']] = _tmp_content
            #_f.new_content.append(_tmp_item)
        #print _f.new_content
    response = {
        'status': 'ok',
        'data': [{'id': _f.id, 'name': _f.brief, 'content': json.dumps(_f.new_content)} for _f in forms]
    }
    return HttpResponse(json.dumps(response))


@post_required
@token_required
def app_meter(request, para, user):
    para['route'] = int(request.POST.get('route_id'))
    para['brief'] = request.POST.get('brief')
    para['content'] = request.POST.get('content')

    try:
        _route = k_route.objects.get(id=para['route'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            #'status': 'error',
            'status': 'ok',
            'data': 'route not exists'
        }))

    meter = k_meter(classid=_route.classid, brief=para['brief'], routeid=_route, userid=user, json=para['content'])
    meter.save()

    "记录积分"
    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)
    try:
        project = k_project.objects.get(classid=department_class)
    except ObjectDoesNotExist:
        project = k_project(
            classid=department_class,
            meterscore=2,
            maintenancescore=2,
            taskscore=2
        )
        project.save()
    staffscoreinfo = k_staffscoreinfo(
        userid=user,
        score=float(project.meterscore),
        content=str(project.meterscore) + ';无;任务',
        time=get_current_date()
    )
    staffscoreinfo.save()

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'meter data submitted'
    }))


@get_required
@token_required
def app_checkinfo(request, para, user):
    para['date'] = request.GET.get('date')
    d = datetime.strptime(para['date'], '%Y-%m-%d').date()

    info = k_staffworkinfo.objects.filter(
        userid=user,
        date=d
    )

    if len(info) == 0:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'work info not exist'
        }))
    elif not len(info) == 1:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'server db internal error'
        }))
    else:
        _info = info[0]
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': {
                'checkin': _info.checkin,
                'checkout': _info.checkout
            }
        }))


@post_required
@token_required
def app_check(request, para, user):
    para['date'] = request.POST.get('date')
    para['checkin'] = request.POST.get('checkin')
    para['checkout'] = request.POST.get('checkout')

    info = k_staffworkinfo.objects.filter(
        userid=user.id,
        date=para['date']
    )

    if len(info) == 1:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'check info existed'
        }))
    else:
        _info = k_staffworkinfo.objects.create(userid=user)
        _info.date = datetime.strptime(para['date'], '%Y-%m-%d').date()
        _info.checkin = para['checkin']
        _info.checkout = para['checkout']
        _info.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'check in success'
        }))


@get_required
@token_required
def app_maintain_list_1(request, para, user):
    tasks = k_maintenance.objects.filter(
        mtype='1',
        editorid=user.id,
        state__range=(2, 3)
    )

    data = [{
            'id': task.id,
            'title': task.title,
            'device_name': task.deviceid.name if task.deviceid else "",
            'device_brief': task.deviceid.brief if task.deviceid else "",
            'creator': k_user.objects.get(id=task.creatorid).name,
            'create_time': task.createdatetime.strftime('%Y-%m-%d %H:%M:%S'),
            'assignor': k_user.objects.get(id=task.assignorid).name,
            'description': task.createcontent,
            'memo': task.memo,
            'confirmed': (task.state == "3"),
            'note': task.editcontent
        } for task in tasks]
    sorted_data = sorted(data, key = lambda x:(x['note'], x['confirmed'])) 
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': sorted_data
    }))


@get_required
@token_required
def app_maintain_list_2(request, para, user):
    tasks = k_maintenance.objects.filter(
        mtype='2',
        editorid=user.id,
        state__range=(2, 3)
    )
    data = [{
            'id': task.id,
            'title': task.title,
            'device_name': task.deviceid.name if task.deviceid  else "",
            'device_brief': task.deviceid.brief if task.deviceid else "",
            'creator': k_user.objects.get(id=task.creatorid).name,
            'create_time': task.createdatetime.strftime('%Y-%m-%d %H:%M:%S'),
            'assignor': k_user.objects.get(id=task.assignorid).name,
            'description': task.createcontent,
            'image': task.image.url if task.image else '',
            'memo': task.memo,
            'confirmed': (task.state == "3"),
            'note': task.editcontent
        } for task in tasks]
    sorted_data = sorted(data, key = lambda x:(x['note'], x['confirmed'])) 
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': sorted_data
    }))


@post_required
@token_required
def app_maintain_add(request, para, user):
    para['device_brief'] = request.POST.get('device_brief')
    para['title'] = request.POST.get('title')
    para['description'] = request.POST.get('description')
    # para['image'] = request.POST.get('image')
    para['memo'] = request.POST.get('memo')

    task = k_maintenance()

    if para['device_brief']:
        try:
            device = k_device.objects.get(brief=para['device_brief'])
            task.deviceid = device
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({
                'status': 'error',
                'data': 'device not exist'
            }))
    task.state = '1'
    task.title = para['title']
    task.createcontent = para['description']
    # task.image = para['image']
    task.classid = user.classid
    task.memo = para['memo']
    task.mtype = '2'
    task.creatorid = user.id
    task.createdatetime = datetime.now()

    task.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': task.id
    }))


@post_required
@token_required
def app_maintain_confirm(request, para, user):
    para['maintain_id'] = int(request.POST.get('maintain_id'))

    try:
        task = k_maintenance.objects.get(id=para['maintain_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not exist'
        }))

    if task.state == '3':
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'already confirmed'
        }))
    else:
        task.state = '3'
        task.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'maintain task confirmed'
        }))


@post_required
@token_required
def app_maintain_update(request, para, user):
    para['maintain_id'] = int(request.POST.get('maintain_id'))
    para['note'] = request.POST.get('note')

    try:
        task = k_maintenance.objects.get(id=para['maintain_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not exist'
        }))

    if task.state == '2':
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not confirmed yet'
        }))
    else:
        task.editcontent = para['note']
        task.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'maintain task updated'
        }))


@post_required
@token_required
def app_maintain_submit(request, para, user):
    para['maintain_id'] = int(request.POST.get('maintain_id'))

    try:
        task = k_maintenance.objects.get(id=para['maintain_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not exist'
        }))

    task.state = '4'
    task.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'maintain task submitted'
    }))


@get_required
@token_required
def app_task_list(request, para, user):
    tasks = k_taskitem.objects.filter(
        editorid=user.id,
        state__range=(1, 2)
    )
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': [{
            'id': task.id,
            'title': task.title,
            'description': task.createcontent,
            'super_title': task.taskid.title,
            'super_description': task.taskid.createcontent,
            'creator': k_user.objects.get(id=task.creatorid).name,
            'create_time': task.createdatetime.strftime('%Y-%m-%d %H:%M:%S'),
            'memo': task.memo,
            'confirmed': (task.state == '2'),
            'note': task.editcontent
        } for task in tasks]
    }))


@post_required
@token_required
def app_task_confirm(request, para, user):
    para['task_id'] = int(request.POST.get('task_id'))

    try:
        task = k_taskitem.objects.get(id=para['task_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'taskitem not exists'
        }))

    if task.state == '2':
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'already confirmed'
        }))
    else:
        task.state = '2'
        task.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'task confirmed'
        }))


@post_required
@token_required
def app_task_update(request, para, user):
    para['task_id'] = int(request.POST.get('task_id'))
    para['note'] = request.POST.get('note')

    try:
        task = k_taskitem.objects.get(id=para['task_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'taskitem not exists'
        }))

    if task.state == '1':
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'task not confirmed yet'
        }))
    else:
        task.editcontent = para['note']
        task.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'task updated'
        }))


@post_required
@token_required
def app_task_submit(request, para, user):
    para['task_id'] = int(request.POST.get('task_id'))

    try:
        task = k_taskitem.objects.get(id=para['task_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'taskitem not exists'
        }))

    task.state = '3'
    task.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'task submitted'
    }))


@post_required
@token_required
def app_feedback(request, para, user):
    para['feedback'] = request.POST.get('feedback')

    _feedback = k_feedback.objects.create()

    _feedback.feedback = para['feedback']
    _feedback.creatorid = user.id
    _feedback.createdatetime = datetime.now()

    _feedback.save()

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'feedback created'
    }))


@get_required
@token_required
def app_device_brief(request, para, user):
    devices = k_device.objects.all()
    name_dict = dict()
    for _d in devices:
        name_dict[_d.brief] = _d.name
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': {
            'brief': [_d.brief for _d in devices],
            'dict': name_dict
            }
    }))


@get_required
@token_required
def app_device_info(request, para, user):
    para['device_brief'] = request.GET.get('device_brief')

    try:
        d = k_device.objects.get(brief=para['device_brief'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'device not exist'
        }))

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': {
            'id': d.id,
            'brief': d.brief,
            'name': d.name,
            'producer': d.producerid.name,
            'type': d.typeid.name,
            'serial': d.serial,
            'brand': d.brand,
            'model': d.model,
            'bought_time': d.buytime.strftime('%Y-%m-%d'),
            'location': d.position,
            'memo': d.memo
        }
    }))


def app_version(request):
    return render_to_response('version.xml',content_type="application/xml")


@get_required
@token_required
def app_egg_time(request, para, user):
    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)

    try:
        config = k_config.objects.get(classid=department_class)
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': {
                'bonus': config.eggbonus,
                'probability': config.eggprobability,
                'start_time': config.starttime.strftime('%H:%M'),
                'end_time': config.endtime.strftime('%H:%M')
            }
        }))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'bonus config does not found'
        }))


@get_required
@token_required
def app_egg(request, para, user):
    # query whether already tried to get an egg today
    egginfo = k_staffegginfo.objects.filter(userid=user, time=date.today())

    if egginfo.exists():
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'already tried today'
        }))


    department_class = user.classid
    while department_class.depth > 1:
        department_class = k_class.objects.get(id=department_class.parentid)

    try:
        config = k_config.objects.get(classid=department_class)
        number = random.random()

        # update staff egg info
        _info = k_staffegginfo.objects.create(
            userid=user,
            time=date.today(),
            bonus=config.eggbonus,
            probability=config.eggprobability,
            state=1 if config.eggprobability > number else 0
        )

        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': {
                'bonus': config.eggbonus,
                'probability': config.eggprobability,
                'result': config.eggprobability > number
            }
        }))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'bonus config does not found'
        }))


@get_required
@token_required
def app_egg_info(request, para, user):
    para['date'] = request.GET.get('date')

    _d = datetime.strptime(para['date'], '%Y-%m-%d').date()

    try:
        _info = k_staffegginfo.objects.get(userid=user, time=_d)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'element not exists'
        }))
    except MultipleObjectsReturned:
    	return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'multi bonus record found'
        }))

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': {
            'bonus': _info.bonus,
            'probability': _info.probability,
            'state': _info.state
        }
    }))


@post_required
@token_required
def app_avatar(request, para, user):
    _fs = request.FILES

    if _fs:
        user.avatar = _fs['avatar']
        user.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'avatar upload success'
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'avatar upload failed'
        }))


@post_required
@token_required
def app_maintain_image(request, para, user):
    para['id'] = int(request.POST.get('id'))
    try:
        _t = k_maintenance.objects.get(id=para['id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not exist'
        }))

    _fs = request.FILES

    if _fs:
        _t.image = _fs['image']
        _t.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'image upload success'
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'iamge upload failed'
        }))


@get_required
@token_required
def app_class_tree(request, para, user):
    def tree_traverse(parent_id, result):
        nodes = k_class.objects.filter(parentid=parent_id)
        if nodes.exists():
            result['children'] = [{
                'class_id': node.id,
                'type': node.depthname,
                'name': node.name
            } for node in nodes]
            depths = [tree_traverse(child['class_id'], child) for child in result['children']]
            return max(depths) + 1
        else:
            return 0

    try:
        root = k_class.objects.get(parentid=0)  # root node has parentid=0
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return HttpResponse(json.dump({
            'status': 'error',
            'data': 'illegal db data'
        }))

    tree = {'root': {'class_id': root.id, 'type': root.depthname, 'name': root.name}, 'depth': 1}

    tree['depth'] += tree_traverse(root.id, tree['root'])

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': tree
    }))


@get_required
@token_required
def app_class_device_type_classified(request, para, user):
    para['class_id'] = int(request.GET.get('class_id'))

    try:
        class_object = k_class.objects.get(id=para['class_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'class not exists'
        }))

    devices = k_device.objects.filter(classid=class_object)

    types = [d['typeid'] for d in devices.values('typeid').distinct()]

    result = []
    for t in types:
        device_type = k_devicetype.objects.get(id=t)
        type_devices = devices.filter(typeid=device_type)
        result.append({
            'type': device_type.name,
            'devices': [{'brief': d.brief, 'name': d.name} for d in type_devices]
        })

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': result
    }))


