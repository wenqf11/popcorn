# -*- encoding=UTF-8 -*-
__author__ = 'SYB'

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import *
from models import *
from datetime import date, datetime, time, timedelta
import json


# wrapper that require the request to be GET type
def get_required(func):
    def checker(request):
        if not request.GET:
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
        if not request.POST:
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
def token_required(request_type):
    def wrapper(func):
        def checker(request):
            body = request.GET if request_type == 'GET' else request.POST
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
    return wrapper


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

    if user.password == para['password']:
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'hello_world;'
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'wrong password'
        }))


@post_required
@token_required('POST')
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

    user.password = para['new_password']
    user.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'password changed'
    }))


@get_required
@token_required('GET')
def app_userinfo(request, para, user):
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': {
            'username': user.username,
            'name': user.name,
            'department': user.classid.name,
            'state': user.state,
            'gender': user.gender,
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


@get_required
@token_required('GET')
def app_score(request, para, user):
    try:
        score = k_staffscoreinfo.objects.get(userid=user.id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'score not exist for this user'
        }))

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': int(score.score)
    }))


@get_required
@token_required('GET')
def app_route(request, para, user):
    schedules = k_schedule.objects.filter(user=user, date=date.today())
    if not schedules.exists():
        return HttpResponse(json.dumps({
            'status': 'empty',
            'data': []
        }))

    routes = [_s.route for _s in schedules]
    response = {
        'status': 'ok',
        'data': [{'id': _r.id, 'name': _r.name, 'start_time': _r.starttime.strftime('%H:%M'), 'interval': _r.period, 'checked': 0} for _r in routes]
    }
    return HttpResponse(json.dumps(response))


@get_required
@token_required('GET')
def app_form(request, para, user):
    try:
        route = k_route.objects.get(id=int(request.GET.get('route_id')))
    except Exception:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'route not exists'
        }))

    if route.formid:
        forms = [k_form.objects.get(id=int(_r)) for _r in route.formid.split(',')]
    else:
        forms = []

    response = {
        'status': 'ok',
        'data': [{'id': _f.id, 'name': _f.brief, 'form_content': _f.content} for _f in forms]
    }
    return HttpResponse(json.dumps(response))


@get_required
@token_required('GET')
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
@token_required('POST')
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
@token_required('GET')
def app_maintain_list_1(request, para, user):
    tasks = k_maintenance.objects.filter(
        mtype=1,
        assignorid=user.id,
        state__range=(2, 3)
    )

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': [{
            'id': task.id,
            'title': task.title,
            'device_name': task.deviceid.name,
            'device_brief': task.deviceid.brief,
            'creator': k_user.objects.get(id=task.creatorid).name,
            'create_time': task.createdatetime.strftime('%Y-%m-%d %H:%M:%S'),
            'description': task.createcontent,
            'image': task.image,
            'memo': task.memo,
            'confirmed': (task.state == 3),
            'note': task.editcontent
        } for task in tasks]
    }))


@get_required
@token_required('GET')
def app_maintain_list_2(request, para, user):
    tasks = k_maintenance.objects.filter(
        mtype=2,
        assignorid=user.id,
        state__range=(2, 3)
    )

    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': [{
            'id': task.id,
            'title': task.title,
            'device_name': task.deviceid.name,
            'device_brief': task.deviceid.brief,
            'creator': k_user.objects.get(id=task.creatorid).name,
            'create_time': task.createdatetime.strftime('%Y-%m-%d %H:%M:%S'),
            'description': task.createcontent,
            'image': task.image,
            'memo': task.memo,
            'confirmed': (task.state == 3),
            'note': task.editcontent
        } for task in tasks]
    }))


@post_required
@token_required('POST')
def app_maintain_add(request, para, user):
    para['device_brief'] = int(request.POST.get('device_brief'))
    para['title'] = request.POST.get('title')
    para['description'] = request.POST.get('description')
    para['image'] = request.POST.get('image')
    para['memo'] = request.POST.get('memo')

    try:
        device = k_device.objects.get(brief=para['device_brief'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'device not exist'
        }))

    task = k_maintenance.objects.create(deviceid=device)
    task.state = 1
    task.title = para['title']
    task.createcontent = para['description']
    task.image = para['image']
    task.memo = para['memo']
    task.mtype = 2
    task.creatorid = user.id
    task.createdatetime = datetime.now()

    task.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'maintain task added'
    }))


@post_required
@token_required('POST')
def app_maintain_confirm(request, para, user):
    para['maintain_id'] = int(request.POST.get('maintain_id'))

    try:
        task = k_maintenance.objects.get(id=para['maintain_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not exist'
        }))

    if task.state == 3:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'already confirmed'
        }))
    else:
        task.state = 3
        task.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'maintain task confirmed'
        }))


@post_required
@token_required('POST')
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

    if task.state == 2:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not confirmed yet'
        }))
    else:
        task.note = para['note']
        task.save()
        return HttpResponse(json.dumps({
            'status': 'ok',
            'data': 'maintain task updated'
        }))


@post_required
@token_required('POST')
def app_maintain_submit(request, para, user):
    para['maintain_id'] = int(request.POST.get('maintain_id'))

    try:
        task = k_maintenance.objects.get(id=para['maintain_id'])
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            'status': 'error',
            'data': 'maintain task not exist'
        }))

    task.state = 4
    task.save()
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': 'maintain task submitted'
    }))


