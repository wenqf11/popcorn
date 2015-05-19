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
                    'data': 'unknown token error'
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
    schedules = k_schedule.objects.filter(user=user.id, date=date.today())
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

    forms = [k_form.objects.get(id=int(_r)) for _r in route.formid.split(',')]
    response = {
        'status': 'ok',
        'data': [{'id': _f.id, 'name': _f.brief, 'form_content': _f.content} for _f in forms]
    }
    return HttpResponse(json.dumps(response))


