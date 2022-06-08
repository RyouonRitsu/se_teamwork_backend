from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from movie.models import *
from datetime import date
from account.views import login_required
from book.views import admin_required

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
    971:    影视不存在
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
            not starring or not language:
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
        if score and (float(score) < 0 or float(score) > 10):
            return -1, JsonResponse({'errno': 941, 'msg': '评分不合法'})
    except ValueError:
        return -1, JsonResponse({'errno': 941, 'msg': '评分不合法'})
    try:
        if heat and int(heat) < 0:
            return -1, JsonResponse({'errno': 943, 'msg': '热门度不合法'})
    except ValueError:
        return -1, JsonResponse({'errno': 943, 'msg': '热门度不合法'})
    return 0, None


@csrf_exempt
@login_required
@admin_required
def add_movie(request):
    """
    新增書籍, 只接受POST請求, Body所需的字段為:\n
    **# 必填項**\n
    'movie_name': 影视名\n
    'movie_type': 影视类型\n
    'area': 地区\n
    'release_date': 上映日期\n
    'director': 导演名\n
    'screenwriter': 编剧名\n
    'starring': 主演名\n
    'language': 语言\n
    **# 非必填項**\n
    'movie_cover': 影视封面文件\n
    'introduction': 影视简介\n
    'movie_form': 影视形式\n
    'duration': 片长\n
    'score': 评分\n
    'heat': 热门度

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method != 'POST':
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})
    movie_name = request.POST.get('movie_name')
    movie_cover = request.FILES.get('movie_cover')
    introduction = request.POST.get('introduction')
    movie_form = request.POST.get('movie_form')
    movie_type = request.POST.get('movie_type')
    area = request.POST.get('area')
    release_date = request.POST.get('release_date')
    director = request.POST.get('director')
    screenwriter = request.POST.get('screenwriter')
    starring = request.POST.get('starring')
    language = request.POST.get('language')
    duration = request.POST.get('duration')
    score = request.POST.get('score')
    heat = request.POST.get('heat')
    code, msg = __check_movie_info(movie_name, movie_form, movie_type, area, release_date, director, screenwriter,
                                   starring, language, duration, score, heat)
    if code < 0:
        return msg
    new_movie = Movie(
        movie_name=movie_name,
        movie_cover=movie_cover,
        introduction=introduction if introduction else '',
        movie_form=movie_form if movie_form else '',
        movie_type=movie_type,
        area=area,
        release_date=date.fromisoformat(release_date),
        director=director,
        screenwriter=screenwriter,
        starring=starring,
        language=language,
        duration=duration if duration else None,
        score=score if score else None
    )
    if heat:
        new_movie.heat = heat
    new_movie.save()
    return JsonResponse({'errno': 0, 'msg': '添加成功'})


@csrf_exempt
@login_required
@admin_required
def delete_movie(request):
    """
    刪除影视, 只接受POST請求, Body所需的字段為:\n
    **# 必填項**\n
    'movie_id': 影视ID

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method != 'POST':
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})
    movie_id = request.POST.get('movie_id')
    if not movie_id:
        return JsonResponse({'errno': 911, 'msg': '必填字段为空'})
    try:
        Movie.objects.get(movie_id=movie_id).delete()
        return JsonResponse({'errno': 0, 'msg': '刪除成功'})
    except Movie.DoesNotExist:
        return JsonResponse({'errno': 971, 'msg': '影视不存在'})


@csrf_exempt
@login_required
@admin_required
def update_movie_info(request):
    """
    更新指定movie_id的對應影视信息, 只接受POST請求, Body所需的字段為:\n
    'movie_id': 影视ID\n
    **# 以下所有的字段都是非必填的, 要改哪個填哪個**\n
    'movie_name': 影视名\n
    'movie_cover': 影视封面文件\n
    'introduction': 影视简介\n
    'movie_form': 影视形式\n
    'movie_type': 影视类型\n
    'area': 地区\n
    'release_date': 上映日期\n
    'director': 导演名\n
    'screenwriter': 编剧名\n
    'starring': 主演名\n
    'language': 语言\n
    'duration': 片长\n
    'score': 评分\n
    'heat': 热门度

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method != 'POST':
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})
    movie_id = request.POST.get('movie_id')
    if not movie_id:
        return JsonResponse({'errno': 911, 'msg': '必填字段为空'})
    try:
        movie = Movie.objects.get(movie_id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'errno': 971, 'msg': '影视不存在'})
    info = {
        'movie_name': request.POST.get('movie_name'),
        'introduction': request.POST.get('introduction'),
        'movie_form': request.POST.get('movie_form'),
        'movie_type': request.POST.get('movie_type'),
        'area': request.POST.get('area'),
        'release_date': request.POST.get('release_date'),
        'director': request.POST.get('director'),
        'screenwriter': request.POST.get('screenwriter'),
        'starring': request.POST.get('starring'),
        'language': request.POST.get('language'),
        'duration': request.POST.get('duration'),
        'score': request.POST.get('score'),
        'heat': request.POST.get('heat')
    }
    for key, value in info.items():
        if not value:
            info[key] = movie.__dict__[key]
    code, msg = __check_movie_info(info['movie_name'], info['movie_form'], info['movie_type'], info['area'],
                                   info['release_date'], info['director'], info['screenwriter'], info['starring'],
                                   info['language'], info['duration'], info['score'], info['heat'])
    if code < 0:
        return msg
    movie.movie_name = info['movie_name']
    movie_cover = request.FILES.get('movie_cover')
    if movie_cover:
        movie.movie_cover = movie_cover
    movie.introduction = info['introduction']
    movie.movie_form = info['movie_form']
    movie.movie_type = info['movie_type']
    movie.area = info['area']
    movie.release_date = date.fromisoformat(info['release_date'])
    movie.director = info['director']
    movie.screenwriter = info['screenwriter']
    movie.starring = info['starring']
    movie.language = info['language']
    movie.duration = info['duration']
    movie.score = info['score']
    movie.heat = info['heat']
    movie.save()
    return JsonResponse({'errno': 0, 'msg': '更新成功'})


@csrf_exempt
def get_movie_info_by_key(request, raw=False):
    """
    取得指定屬性同時包含指定關鍵詞的信息的對應影视信息, **可选** 根据关键字排序和选择升序降序(是否反转), 只接受GET請求, Params格式為:\n
    ?屬性名=關鍵詞[&...][&sort_by=屬性名&reverse=(True or False)]

    :param request: WSGIRequest
    :param raw: bool = False, 是否返回原始数据
    :return: JsonResponse
    """

    def __search(__info, obj):
        for key in [key for key in __info if __info[key] is not None and __info[key] != '']:
            if __info[key] not in obj.__dict__[key]:
                return False
        return True

    if request.method != 'GET':
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})
    info = {
        'movie_id': request.GET.get('movie_id'),
        'movie_name': request.GET.get('movie_name'),
        'introduction': request.GET.get('introduction'),
        'movie_form': request.GET.get('movie_form'),
        'movie_type': request.GET.get('movie_type'),
        'area': request.GET.get('area'),
        'release_date': request.GET.get('release_date'),
        'director': request.GET.get('director'),
        'screenwriter': request.GET.get('screenwriter'),
        'starring': request.GET.get('starring'),
        'language': request.GET.get('language'),
        'duration': request.GET.get('duration'),
        'score': request.GET.get('score'),
        'heat': request.GET.get('heat')
    }
    if not any(info.values()):
        if raw:
            return []
        return JsonResponse({'errno': 911, 'msg': '必填字段为空'})
    movies = list(filter(lambda x: __search(info, x), Movie.objects.all()))
    sort_by = request.GET.get('sort_by')
    reverse = request.GET.get('reverse')
    if sort_by:
        if sort_by not in Movie.__dict__:
            return JsonResponse({'errno': 934, 'msg': '排序字段不存在'})
        if reverse in ['True', 'true', 't', 'T', 'TRUE', '1', 'Yes', 'yes', 'YES', 'y', 'Y', '1']:
            reverse = True
        else:
            reverse = False
        movies.sort(key=lambda x: (x.__dict__[sort_by], x.score, x.movie_id), reverse=reverse)
    if raw:
        return list(map(lambda x: x.to_dict(), movies))
    if len(movies) == 0:
        return JsonResponse({'errno': 946, 'msg': '找不到符合条件的结果'})
    return JsonResponse({'errno': 0, 'msg': '查询成功', 'data': list(map(lambda x: x.to_dict(), movies))})


@csrf_exempt
def get_movie_info(request, raw=False):
    """
    根據關鍵字進行模糊搜索, 每個關鍵字之間使用','分割\n
    只要滿足屬性中同時包含所有關鍵字的影视都會被選出\n
    如果提供的keyword為空則默認返回所有影视的信息\n
    **可选** 根据关键字排序和选择升序降序(是否反转)\n
    只接受GET請求, Params格式為:\n
    ?keyword=value1[,value2,...][&sort_by=屬性名&reverse=(True or False)]

    :param request: WSGIRequest
    :param raw: bool = False, 是否返回原始数据
    :return: JsonResponse
    """

    def __search(__keywords, obj):
        _ = obj.to_dict()
        for key in _:
            for __keyword in __keywords:
                if __keyword not in str(_[key]):
                    break
            else:
                return True
        return False

    if request.method != 'GET':
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})
    keyword = request.GET.get('keyword')
    if not keyword:
        if raw:
            return list(map(lambda x: x.to_dict(), Movie.objects.all()))
        return JsonResponse(
            {'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), Movie.objects.all()))}
        )
    keywords = str(keyword).split(',')
    movies = list(filter(lambda x: __search(keywords, x), Movie.objects.all()))
    sort_by = request.GET.get('sort_by')
    reverse = request.GET.get('reverse')
    if sort_by:
        if sort_by not in Movie.__dict__:
            return JsonResponse({'errno': 934, 'msg': '排序字段不存在'})
        if reverse in ['True', 'true', 't', 'T', 'TRUE', '1', 'Yes', 'yes', 'YES', 'y', 'Y', '1']:
            reverse = True
        else:
            reverse = False
        movies.sort(key=lambda x: (x.__dict__[sort_by], x.score, x.movie_id), reverse=reverse)
    if raw:
        return list(map(lambda x: x.to_dict(), movies))
    if len(movies) == 0:
        return JsonResponse({'errno': 946, 'msg': '找不到符合条件的结果'})
    return JsonResponse({'errno': 0, 'msg': '查询成功', 'data': list(map(lambda x: x.to_dict(), movies))})


@csrf_exempt
def get_movie_info_by_id(request, raw=False):
    """
    取得指定movie_id的影视信息, 並為熱度值+1, 只接受GET請求, Params格式為:\n
    ?movie_id=要查询的影视ID

    :param request: WSGIRequest
    :param raw: bool = False, 是否返回原始数据
    :return: JsonResponse
    """
    if request.method != 'GET':
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})
    movie_id = request.GET.get('movie_id')
    if not movie_id:
        if raw:
            return []
        return JsonResponse({'errno': 911, 'msg': '必填字段为空'})
    try:
        movie = Movie.objects.get(movie_id=movie_id)
    except Movie.DoesNotExist:
        if raw:
            return []
        return JsonResponse({'errno': 946, 'msg': '找不到符合条件的结果'})
    movie.heat += 1
    movie.save()
    if raw:
        return [movie.to_dict()]
    return JsonResponse({'errno': 0, 'msg': '查询成功', 'data': [movie.to_dict()]})
