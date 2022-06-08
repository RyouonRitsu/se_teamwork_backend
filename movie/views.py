from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import User
from movie.models import *
from datetime import date
from account.views import login_required

# Create your views here.

"""
調用方法:
    前端發送GET或POST請求到/movie/函數名, 並添加相應的Params或Body(data使用鍵值對形式), 即可獲得包含相應信息的響應返回
errno:
    0:      [成功]
    901:    请求方式错误, 只接受POST请求
    902:    两次输入的密码不一致
    903:    用户名不合法
    904:    用户名已存在
    905:    密码不合法
    906:    用户不存在
    907:    Email不合法
    908:    手机号码不合法
    909:    城市或地址不合法
    910:    原密码错误
    911:    必填字段为空
    912:    用户未登录
    913:    重复登录
    914:    密码错误
    915:    年龄不合法
    916:    请求方式错误, 只接受GET请求
    917:    用户未登录, 且未提供任何可供查询的字段
    931:    ISBN已存在
    932:    ISBN过长
    933:    书名过长
    934:    排序字段不存在
    935:    书籍类型过长
    936:    作者姓名过长
    937:    作者国籍过长
    938:    出版社名过长
    939:    出版日期不合法
    940:    价格不合法
    941:    评分不合法
    942:    书籍不存在
    943:    热门度不合法
    944:    页数不合法
    945:    您没有权限执行此操作
    946:    找不到符合条件的结果
    961:    影视名过长
    962:    影视形式过长
    963:    影视类型过长
    964:    地区过长
    965:    上映日期不合法
    966:    导演名过长
    967:    编剧名过长
    968:    主演名过长
    969:    语言过长
    970:    片长不合法
"""


def __check_movie_info(movie_name, movie_form, movie_type, area, release_date, director, screenwriter, starring,
                       language, duration, score, heat):
    """
    檢查影视信息是否合法, 並返回錯誤代碼和jsonResponse, 合法返回0, 否則返回-1, 私有函數, 不可在外部調用, 此函數可忽略

    :param movie_name: str
    :param movie_form: str
    :param movie_type: str
    :param area: str
    :param release_date: str
    :param director: str
    :param screenwriter: str
    :param starring: str
    :param language: str
    :param duration: str
    :param score: str
    :param heat: str
    :return: tuple(code: int, msg: JsonResponse | None)
    """
    if not movie_name or not movie_type or not area or not release_date or not director or not screenwriter or \
            not starring or not language or movie_name == '' or movie_type == '' or area == '' or release_date == '' or \
            director == '' or screenwriter == '' or starring == '' or language == '':
        return -1, JsonResponse({'errno': 911, 'msg': '必填字段为空'})
    if len(str(movie_name)) > 100:
        return -1, JsonResponse({'errno': 961, 'msg': '影视名过长'})
    if movie_form and len(str(movie_form)) > 100:
        return -1, JsonResponse({'errno': 962, 'msg': '影视形式过长'})
    if len(str(movie_type)) > 50:
        return -1, JsonResponse({'errno': 963, 'msg': '影视类型过长'})
    if len(str(area)) > 100:
        return -1, JsonResponse({'errno': 964, 'msg': '地区过长'})
    try:
        date.fromisoformat(release_date)
    except ValueError:
        return -1, JsonResponse({'errno': 965, 'msg': '上映日期不合法'})
    if len(str(director)) > 100:
        return -1, JsonResponse({'errno': 966, 'msg': '导演名过长'})
    if len(str(screenwriter)) > 100:
        return -1, JsonResponse({'errno': 967, 'msg': '编剧名过长'})
    if len(str(starring)) > 100:
        return -1, JsonResponse({'errno': 968, 'msg': '主演名过长'})
    if len(str(language)) > 50:
        return -1, JsonResponse({'errno': 969, 'msg': '语言过长'})
    try:
        if duration and int(duration) <= 0:
            return -1, JsonResponse({'errno': 970, 'msg': '片长不合法'})
    except ValueError:
        return -1, JsonResponse({'errno': 970, 'msg': '片长不合法'})
    try:
        if score != '' and score is not None and (float(score) < 0 or float(score) > 10):
            return -1, JsonResponse({'errno': 941, 'msg': '评分不合法'})
    except ValueError:
        return -1, JsonResponse({'errno': 941, 'msg': '评分不合法'})
    try:
        if heat != '' and heat is not None and int(heat) < 0:
            return -1, JsonResponse({'errno': 943, 'msg': '热门度不合法'})
    except ValueError:
        return -1, JsonResponse({'errno': 943, 'msg': '热门度不合法'})
    return 0, None
