from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from account.models import User
from book.models import Book
from comment.models import Comment, Report
from account.views import login_required
from book.views import admin_required
from group.models import Group, Post
from movie.models import Movie
from topic.models import Diary


@csrf_exempt
# @login_required
def send_comment(request):
    """
    接受post请求，将评论信息存入数据库
    :param body_type:
    :param request:
    :param body_id:
    error_code:
        0: success
        1: only post request is allowed
        2: body_type error
        3: content is empty
    """
    global Comment, title
    if request.method == 'POST':
        body_type = request.POST.get('body_type')
        body_id = request.POST.get('body_id')
        content = request.POST.get('content')
        if content == '' or not content:
            return JsonResponse({'errno': '3', 'msg': 'content is empty'})
        authorId = request.session.get('user_id')
        # param type 1 for book 2 for movie 3 for post 4 for diary
        body_type = int(body_type)
        # param body_id for the body that this comment belongs to
        body_id = int(body_id)
        if body_type == 1:
            book = Book.objects.get(ISBN=body_id)
            book.book_num_comments += 1
            title = request.POST.get('title')
            if title == '' or not title:
                return JsonResponse({'errno': '3', 'msg': 'title is empty'})
            if len(content) < 25:
                return JsonResponse({'errno': '3', 'msg': 'content is too short'})
            book.save()
        elif body_type == 2:
            movie = Movie.objects.get(movie_id=body_id)
            movie.movie_num_comments += 1
            title = request.POST.get('title')
            if title == '' or not title:
                return JsonResponse({'errno': '3', 'msg': 'title is empty'})
            if len(content) < 25:
                return JsonResponse({'errno': '3', 'msg': 'content is too short'})
            movie.save()
        elif body_type == 3:
            from group.models import Post
            post = Post.objects.get(id=body_id)
            post.post_num_comments += 1
            post.save()
        elif body_type == 4:
            from topic.models import Diary
            diary = Diary.objects.get(id=body_id)
            diary.diary_num_comments += 1
            diary.save()
        elif body_type == 5:
            from comment.models import Comment
            comment = Comment.objects.get(id=body_id)
            comment.comment_num_comments += 1
            comment.save()
        else:
            return JsonResponse({'errno': 2, "msg": "Invalid type."})
        if body_type == 1 or body_type == 2:
            curr_comment = Comment(title=title, content=content, authorId=authorId, type=body_type, body_id=body_id)
        else:
            curr_comment = Comment(content=content, authorId=authorId, type=body_type, body_id=body_id)
        curr_comment.save()
        return JsonResponse({'errno': 0, "msg": "You have sent a new comment."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
def get_all_comments(request):
    """
    接受get请求，返回评论信息
    :param type:
    :param request:
    :param body_id:
    """
    if request.method == 'GET':
        body_id = request.GET.get('body_id')

        all_comments = Comment.objects.filter(body_id=body_id).order_by('-num_likes')
        data = []
        for comment in all_comments:
            if comment.type == 1:
                _ = comment.to_dict()
                _['book_info'] = Book.objects.get(ISBN=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                data.append(_)
            elif comment.type == 2:
                _ = comment.to_dict()
                _['movie_info'] = Movie.objects.get(movie_id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                data.append(_)
            elif comment.type == 3:
                _ = comment.to_dict()
                _['post_info'] = Post.objects.get(id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                data.append(_)
            elif comment.type == 4:
                _ = comment.to_dict()
                _['diary_info'] = Diary.objects.get(id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                data.append(_)
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': data})


@csrf_exempt
@login_required
@admin_required
def remove_comment(request):
    """
    接受post请求，将评论删除
    :param request:
    :param comment_id:
    """
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'errno': 0, "msg": "You have removed a comment."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


# like a comment
@csrf_exempt
@login_required
def like_comment(request):
    """
    接受post请求，将评论点赞数加1
    :param request:
    :param comment_id:
    """
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.num_likes += 1
        comment.save()
        return JsonResponse({'errno': 0, "msg": "You have liked a comment."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
def dislike_comment(request):
    """
    接受post请求，将评论踩数加1
    :param request:
    :param comment_id:
    """
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.num_dislikes += 1
        comment.save()
        return JsonResponse({'errno': 0, "msg": "You have disliked a comment."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
def report_comment(request):
    """
    接受post请求，将评论举报
    :param request:
    :param comment_id:
    """
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        report_title = request.POST.get('report_title')
        if report_title == '' or not report_title:
            return JsonResponse({'errno': 2, "msg": "Report title is empty."})
        reason = request.POST.get('reason')
        if reason == '' or not reason:
            return JsonResponse({'errno': '2', 'msg': 'reason is empty'})
        if len(reason) < 15:
            return JsonResponse({'errno': '3', 'msg': 'reason is too short'})
        # add a new report to the database
        report = Report(comment_id=comment_id, title=report_title, reason=reason,
                        reporter_id=request.session.get('user_id'))

        report.save()
        return JsonResponse({'errno': 0, "msg": "You have reported a comment."})
    else:
        return JsonResponse({'errno': 1, "msg": "Only POST method is allowed."})


@csrf_exempt
@login_required
@admin_required
def show_report(request):
    """
    接受get请求，返回举报信息
    :param request:
    """
    if request.method == 'GET':
        reports = Report.objects.all()
        # sort by time
        reports = reports.order_by('-date')
        return JsonResponse({'errno': 0, 'msg': 'success', 'data': list(map(lambda x: x.to_dict(), reports))})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


def get_comments_by_type(request):
    """
    接受get请求，返回评论信息
    :param type:
    :param request:
    :param body_id:
    """
    if request.method == 'GET':
        body_type = request.GET.get('body_type')
        all_comments = Comment.objects.filter(type=body_type).order_by('-num_likes')
        result = []
        if all_comments is None:
            return JsonResponse({'errno': 0, 'msg': 'success', 'data': []})

        if int(body_type) == 1:
            for comment in all_comments:
                _ = comment.to_dict()
                _['book_info'] = Book.objects.get(ISBN=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                result.append(_)
            # books = Book.objects.filter(ISBN__in=[comment.body_id for comment in all_comments])
            # for i in range(len(books)):
            #     book = [books[i].to_dict()]
            #     comment = [all_comments[i].to_dict()]
            #     result.append(book + comment)
            return JsonResponse({'errno': 0, 'msg': 'success', 'data': result})

        elif int(body_type) == 2:
            for comment in all_comments:
                _ = comment.to_dict()
                _['movie_info'] = Movie.objects.get(movie_id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                result.append(_)
            # movies = Movie.objects.filter(movie_id__in=[comment.body_id for comment in all_comments])
            # for i in range(len(all_comments)):
            #     movie = [movies[i].to_dict]
            #     comment = [all_comments[i].to_dict()]
            #     result.append(movie + comment)
            return JsonResponse({'errno': 0, 'msg': 'success', 'data': result})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})


def get_comments_by_heat(request):
    """
    接受get请求，返回评论信息
    :param type:
    :param request:
    :param body_id:
    """
    global t
    if request.method == 'GET':
        all_comments = Comment.objects.order_by('-num_likes')
        # 遍历 all_comments
        # 如果评论的点赞数大于0，则将评论加入到热门评论中
        bodies = []
        for comment in all_comments:
            if comment.type == 1:
                _ = comment.to_dict()
                _['book_info'] = Book.objects.get(ISBN=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                bodies.append(_)
            elif comment.type == 2:
                _ = comment.to_dict()
                _['movie_info'] = Movie.objects.get(movie_id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                bodies.append(_)
            elif comment.type == 3:
                _ = comment.to_dict()
                _['post_info'] = Post.objects.get(id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                bodies.append(_)
            elif comment.type == 4:
                _ = comment.to_dict()
                _['diary_info'] = Diary.objects.get(id=comment.body_id).to_dict()
                _['user_info'] = User.objects.get(user_id=comment.authorId).to_dict()
                bodies.append(_)

        return JsonResponse({'errno': 0, 'msg': 'success', 'data': bodies})
    else:
        return JsonResponse({'errno': 1, "msg": "Only GET method is allowed."})