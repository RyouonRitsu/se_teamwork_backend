from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from publish.models import *
import re


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if len(str(username)) == 0 or len(str(password_1)) == 0 or len(str(password_2)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必填字段為空'})
        try:
            _ = User.objects.get(username=username)
            return JsonResponse({'errno': 904, 'msg': '用戶名已存在'})
        except User.DoesNotExist:
            if re.match('.*[^a-zA-Z\\d]+.*', str(username)) is not None:
                return JsonResponse({'errno': 903, 'msg': '用戶名不合法'})
            elif password_1 != password_2:
                return JsonResponse({'errno': 902, 'msg': '兩次輸入的密碼不同'})
            elif len(str(password_1)) < 8 or len(str(password_1)) > 18 or \
                    re.match('.*\\d+.*', str(password_1)) is None or \
                    re.match('.*[a-zA-Z]+.*', str(password_1)) is None:
                return JsonResponse({'errno': 905, 'msg': '密碼不合法'})
            else:
                new_author = User(username=username, password=password_1)
                new_author.save()
                return JsonResponse({'errno': 0, 'msg': '註冊成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if len(str(username)) == 0 or len(str(password)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必填字段為空'})
        try:
            author = User.objects.get(username=username)
            if author.password == password:
                request.session['username'] = username
                return JsonResponse({'errno': 0, 'msg': '登入成功'})
            else:
                return JsonResponse({'errno': 902, 'msg': '密碼錯誤'})
        except User.DoesNotExist:
            return JsonResponse({'errno': 906, 'msg': '用戶不存在'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤'})


@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'errno': 0, 'msg': '註銷成功'})
