from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from topic.models import Topic, Topic_Members, Diary

from account.views import login_required
from book.views import admin_required


@csrf_exempt
def get_topic_by_id(request):
    """
    接受get请求，返回话题信息
    :param request:
    :param topic_id:
    :return:
    """
    if request.method == 'GET':
        topic_id = request.GET.get('topic_id')
        curr_topic = Topic.objects.get(id=topic_id)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': curr_topic.to_dict()})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
def get_all_topics(request):
    """
    接受get请求，返回所有话题信息,并按热度排序
    :param request:
    :return:
    """
    if request.method == 'GET':
        all_topics = sorted(Topic.objects.all(), key=lambda topic: topic.topic_heat, reverse=True)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [topic.to_dict() for topic in all_topics]})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
@login_required
def join_topic(request):
    '''
    接受post请求，加入话题
    :param request:
    :param topic_id:
    :return:
    '''
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        curr_topic = Topic.objects.get(id=topic_id)
        if Topic_Members.objects.filter(user_id=request.session.get('user_id'), topic_id=topic_id).exists():
            return JsonResponse({'errno': 2, "msg": "You have already joined the group."})
        curr_topic.topic_num_members += 1
        Topic_Members.objects.create(user_id=request.session.get('user_id'), topic_id=topic_id)
        # save what we have done
        curr_topic.save()
        return JsonResponse({'errno': 0, "msg": "You have joined the group_app."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
def get_all_topics_by_user(request):
    """
    接受get请求，返回当前用户关注的所有话题
    :param request:
    :param user_id:
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        topic_ids = Topic_Members.objects.filter(user_id=user_id).values_list('topic_id', flat=True)
        topics = Topic.objects.filter(id__in=topic_ids)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [topic.to_dict() for topic in topics]})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
@login_required
def leave_topic(request):
    """
    接受post请求，退出话题
    :param request:
    :param topic_id:
    :return:
    """
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        curr_topic = Topic.objects.get(id=topic_id)
        if not Topic_Members.objects.filter(user_id=request.session.get('user_id'), topic_id=topic_id).exists():
            return JsonResponse({'errno': 2, "msg": "You have already left the group."})
        curr_topic.topic_num_members -= 1
        Topic_Members.objects.filter(user_id=request.session.get('user_id'), topic_id=topic_id).delete()
        # save what we have done
        curr_topic.save()
        return JsonResponse({'errno': 0, "msg": "You have left the group_app."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@admin_required
def create_topic(request):
    """
    接受post请求，创建话题
    :param request:
    :return:
    error_code:
        0: success
        1: only post method is allowed
        2: topic name cannot be empty
        3: topic name too long
        4: topic name already exists
        5: topic description too long
    """
    if request.method == 'POST':
        topic_name = request.POST.get('topic_name')
        if not topic_name or topic_name == '':
            return JsonResponse({'errno': 2, "msg": "Topic name can't be empty."})
        if len(topic_name) > 200:
            return JsonResponse({'errno': 3, "msg": "Topic name is too long."})
        if Topic.objects.filter(topic_name=topic_name).exists():
            return JsonResponse({'errno': 4, "msg": "The topic_name has already existed."})
        topic_description = request.POST.get('topic_description')
        if len(topic_description) > 200:
            return JsonResponse({'errno': 5, "msg": "The topic_description is too long."})
        topic_num_members = 0
        topic_heat = 0
        Topic.objects.create(topic_name=topic_name, topic_description=topic_description,
                             topic_num_members=topic_num_members, topic_heat=topic_heat)
        return JsonResponse({'errno': 0, "msg": "You have created a new group_app."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
def write_diary(request):
    """
    接受post请求，发送日记
    :param request:
    :param topic_id:
    :return:
    error code:
    0: success
    1: only post method is allowed
    2: you have not joined the group
    3: the diary title can't be empty
    4: the diary title is too long
    5: the diary can't be empty
    """
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        user_id = request.session.get('user_id')
        if not Topic_Members.objects.filter(user_id=user_id, topic_id=topic_id).exists():
            return JsonResponse({'errno': 2, "msg": "You have not joined the topic."})
        diary_title = request.POST.get('diary_title')
        if not diary_title or diary_title == '':
            return JsonResponse({'errno': 3, "msg": "Diary title can't be empty."})
        if len(diary_title) > 200:
            return JsonResponse({'errno': 4, "msg": "Diary title is too long."})
        diary_content = request.POST.get('diary_content')
        if not diary_content or diary_content == '':
            return JsonResponse({'errno': 5, "msg": "Diary content can't be empty."})
        Diary.objects.create(topic_id=topic_id, diary_title=diary_title, diary_content=diary_content)
        return JsonResponse({'errno': 0, "msg": "You have sent a new diary."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
def like_diary(request):
    """
    接受post请求，点赞日记
    :param request:
    :param diary_id:
    :return:
    """
    if request.method == 'POST':
        diary_id = request.POST.get('diary_id')
        curr_diary = Diary.objects.get(id=diary_id)
        curr_diary.likes += 1
        curr_diary.save()
        return JsonResponse({'errno': 0, "msg": "You have liked the diary."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
def dislike_diary(request):
    """
    接受post请求，点赞日记
    :param request:
    :param diary_id:
    :return:
    """
    if request.method == 'POST':
        diary_id = request.POST.get('diary_id')
        curr_diary = Diary.objects.get(id=diary_id)
        curr_diary.dislikes += 1
        curr_diary.save()
        return JsonResponse({'errno': 0, "msg": "You have disliked the diary."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
def get_all_diary_by_heat(request):
    """
    接受get请求，获取话题下的所有日记
    :param request:
    :param topic_id:
    :return:
    """
    if request.method == 'GET':
        topic_id = request.GET.get('topic_id')
        diaries = Diary.objects.filter(topic_id=topic_id)
        diaries = diaries.order_by('-diary_heat')
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [diary.to_dict() for diary in diaries]})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
def get_all_diary_by_time(request):
    """
    接受get请求，获取话题下的所有日记
    :param request:
    :param topic_id:
    :return:
    """
    if request.method == 'GET':
        topic_id = request.GET.get('topic_id')
        diaries = Diary.objects.filter(topic_id=topic_id)
        diaries = diaries.order_by('-diary_create_time')
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [diary.to_dict() for diary in diaries]})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
def get_diary_by_author_id(request):
    """
    接受get请求，获取当前作者所写的所有日记
    :param request:
    :param diary_id:
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        diaries = Diary.objects.filter(diary_authorId=user_id)
        diaries = diaries.order_by('-diary_create_time')
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [diary.to_dict() for diary in diaries]})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
def get_diary_by_id(request):
    """
    接受get请求，获取指定日记
    :param request:
    :param diary_id:
    :return:
    """
    if request.method == 'GET':
        diary_id = request.GET.get('diary_id')
        diary = Diary.objects.get(id=diary_id)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': diary.to_dict()})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


@csrf_exempt
def diary_heat_add(request):
    """
    接受post请求，对应的日记的热度加一
    :param request:
    :param diary_id:
    :return:
    """
    if request.method == 'POST':
        diary_id = request.POST.get('diary_id')
        diary = Diary.objects.get(id=diary_id)
        diary.diary_heat += 1
        diary.save()
        return JsonResponse({'errno': 0, "msg": "You have liked the diary."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
def topic_heat_add(request):
    """
    接受post请求，对应的话题的热度加一
    :param request:
    :param topic_id:
    :return:
    """
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        topic.topic_heat += 1
        topic.save()
        return JsonResponse({'errno': 0, "msg": "You have liked the topic."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
def get_topic_info_by_key(request):
    """
    取得指定屬性同時包含指定關鍵詞的信息对应话题信息, 只接受GET請求, Params格式為:
    ?屬性名=關鍵詞[&...]
    :param request: WSGIRequest
    :return: JsonResponse
    """

    def __search(__info, obj):
        for key in [key for key in __info if __info[key] is not None and __info[key] != '']:
            if __info[key] not in obj.__dict__[key]:
                return False
        return True

<<<<<<< HEAD
=======

>>>>>>> 05614248f12656d946c15de7e2219c368a29ad6f
    if request.method == 'GET':
        info = {
            'topic_name': request.GET.get('topic_name'),
            'topic_description': request.GET.get('topic_description'),
            'topic_num_members': request.GET.get('topic_num_members'),
            'topic_heat': request.GET.get('topic_heat'),
            'topic_create_date': request.GET.get('topic_create_date'),
        }
        if not any(info.values()):
            return JsonResponse({'errno': 2, 'msg': '必填字段為空'})
        topics = list(filter(lambda x: __search(info, x), Topic.objects.all()))
        if len(topics) == 0:
            return JsonResponse({'errno': 3, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), topics))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_topic_info(request):
    """
    根據關鍵字進行模糊搜索, 每個關鍵字之間使用','分割\n
    只要滿足屬性中同時包含所有關鍵字的書籍都會被選出\n
    如果提供的keyword為空則默認返回所有書籍的信息\n
    只接受GET請求, Params格式為:\n
    ?keyword=value1[,value2,...]
    :param request: WSGIRequest
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

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword is None or keyword == '':
            return JsonResponse(
                {'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), Topic.objects.all()))}
            )
        keywords = str(keyword).split(',')
        topics = list(filter(lambda x: __search(keywords, x), Topic.objects.all()))
        if len(topics) == 0:
            return JsonResponse({'errno': 2, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), topics))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_diary_info_by_key(request):
    """
    取得指定屬性同時包含指定關鍵詞的信息对应话题信息, 只接受GET請求, Params格式為:
    ?屬性名=關鍵詞[&...]
    :param request: WSGIRequest
    :return: JsonResponse
    """

    def __search(__info, obj):
        for key in [key for key in __info if __info[key] is not None and __info[key] != '']:
            if __info[key] not in obj.__dict__[key]:
                return False
        return True

<<<<<<< HEAD
=======

>>>>>>> 05614248f12656d946c15de7e2219c368a29ad6f
    if request.method == 'GET':
        info = {
            'diary_title': request.GET.get('diary_title'),
            'diary_content': request.GET.get('diary_content'),
            'diary_create_time': request.GET.get('diary_create_time'),
            'diary_heat': request.GET.get('diary_heat'),
            'diary_authorId': request.GET.get('diary_authorId'),
            'likes': request.GET.get('likes'),
            'dislikes': request.GET.get('dislikes'),
            'diary_num_comments': request.GET.get('diary_num_comments'),
        }
        if not any(info.values()):
            return JsonResponse({'errno': 2, 'msg': '必填字段為空'})
        diaries = list(filter(lambda x: __search(info, x), Diary.objects.all()))
        if len(diaries) == 0:
            return JsonResponse({'errno': 3, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), diaries))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_diary_info(request):
    """
    根據關鍵字進行模糊搜索, 每個關鍵字之間使用','分割\n
    只要滿足屬性中同時包含所有關鍵字的書籍都會被選出\n
    如果提供的keyword為空則默認返回所有書籍的信息\n
    只接受GET請求, Params格式為:\n
    ?keyword=value1[,value2,...]
    :param request: WSGIRequest
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

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword is None or keyword == '':
            return JsonResponse(
                {'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), Diary.objects.all()))}
            )
        keywords = str(keyword).split(',')
        diaries = list(filter(lambda x: __search(keywords, x), Diary.objects.all()))
        if len(diaries) == 0:
            return JsonResponse({'errno': 2, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), diaries))})
    else:
<<<<<<< HEAD
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})
=======
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})
>>>>>>> 05614248f12656d946c15de7e2219c368a29ad6f
