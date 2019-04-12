from django.http import JsonResponse
# from .models import Coach, Student
import json
# from mongoengine.queryset.visitor import Q
from django.views.decorators.csrf import csrf_exempt
import logging
# import os
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from parking_lot.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
# from parking_lot.settings import BASE_DIR
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


@login_required
@csrf_exempt
def logout_handler(request):
    """
    退出登录
    """
    if request.method == 'GET':
        logout(request)
        return redirect(LOGOUT_REDIRECT_URL)
    else:
        return HttpResponseForbidden()


@login_required
@csrf_exempt
def admin_logout(req):
    """
    停车场管理系统的 admin 界面的登出
    """
    if req.method == 'POST':
        logout(req)
        # 都是成功
        return JsonResponse({
            'code': 20000,
            'data': 'success'
        })
    else:
        return HttpResponseForbidden()


@csrf_exempt
def debug_url(request):
    """
    debug
    """
    if request.method == 'GET':
        return HttpResponse('Req typle: ' + request.method + ', req data: ' +
                            str(request.GET))
    elif request.method == 'POST':
        if request.content_type == 'application/x-www-form-urlencoded':
            return HttpResponse('Req typle: ' + request.method +
                                ', req data: ' + str(request.POST))
        elif request.content_type == 'application/json':
            # res = json.loads(str(request.body, encoding='utf-8'))
            return HttpResponse('Req typle: ' + request.method +
                                ', req data: ' +
                                str(request.body, encoding='utf-8'))


@csrf_exempt
def log_state(request):
    """
    确认是否已经登录
    """
    if request.method == 'GET':
        return JsonResponse({'result': request.user.is_authenticated})
    else:
        return HttpResponseForbidden()


@csrf_exempt
def login_handler(request):
    """
    自定义登录
    """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
        else:
            # invalid login
            return HttpResponse('账号或密码错误, 请返回并重新登录!')
    else:
        return HttpResponseForbidden()


@csrf_exempt
def admin_login(req):
    """
    admin 界面的登录处理(不是 Django 的 admin 界面)
    """
    if req.method == 'POST':
        post = json.loads(req.body)
        username = post.get('username', '')
        password = post.get('password', '')
        user = authenticate(req, username=username, password=password)
        print('debug:', username, password, user)
        # TODO: 暂时只接受 admin 用户的登录
        if user is not None and username == 'admin':
            login(req, user)
            return JsonResponse({'code': 20000, 'data': 'admin-token'})
        else:
            # invalid login
            return JsonResponse({'code': 60204,
                                 'message': '账号或者密码错误, 必须以 admin 登录'})
    else:
        return HttpResponseForbidden()


@csrf_exempt
@login_required
def admin_info(req):
    if req.method == 'GET':
        print(req.COOKIES)
        token = req.COOKIES.get("Admin-Token", None)
        # TODO: 暂时只支持 admin
        if token:
            # TODO: 更多数据库有关信息
            return JsonResponse({'code': 20000, 'data': {
                'roles': ['admin'],
                'introduction': '停车场管理系统超级管理员',
                # 'avatar': 'https://example.com/res.jpg',
                'name': '超级管理员'}
                                 })
        else:
            return JsonResponse({
                'code': 50008,
                'message': '登录失败, 无法获取用户信息'
            })
    else:
        return HttpResponseForbidden()


@csrf_exempt
def page_not_found(request, exception):
    # 必须像在 setting 中设置 debug 为 False
    return HttpResponseRedirect('/404/404.html')
