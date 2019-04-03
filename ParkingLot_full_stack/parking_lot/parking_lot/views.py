from django.http import JsonResponse
from .models import Coach, Student
import json
from mongoengine.queryset.visitor import Q
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import os
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from parking_lot.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL, BASE_DIR
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


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
			return HttpResponse('Req typle: ' + request.method + ', req data: ' +
				str(request.POST))
		elif request.content_type =='application/json':
			res = json.loads(str(request.body, encoding='utf-8'))
			return HttpResponse('Req typle: ' + request.method + ', req data: ' +
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
def page_not_found(request, exception):
	# 必须像在 setting 中设置 debug 为 False
	return HttpResponseRedirect('/404/404.html')


@login_required
@csrf_exempt
def add(request):
	"""
	使用 http 传输 post, 不安全
	"""
	if request.method == 'POST':
		res = request.POST
		target = res.get('target', '')
		mobile = int(res.get('mobile', 0))
		origin_mobile = int(res.get('origin_mobile', 0))
		cardId = res.get('cardId', '')
		name = res.get('name', '')
		sex = res.get('sex', 'male')
		password = res.get('password', 'changeme')
		origin_cardId = res.get('origin_cardId', '')
		# 这里有一个 json 后的 string 在 js 和 python 之间表达的类型不一致的问题
		# 可以用 json.loads 解决, 不过因为有 headphoto 所以会出问题, 可以尝试先把 headphoto 字段去掉再 loads
		update = res.get('update', False)
		if update == 'true':
			update = True
		else:
			update = False
		if cardId == '':
			# ERROR
			return JsonResponse({'code': 2, 'msg': 'nfc 卡号不能为空/0!'})
		if mobile == 0:
			# ERROR
			return JsonResponse({'code': 2, 'msg': '手机号不能为空/0!'})
		if target == 'coach':
			exists = False
			if len(Coach.objects(cardId=cardId)) > 0:
				if update:
					exists = True
					if ( origin_mobile != mobile and len(Coach.objects(mobile=mobile) ) > 0 ) or \
							( origin_cardId != cardId and len(Coach.objects(cardId=cardId)) > 0 ):
						return JsonResponse({'code': 4, 'msg': '要更改的cardId=' + cardId + 
						' 或者 mobile=' + str(mobile) + 
						' 在数据库中已经存在, 你可以通过查询界面进行修改'})	
				else:
					return JsonResponse({'code': 3, 'msg': 'cardId=' + cardId + 
						' 或者 mobile=' + str(mobile) + 
						' 已经存在, 你可以通过查询界面进行修改'})	
			if exists:
				if len(request.FILES) > 0:
					f = request.FILES['headphoto']
					with open(os.path.join(BASE_DIR, 'media', 'headphotos', 'coach', f.name), 'wb+') as dst:
						for chunk in f.chunks():
							dst.write(chunk)
					headphoto = f.name
					Coach._get_collection().find_one_and_update({'cardId': origin_cardId}, {'$set': \
							{'mobile': mobile, 'name': name, 'sex': sex, 'cardId': cardId, 'password': password,\
							'headphoto': headphoto}})
				else:
					Coach._get_collection().find_one_and_update({'cardId': origin_cardId}, {'$set': \
							{'mobile': mobile, 'name': name, 'sex': sex, 'cardId': cardId, 'password': password}})
				return JsonResponse({'code': 0, 'msg': '更新教练成功!'})
			coach = Coach(mobile=mobile, name=name, sex=sex, cardId=cardId, password=password)
			if len(request.FILES) > 0:
				f = request.FILES['headphoto']
				with open(os.path.join(BASE_DIR, 'media', 'headphotos', 'coach', f.name), 'wb+') as dst:
					for chunk in f.chunks():
						dst.write(chunk)
				coach.headphoto = f.name
			coach.save()
			return JsonResponse({'code': 0, 'msg': '添加教练成功!'})
		elif target == 'student':
			height = res.get('height', 0)
			weight = res.get('weight', 0)
			# TODO: 默认值
			f1 = res.get('f1', 20)
			x1 = res.get('x1', 150)
			f2 = res.get('f2', 20)
			x2 = res.get('x2', 150)
			f3 = res.get('f3', 20)
			x3 = res.get('x3', 150)
			f4 = res.get('f4', 20)
			x4 = res.get('x4', 150)
			xmin = res.get('xmin', 80)
			xmax = res.get('xmax', 150)
			exists = False
			if len(Student.objects(cardId=origin_cardId)) > 0:
				if update:
					exists = True
					if ( origin_mobile != mobile and len(Student.objects(mobile=mobile) ) > 0 ) or \
							( origin_cardId != cardId and len(Student.objects(cardId=cardId)) > 0 ):
						return JsonResponse({'code': 4, 'msg': '要更改的cardId=' + cardId + 
						' 或者 mobile=' + str(mobile) + 
						' 在数据库中已经存在, 你可以通过查询界面进行修改'})	
				else:
					return JsonResponse({'code': 3, 'msg': 'cardId=' + cardId + 
						' 已经存在, 你可以通过查询界面进行修改'})
			# 因为 save 的时候执行的 update 的所有元素的 update, 并不能做到 pairial, 要
			# 做到 partial update, 使用 pymongo 的 Student._get_collection()
			if exists:
				if len(request.FILES) > 0:
					f = request.FILES['headphoto']
					with open(os.path.join(BASE_DIR, 'media', 'headphotos', 'student', f.name), 'wb+') as dst:
						for chunk in f.chunks():
							dst.write(chunk)
					headphoto = f.name
					Student._get_collection().find_one_and_update({'cardId': origin_cardId}, {'$set': \
						{'mobile': mobile, 'name': name, 'sex': sex, 'cardId': cardId, 'password': password,\
						'headphoto': headphoto, 'height': height, 'weight': weight, 'x_min': xmin, \
						'x_max': xmax, 'f1': f1, 'x1': x1, 'f2': f2, 'x2': x2, 'f3': f3, 'x3': x3, 'f4': f4, 'x4': x4}})
				else:
					Student._get_collection().find_one_and_update({'cardId': origin_cardId}, {'$set': \
						{'mobile': mobile, 'name': name, 'sex': sex, 'cardId': cardId, 'password': password, \
						'height': height, 'weight': weight, 'x_min': xmin, \
						'x_max': xmax, 'f1': f1, 'x1': x1, 'f2': f2, 'x2': x2, 'f3': f3, 'x3': x3, 'f4': f4, 'x4': x4}})
				return JsonResponse({'code': 0, 'msg': '更新学员成功!'})
			stu = Student(mobile=mobile, name=name, sex=sex, cardId=cardId, password=password, \
										height=height, weight=weight, x_min=xmin, \
										x_max=xmax, f1=f1, x1=x1, f2=f2, x2=x2, f3=f3, x3=x3, f4=f4, x4=x4)
			
			if len(request.FILES) > 0:
				f = request.FILES['headphoto']
				with open(os.path.join(BASE_DIR, 'media', 'headphotos', 'student', f.name), 'wb+') as dst:
					for chunk in f.chunks():
						dst.write(chunk)
				stu.headphoto = f.name
			stu.save()
			return JsonResponse({'code': 0, 'msg': '添加学员成功!'})
	else:
		return HttpResponseForbidden()

@csrf_exempt
def search(request):
	"""
	使用 http 传输 post, 不安全
	"""
	if request.method == 'POST':
		res = json.loads(str(request.body, encoding='utf-8'))
		# coach / student
		target = res.get('target', '')
		# cardId / mobile
		query_type = res.get('type', '')
		cardId = res.get('cardId', '')
		mobile = res.get('mobile', 0)
		if target == '' or query_type == '':
			# ERROR
			return JsonResponse({'code': 1, 'msg': '请指定查询的对象和类型, ' + 
				'target: student/coach, type: cardId/mobile'})
		elif target == 'coach':
			if query_type == 'cardId' and cardId != '':
				coach = Coach.objects(cardId=cardId)
				if len(coach) == 0:
					return JsonResponse({'code': 3, 'msg': '指定的 NFC 卡号 ' + cardId + 
						' 查无此人'})
				else:
					coach = coach[0]
					return JsonResponse({'code': 0, 'data': {'name': coach.name, 
						'sex': coach.sex, 'cardId': coach.cardId, 'mobile': coach.mobile, 
						'password': coach.password,
						'headphoto': '/media/headphotos/coach/' + coach.headphoto}})
			elif query_type == 'mobile' and mobile != 0:
				coach = Coach.objects(mobile=mobile)
				if len(coach) == 0:
					return JsonResponse({'code': 3, 'msg': '指定的手机号 ' + str(mobile) + 
						' 查无此人'})
				else:
					coach = coach[0]
					return JsonResponse({'code': 0, 'data': {'name': coach.name, 
						'sex': coach.sex, 'cardId': coach.cardId, 'mobile': coach.mobile,
						'password': coach.password,
						'headphoto': '/media/headphotos/coach/' + coach.headphoto}})
			else:
				return JsonResponse({'code': 1, 'msg': 'cardId=' + cardId + ', mobile=' 
					+ str(mobile) + ' 在 query_type=' + query_type + ' 下有一个为空!'})
		elif target == 'student':
			if query_type == 'cardId' and cardId != '':
				stu = Student.objects(cardId=cardId)
				if len(stu) == 0:
					return JsonResponse({'code': 3, 'msg': '指定的 NFC 卡号 ' + cardId + 
						' 查无此人'})
				else:
					stu = stu[0]
					return JsonResponse({'code': 0, 'data': {'name': stu.name, 'sex': stu.sex,
						'cardId': stu.cardId, 'mobile': stu.mobile, 'password': stu.password,
						'headphoto': '/media/headphotos/student/' + stu.headphoto, 'height': stu.height,
						'weight': stu.weight, 'xmin': stu.x_min, 'xmax': stu.x_max, 'f1': stu.f1, 'x1': stu.x1,
						'f2': stu.f2, 'x2': stu.x2, 'f3': stu.f3, 'x3': stu.x3, 'f4': stu.f4, 'x4': stu.x4}})
			elif query_type == 'mobile' and mobile != 0:
				stu = Student.objects(mobile=mobile)
				if len(stu) == 0:
					return JsonResponse({'code': 3, 'msg': '指定的手机号 ' + str(mobile) + 
						' 查无此人'})
				else:
					stu = stu[0]
					return JsonResponse({'code': 0, 'data': {'name': stu.name, 'sex': stu.sex,
						'cardId': stu.cardId, 'mobile': stu.mobile, 'password': stu.password,
						'headphoto': '/media/headphotos/student/' + stu.headphoto, 'height': stu.height,
						'weight': stu.weight, 'xmin': stu.x_min, 'xmax': stu.x_max, 'f1': stu.f1, 'x1': stu.x1,
						'f2': stu.f2, 'x2': stu.x2, 'f3': stu.f3, 'x3': stu.x3, 'f4': stu.f4, 'x4': stu.x4}})
			else:
				return JsonResponse({'code': 1, 'msg': 'cardId=' + cardId + ', mobile=' 
					+ str(mobile) + ' 在 query_type=' + query_type + ' 下有一个为空!'})
	else:
		return HttpResponseForbidden()
