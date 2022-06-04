from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import *
import re

# Create your views here.

"""
調用方法:
    前端發送GET或POST請求到/account/函數名, 並添加相應的Params或Body(data使用鍵值對形式), 即可獲得包含相應信息的響應返回
errno:
    0:      [成功]
    901:    請求方式錯誤, 只接受POST請求
    902:    兩次輸入的密碼不一致
    903:    用戶名不合法
    904:    用戶名已存在
    905:    密碼不合法
    906:    用戶不存在
    907:    Email不合法
    908:    手機號碼不合法
    909:    城市或地址不合法
    910:    原密碼錯誤
    911:    必填字段為空
    912:    用戶未登入
    913:    重複登入
    914:    密碼錯誤
    915:    年齡不合法
    916:    請求方式錯誤, 只接受GET請求
"""


def __check_user_info(username, password_1, password_2, email, phone, age, city, address, skip_check_duplicates=False):
    """
    檢查用戶資訊是否合法, 並返回錯誤代碼和jsonResponse, 合法返回0, 否則返回-1, 私有函數, 不可在外部調用, 此函數可忽略

    :param username: str
    :param password_1: str
    :param password_2: str
    :param email: str
    :param phone: str
    :param age: str
    :param city: str
    :param address: str
    :param skip_check_duplicates: bool = False
    :return: tuple(code: int, msg: JsonResponse | None)
    """
    if username is None or password_1 is None or password_2 is None or email is None or \
            len(str(username)) == 0 or len(str(password_1)) == 0 or len(str(password_2)) == 0 or len(str(email)) == 0:
        return -1, JsonResponse({'errno': 911, 'msg': '必填字段為空'})
    try:
        if skip_check_duplicates:
            raise User.DoesNotExist()
        _ = User.objects.get(username=username)
        return -1, JsonResponse({'errno': 904, 'msg': '用戶名已存在'})
    except User.DoesNotExist:
        if re.match('.*\\W+.*', str(username)) is not None or len(str(username)) > 30:
            return -1, JsonResponse({'errno': 903, 'msg': '用戶名不合法'})
        elif password_1 != password_2:
            return -1, JsonResponse({'errno': 902, 'msg': '兩次輸入的密碼不一致'})
        elif len(str(password_1)) < 8 or len(str(password_1)) > 18 or \
                re.match('.*\\d+.*', str(password_1)) is None or \
                re.match('.*[a-zA-Z]+.*', str(password_1)) is None:
            return -1, JsonResponse({'errno': 905, 'msg': '密碼不合法'})
        elif len(str(email)) > 254 or re.match('[\\w.]+@[\\w.]+', str(email)) is None:
            return -1, JsonResponse({'errno': 907, 'msg': 'Email不合法'})
        elif phone != '' and phone is not None and \
                (len(str(phone)) != 11 or re.match('.*\\D+.*', str(phone)) is not None):
            return -1, JsonResponse({'errno': 908, 'msg': '手機號碼不合法'})
        elif age != '' and age is not None and (int(age) < 0 or int(age) > 150):
            return -1, JsonResponse({'errno': 915, 'msg': '年齡不合法'})
        elif (city != '' and city is not None and len(str(city)) > 50) or \
                (address != '' and address is not None and len(str(address)) > 100):
            return -1, JsonResponse({'errno': 909, 'msg': '城市或地址不合法'})
        else:
            return 0, None


@csrf_exempt
def register(request):
    """
    注册用户, 只接受POST請求, Body所需的字段為:\n
    **# 必填項**\n
    'username': 用戶名\n
    'password_1': 密碼\n
    'password_2': 密碼確認\n
    'email': Email\n
    **# 非必填項**\n
    'phone': 手機號碼\n
    'age': 年齡\n
    'city': 城市\n
    'address': 地址\n
    'introduction': 簡介

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        city = request.POST.get('city')
        address = request.POST.get('address')
        introduction = request.POST.get('introduction')
        code, msg = __check_user_info(username, password_1, password_2, email, phone, age, city, address)
        if code < 0:
            return msg
        new_user = User(
            username=username,
            password=password_1,
            email=email,
            phone=phone if phone is not None else '',
            age=age,
            city=city if city is not None else '',
            address=address if address is not None else '',
            introduction=introduction if introduction is not None else ''
        )
        new_user.save()
        return JsonResponse({'errno': 0, 'msg': '註冊成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤, 只接受POST請求'})


@csrf_exempt
def login(request):
    """
    用户登录, 只接受POST請求, Body所需的字段為:\n
    'username': 用戶名\n
    'password': 密碼

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if len(str(username)) == 0 or len(str(password)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必填字段為空'})
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                if request.session.get('user_id') is not None:
                    return JsonResponse({'errno': 913, 'msg': '重複登入'})
                request.session['user_id'] = user.user_id
                return JsonResponse({'errno': 0, 'msg': '登入成功'})
            else:
                return JsonResponse({'errno': 914, 'msg': '密碼錯誤'})
        except User.DoesNotExist:
            return JsonResponse({'errno': 906, 'msg': '用戶不存在'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤, 只接受POST請求'})


@csrf_exempt
def logout(request):
    """
    用户登出, 只接受POST請求, Body為空

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'POST':
        if request.session.get('user_id') is None:
            return JsonResponse({'errno': 912, 'msg': '用戶未登入'})
        request.session.flush()
        return JsonResponse({'errno': 0, 'msg': '註銷成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤, 只接受POST請求'})


@csrf_exempt
def get_user_info_by_username(request):
    """
    根据用户名获取用户信息, 只接受GET請求, Params格式為:\n
    ?username=要查詢的用戶名

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'GET':
        username = request.GET.get('username')
        if len(str(username)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必填字段為空'})
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': user.to_dict()})
        except User.DoesNotExist:
            return JsonResponse({'errno': 906, 'msg': '用戶不存在'})
    else:
        return JsonResponse({'errno': 916, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_user_info_by_user_id(request):
    """
    根据用户ID获取用户信息, 只接受GET請求, Params格式為:\n
    ?user_id=要查詢的用戶ID

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if len(str(user_id)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必填字段為空'})
        try:
            user = User.objects.get(user_id=user_id)
            return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': user.to_dict()})
        except User.DoesNotExist:
            return JsonResponse({'errno': 906, 'msg': '用戶不存在'})
    else:
        return JsonResponse({'errno': 916, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_user_info(request):
    """
    获取用户信息, 只接受GET請求, Params為空

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.session.get('user_id') is None:
        return JsonResponse({'errno': 912, 'msg': '用戶未登入'})
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': user.to_dict()})
        except User.DoesNotExist:
            return JsonResponse({'errno': 906, 'msg': '用戶不存在'})
    else:
        return JsonResponse({'errno': 916, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def update_user_info(request):
    """
    更新目前登入的用户信息, 只接受POST請求, Body所需的字段為:\n
    **# 以下所有的字段都是非必填的, 要改哪個填哪個**\n
    'username': 用戶名\n
    'is_admin': 是否為管理員\n
    'is_banned': 是否被封禁\n
    'email': 電子郵件\n
    'phone': 電話號碼\n
    'age': 年齡\n
    'city': 城市\n
    'address': 地址\n
    'introduction': 簡介

    **# 需要注意的是如需修改密碼需要提供原密碼且正確才能修改**\n
    **# 如果需要修改密碼, 則必填以下項**\n
    'old_password': 原密碼\n
    'password_1': 新密碼\n
    'password_2': 確認新密碼

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.session.get('user_id') is None:
        return JsonResponse({'errno': 912, 'msg': '用戶未登入'})
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        info = {
            'username': request.POST.get('username'),
            'is_admin': request.POST.get('is_admin'),
            'is_banned': request.POST.get('is_banned'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'address': request.POST.get('address'),
            'introduction': request.POST.get('introduction')
        }
        old_password = request.POST.get('old_password')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        user = User.objects.get(user_id=user_id)
        for key in info:
            if len(str(info[key])) == 0 or info[key] is None:
                info[key] = user.__dict__[key]
        if old_password is not None and old_password != '':
            if user.password != old_password:
                return JsonResponse({'errno': 910, 'msg': '原密碼錯誤'})
            else:
                code, msg = __check_user_info(
                    info['username'],
                    password_1,
                    password_2,
                    info['email'],
                    info['phone'],
                    info['age'],
                    info['city'],
                    info['address'],
                    skip_check_duplicates=True
                )
                if code < 0:
                    return msg
                User.objects.filter(user_id=user_id).update(
                    username=info['username'],
                    password=password_1,
                    is_admin=info['is_admin'],
                    is_banned=info['is_banned'],
                    email=info['email'],
                    phone=info['phone'],
                    age=info['age'],
                    city=info['city'],
                    address=info['address'],
                    introduction=info['introduction']
                )
                return JsonResponse({'errno': 0, 'msg': '更新成功'})
        else:
            code, msg = __check_user_info(
                info['username'],
                user.password,
                user.password,
                info['email'],
                info['phone'],
                info['age'],
                info['city'],
                info['address'],
                skip_check_duplicates=True
            )
            if code < 0:
                return msg
            User.objects.filter(user_id=user_id).update(
                username=info['username'],
                is_admin=info['is_admin'],
                is_banned=info['is_banned'],
                email=info['email'],
                phone=info['phone'],
                age=info['age'],
                city=info['city'],
                address=info['address'],
                introduction=info['introduction']
            )
            return JsonResponse({'errno': 0, 'msg': '更新成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤, 只接受POST請求'})
