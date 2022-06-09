from datetime import datetime

from django.contrib.messages.storage import session
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from group.models import Group, Post, Group_Members
from account.views import login_required
from book.views import admin_required


@csrf_exempt
def get_group_by_id(request):
    """
    返回给定的小组id对应的组的信息
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        all_groups = Group.objects.all()
        for group in all_groups:
            if group.id == group_id:
                curr_group = group
                break
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': curr_group.to_dict()})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


@csrf_exempt
def get_all_groups(request):
    """
    返回所有的小组信息，并将小组按照热度排序
    :param request:
    :return:
    """
    if request.method == 'GET':
        all_groups = Group.objects.all()
        all_groups = sorted(all_groups, key=lambda group: group.group_heat, reverse=True)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [group.to_dict() for group in all_groups]})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


# join a group_app by the group_app id
@csrf_exempt
@login_required
def join_group(request):
    """
    接受Post请求，将当前用户加入给定的小组
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        curr_group = Group.objects.get(id=group_id)
        # if the user_id and group_id already exist in the Group_Members table,
        # then the user has already joined the group_app
        if Group_Members.objects.filter(user_id=request.session.get('user_id'), group_id=group_id).exists():
            return JsonResponse({'errno': 2, 'msg': 'You have already joined this group.'})
        curr_group.group_num_members += 1
        Group_Members.objects.create(group_id=curr_group, user_id=request.session.get('user_id'))
        # save what we have done
        curr_group.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


# leave a group_app we have joined by the group_app id
@csrf_exempt
@login_required
def leave_group(request):
    """
    将当前用户从给定的小组中移除
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        curr_group = Group.objects.get(id=group_id)
        if not Group_Members.objects.filter(user_id=request.session.get('user_id'), group_id=group_id).exists():
            return JsonResponse({'errno': 2, 'msg': 'You have not joined this group.'})
        curr_group.group_num_members -= 1
        curr_group.save()
        Group_Members.objects.filter(user_id=request.session.get('user_id'), group_id=group_id).delete()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


# create a group_app by the group_app name and description
@csrf_exempt
@login_required
def create_group(request):
    """
    接受Post请求，创建一个小组,创建者为管理员
    :param request:
    :return:
    error code:
    0: success
    1: only POST method is allowed
    2: group name too long
    3: group name is empty
    4: group name already exists
    5: group description too long
    6: group picture is empty
    """
    if request.method == 'POST':
        group_name = request.POST['group_name']

        if len(group_name) > 200:
            return JsonResponse({'errno': 2, 'msg': 'Group name is too long.'})

        if not group_name or group_name == '':
            return JsonResponse({'errno': 3, 'msg': 'Group name is empty.'})

        if Group.objects.filter(group_name=group_name).exists():
            return JsonResponse({'errno': 4, 'msg': 'Group name already exists.'})

        group_description = request.POST['group_description']
        if len(group_description) > 200:
            return JsonResponse({'errno': 5, 'msg': 'Group description is too long.'})
        group_rules = request.POST['group_rules']

        group_picture_url = request.POST['group_picture_url']
        if group_picture_url == '' or not group_picture_url:
            return JsonResponse({'errno': 6, 'msg': 'Group picture url is empty.'})

        # current user is one of the admins of the group
        group = Group(group_name=group_name, group_description=group_description, group_rules=group_rules,
                      group_picture_url=group_picture_url, group_num_members=1)

        Group_Members.objects.create(group_id=group.id, user_id=request.session.get('user_id'), is_admin=True)
        # save what we have done to the database
        group.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


# a function return all the groups that the user has joined
@csrf_exempt
@login_required
def get_groups_by_user(request):
    """
    接受Get请求，返回所有当前用户加入的小组
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        # get all the group_id that the user has joined
        group_ids = Group_Members.objects.filter(user_id=user_id).values_list('group_id', flat=True)
        # get all the groups that id in the group_ids
        groups = Group.objects.filter(id__in=group_ids)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [group.to_dict() for group in groups]})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


# a function to send a post to a group_app if the user is in the group_app
@csrf_exempt
def get_post_by_id(request):
    """
    接受Get请求，返回给定帖子id对应的帖子的详细信息
    :param request:
    :param group_id:
    :param post_id:
    :return:
    """
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': post.to_dict()})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


@csrf_exempt
@login_required
def send_post(request):
    """
    接受Post请求，发送一个帖子到给定的小组
    :param request:
    :param group_id:
    :return:
    error code:
    0: success
    1: only POST method is allowed
    2: you are not in the group
    3: post title is empty
    4: post title is too long
    5: post content is empty
    """
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        curr_group = Group.objects.get(id=group_id)
        # if the user_id and group_id already exists in the Group_Members table, then send the post
        if Group_Members.objects.filter(user_id=request.session.get('user_id'), group_id=group_id).exists():
            group_id = curr_group.id
            post_title = request.POST['post_title']
            if post_title == '' or not post_title:
                return JsonResponse({'errno': 3, 'msg': 'Post title is empty.'})
            if len(post_title) > 200:
                return JsonResponse({'errno': 4, 'msg': 'Post title is too long.'})
            post_content = request.POST['post_content']
            if post_content == '' or not post_content:
                return JsonResponse({'errno': 5, 'msg': 'Post content is empty.'})
            post_author = request.session.get('user_id')
            post = Post(group_id=group_id, post_title=post_title, post_content=post_content,
                        post_authorId=post_author)
            post.save()
            curr_group.num_of_posts += 1
            return JsonResponse({'errno': 0, 'msg': 'success'})
        else:
            return JsonResponse({'errno': 2, 'msg': 'You are not in the group_app.'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


@csrf_exempt
@login_required
def remove_post(request):
    """
    接受Post请求，删除给定帖子
    :param request:
    :param post_id:
    :return:
    """
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        # get the group_app of the post
        curr_post = Post.objects.get(id=post_id)
        group_id = curr_post.group_id
        curr_group = Group.objects.get(id=group_id)
        # check if the user is the admin of the group or the author of the post
        if request.session.get('user_id') == curr_post.post_authorId or request.session.get(
                'user_id') in Group_Members.objects.filter(group_id=group_id, is_admin=True):
            curr_post.delete()
            curr_group.num_of_posts -= 1
            curr_group.save()
            return JsonResponse({'errno': 0, 'msg': 'success'})
        else:
            return JsonResponse(
                {'errno': 2, 'msg': 'You are not the author of the post or the admin of the group_app.'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


@csrf_exempt
def get_posts_by_group_id(request):
    """
    接受Get请求，返回给定小组的所有帖子
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        curr_group = Group.objects.get(id=group_id)
        posts = curr_group.posts.all()
        posts = sorted(posts, key=lambda post: post.post_heat, reverse=True)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [post.to_dict() for post in posts]})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


# a function to remove a post by the post id if the user is the admin of the group_app or the author of the post


@csrf_exempt
@login_required
def get_posts_by_user(request):
    """
    接受Get请求，返回所有当前用户发布的帖子
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        posts = Post.objects.filter(post_authorId=user_id)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': [post.to_dict() for post in posts]})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


# like the post by the user
@csrf_exempt
@login_required
def like_post(request):
    """
    接受Post请求，给给定帖子点赞
    :param request:
    :param post_id:
    """
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        curr_post = Post.objects.get(id=post_id)
        curr_post.post_heat += 1
        curr_post.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


# dislike the post by the user
@csrf_exempt
@login_required
def dislike_post(request):
    """
    接受Post请求，给给定帖子点踩
    :param request:
    :param post_id:
    """
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        curr_post = Post.objects.get(id=post_id)
        curr_post.post_heat -= 1
        curr_post.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


@csrf_exempt
def get_post_by_id(request):
    """
    接受Get请求，返回给定帖子的详细信息
    :param request:
    :param post_id:
    :return:
    """
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        curr_post = Post.objects.get(id=post_id)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': curr_post.to_dict()})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only GET method is allowed.'})


@csrf_exempt
def group_heat_add(request):
    """
    接受Post请求，增加给定小组的热度
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        curr_group = Group.objects.get(id=group_id)
        curr_group.group_heat += 1
        curr_group.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


@csrf_exempt
def post_heat_add(request):
    """
    接受Post请求，增加给定帖子的热度
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        curr_post = Post.objects.get(id=post_id)
        curr_post.post_heat += 1
        curr_post.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
    else:
        return JsonResponse({'errno': 1, 'msg': 'Only POST method is allowed.'})


@csrf_exempt
def get_group_info_by_key(request):
    """
    取得指定屬性同時包含指定關鍵詞的信息的對應小组信息, 只接受GET請求, Params格式為:
    ?屬性名=關鍵詞[&...]
    :param request: WSGIRequest
    :return: JsonResponse
    """

    def __search(__info, obj):
        for key in [key for key in __info if __info[key] is not None and __info[key] != '']:
            if __info[key] not in obj.__dict__[key]:
                return False
        return True

    if request.method == 'GET':
        info = {
            'group_name': request.GET.get('group_name'),
            'group_description': request.GET.get('group_description'),
            'group_created_date': request.GET.get('group_created_date'),
            'group_num_members': request.GET.get('group_num_members'),
            'group_heat': request.GET.get('group_heat'),
            'group_rules': request.GET.get('group_rules'),
            'num_of_posts': request.GET.get('num_of_posts'),
        }
        if not any(info.values()):
            return JsonResponse({'errno': 2, 'msg': '必填字段為空'})
        groups = list(filter(lambda x: __search(info, x), Group.objects.all()))
        if len(groups) == 0:
            return JsonResponse({'errno': 3, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), groups))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_group_info(request):
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
                {'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), Group.objects.all()))}
            )
        keywords = str(keyword).split(',')
        groups = list(filter(lambda x: __search(keywords, x), Group.objects.all()))
        if len(groups) == 0:
            return JsonResponse({'errno': 2, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), groups))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})



@csrf_exempt
def get_post_info_by_key(request):
    """
    取得指定屬性同時包含指定關鍵詞的信息的對應小组信息, 只接受GET請求, Params格式為:
    ?屬性名=關鍵詞[&...]
    :param request: WSGIRequest
    :return: JsonResponse
    """

    def __search(__info, obj):
        for key in [key for key in __info if __info[key] is not None and __info[key] != '']:
            if __info[key] not in obj.__dict__[key]:
                return False
        return True


    if request.method == 'GET':
        info = {
            'group_id': request.GET.get('group_id'),
            'post_title': request.GET.get('post_title'),
            'post_content': request.GET.get('post_content'),
            'post_create_time': request.GET.get('post_create_time'),
            'post_heat': request.GET.get('post_heat'),
            'post_num_comments': request.GET.get('post_num_comments'),
            'post_authorId': request.GET.get('post_authorId'),
            'likes': request.GET.get('likes'),
            'dislikes': request.GET.get('dislikes'),
        }
        if not any(info.values()):
            return JsonResponse({'errno': 2, 'msg': '必填字段為空'})
        posts = list(filter(lambda x: __search(info, x), Post.objects.all()))
        if len(posts) == 0:
            return JsonResponse({'errno': 3, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), posts))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})


@csrf_exempt
def get_post_info(request):
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
                {'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), Post.objects.all()))}
            )
        keywords = str(keyword).split(',')
        posts = list(filter(lambda x: __search(keywords, x), Post.objects.all()))
        if len(posts) == 0:
            return JsonResponse({'errno': 2, 'msg': '找不到符合條件的結果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), posts))})
    else:
        return JsonResponse({'errno': 1, 'msg': '請求方式錯誤, 只接受GET請求'})