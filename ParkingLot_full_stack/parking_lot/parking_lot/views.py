from django.http import JsonResponse
# from .models import Coach, Student
import json
# from mongoengine.queryset.visitor import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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
import db_pool.operations as operations

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
            return JsonResponse({'code': 20000, 'data': {
                'token': 'super_admin'
            }})
        elif user is not None:
            # TODO: 更好地利用 Django 的权限管理
            # TODO: 修改前后端的 token
            login(req, user)
            return JsonResponse({'code': 20000, 'data': {
                'token': 'outdoor_admin'
            }})
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
        token_admin = req.COOKIES.get("Admin-Token", None)
        if token_admin:
            # TODO: 更多数据库有关信息
            if token_admin == 'super_admin':
                return JsonResponse({'code': 20000, 'data': {
                    'roles': ['admin', ],
                    'name': '超级管理员',
                    'avatar': '',
                    'introduction': '停车场管理系统超级管理员',
                    # 'avatar': 'https://example.com/res.jpg
                }})
            elif token_admin == 'outdoor_admin':
                return JsonResponse({'code': 20000, 'data': {
                    'roles': ['editor', ],
                    'name': '出口管理员',
                    'avatar': '',
                    'introduction': '停车场出口管理员',
                }})
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


@csrf_exempt
def parking_lot_status_update(request):
    """
    停车场车位信息更新的 handler, 这是跟车位识别那边交互的接口
    只接受 POST 过来的 json
    """
    # DCMMC: 要不要考虑下安全问题?
    if request.method == 'POST' and request.content_type == 'application/json':
        # TODO
        # 规范:
        # {'code': 'updateParking', 'data': [{'parking_id_1': 'used'}, ...]}
        post = json.loads(request.body)
        # debug
        print('从车位识别得到的结果: {}'.format(json.dumps(post)))
        # TODO
        # 更新数据库之后, 向 parking_lot_realtime/consumers/ParkingLotStatusConsumer
        # 发送 group_send 事件
        try:
            for p in post['data']:
                operations.updateParking(parking_id=p.get('parking_id', None),
                                         used=p.get('used', None),
                                         addition_info=p.get(
                                             'addition_info', ''))
            res = operations.arrange_parkings_by_floor(post['data'])
            channel_layer = get_channel_layer()
            for f_id, f_data in res.items:
                async_to_sync(channel_layer.group_send)(
                    'status_{}'.format(f_id),
                    {
                        # 这个 type 是 Consumer 中的一个 Listen method
                        # 这个 group_send 就是向该 group 下所有 Consumers
                        # 发送一个以这个字典作为数据的 event 给 consumers
                        # 中 type 指定的 method, 注意: type 中的 `.` 会被
                        # 替换为 `_`
                        'type': 'update_parking',
                        # 后面的这些字段将会被 wrap 到 event
                        'message': json.dumps({
                            'code': 'updateParking',
                            'data': f_data
                        })
                    }
                )
            indoors = operations.getAllDoorIds(door_type='indoor')
            for i in indoors.get('data', []):
                async_to_sync(channel_layer.group_send)(
                    'indoor_'.format(i),
                    {
                        'type': 'send_recommand',
                        'message': {}
                    }
                )
            return {'code': 'success'}
        except Exception as e:
            return {'code': 'error', 'info': str(e)}
    else:
        return HttpResponseForbidden()


@csrf_exempt
def get_parkings_filter(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        post = json.loads(request.body)
        res = operations.getParkingsFilter(
            offset=post.get('offset', 0),
            parking_id=post.get('parking_id', ''),
            floor_id=post.get('floor_id', ''),
            region_id=post.get('region_id', ''),
            limit=post.get('limit', 20)
        )
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def update_parking(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        print('收到车位状态更新!')
        post = json.loads(request.body)
        res = operations.updateParking(
            parking_id=post.get('parking_id', None),
            addition_info=post.get('addition_info', ''),
            used=post.get('used', None),
            status=post.get('status', None))
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def add_vehicle(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        post = json.loads(request.body)
        license = post['license_plate']
        del post['license_plate']
        res = operations.addVehicle(license, **post)
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def rm_vehicle(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        post = json.loads(request.body)
        license = post['license_plate']
        res = operations.rmVehicle(license)
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def update_vehicle(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        post = json.loads(request.body)
        license = post['license_plate']
        del post['license_plate']
        res = operations.rmVehicle(license, **post)
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def get_vehicles_filter(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        post = json.loads(request.body)
        res = operations.getVehiclesFilter(**post)
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


@csrf_exempt
def get_bill_log_filter(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        post = json.loads(request.body)
        res = operations.getBillLogsFilter(**post)
        return JsonResponse(res)
    else:
        return HttpResponseForbidden()


