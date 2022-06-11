from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import User
from book.models import *
from datetime import date
from account.views import login_required

# Create your views here.

"""
調用方法:
    前端發送GET或POST請求到/book/函數名, 並添加相應的Params或Body(data使用鍵值對形式), 即可獲得包含相應信息的響應返回
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
    911:    必要信息缺失, 请检查后重新提交
    912:    用户未登录, 没有权限进行此操作
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
"""


def __check_book_info(isbn, book_name, book_cover, book_type, author, author_country, press, published_date,
                      page_number, price, score, heat, skip_check_duplicates=False):
    """
    檢查書籍信息是否合法, 並返回錯誤代碼和jsonResponse, 合法返回0, 否則返回-1, 私有函數, 不可在外部調用, 此函數可忽略

    :param isbn: str
    :param book_name: str
    :param book_cover: File
    :param book_type: str
    :param author: str
    :param author_country: str
    :param press: str
    :param published_date: str
    :param page_number: str
    :param price: str
    :param score: str
    :param heat: str
    :param skip_check_duplicates: bool = False
    :return: tuple(code: int, msg: JsonResponse | None)
    """
    if isbn is None or book_name is None is None or not book_cover or book_type is None or author is None or \
            press is None or published_date is None or price is None or len(str(isbn)) == 0 or \
            len(str(book_name)) == 0 or len(str(book_type)) == 0 or len(str(author)) == 0 or len(str(press)) == 0 or \
            len(str(published_date)) == 0 or len(str(price)) == 0:
        return -1, JsonResponse({'errno': 911, 'msg': '必要信息缺失, 请检查后重新提交'})
    try:
        if skip_check_duplicates:
            raise Book.DoesNotExist()
        _ = Book.objects.get(ISBN=isbn)
        return -1, JsonResponse({'errno': 931, 'msg': 'ISBN已存在'})
    except Book.DoesNotExist:
        if len(str(isbn)) > 20:
            return -1, JsonResponse({'errno': 932, 'msg': 'ISBN过长'})
        if len(str(book_name)) > 100:
            return -1, JsonResponse({'errno': 933, 'msg': '书名过长'})
        if len(str(book_type)) > 50:
            return -1, JsonResponse({'errno': 935, 'msg': '书籍类型过长'})
        if len(str(author)) > 50:
            return -1, JsonResponse({'errno': 936, 'msg': '作者姓名过长'})
        if author_country != '' and author_country is not None and len(str(author_country)) > 50:
            return -1, JsonResponse({'errno': 937, 'msg': '作者国籍过长'})
        if len(str(press)) > 50:
            return -1, JsonResponse({'errno': 938, 'msg': '出版社名过长'})
        try:
            date.fromisoformat(published_date)
        except ValueError:
            return -1, JsonResponse({'errno': 939, 'msg': '出版日期不合法'})
        try:
            if page_number != '' and page_number is not None and int(page_number) <= 0:
                return -1, JsonResponse({'errno': 944, 'msg': '页数不合法'})
        except ValueError:
            return -1, JsonResponse({'errno': 944, 'msg': '页数不合法'})
        try:
            if float(price) < 0:
                return -1, JsonResponse({'errno': 940, 'msg': '价格不合法'})
        except ValueError:
            return -1, JsonResponse({'errno': 940, 'msg': '价格不合法'})
        try:
            if score != '' and score is not None and (float(score) < 0 or float(score) > 5):
                return -1, JsonResponse({'errno': 941, 'msg': '评分不合法'})
        except ValueError:
            return -1, JsonResponse({'errno': 941, 'msg': '评分不合法'})
        try:
            if heat != '' and heat is not None and int(heat) < 0:
                return -1, JsonResponse({'errno': 943, 'msg': '热门度不合法'})
        except ValueError:
            return -1, JsonResponse({'errno': 943, 'msg': '热门度不合法'})
        return 0, None


def admin_required(func):
    """
    管理员权限验证装饰器
    """

    def wrapper(request, *args, **kwargs):
        user = User.objects.get(user_id=request.session.get('user_id'))
        if user.is_admin:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({'errno': 945, 'msg': '您没有权限执行此操作'})

    return wrapper


def save_to_frontend(path, file):
    """
    将文件保存到前端的静态文件目录

    :param path: str
    :param file: File
    """
    with open(f'{path}/{file.name}', 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)


@csrf_exempt
@login_required
@admin_required
def add_book(request):
    """
    新增書籍, 只接受POST請求, Body所需的字段為:\n
    **# 必填項**\n
    'ISBN': ISBN\n
    'book_name': 書名\n
    'book_cover': 封面文件\n
    'book_type': 書籍類型\n
    'author': 作者姓名\n
    'press': 出版社名\n
    'published_date': 出版日期(格式: YYYY-MM-DD)\n
    'price': 價格\n
    **# 非必填項**\n
    'introduction': 簡介\n
    'author_country': 作者國籍\n
    'page_number': 頁數\n
    'score': 評分\n
    'heat': 熱門度

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'POST':
        isbn = request.POST.get('ISBN')
        book_name = request.POST.get('book_name')
        book_cover = request.FILES.get('book_cover')
        introduction = request.POST.get('introduction')
        book_type = request.POST.get('book_type')
        author = request.POST.get('author')
        author_country = request.POST.get('author_country')
        press = request.POST.get('press')
        published_date = request.POST.get('published_date')
        page_number = request.POST.get('page_number')
        price = request.POST.get('price')
        score = request.POST.get('score')
        heat = request.POST.get('heat')
        code, msg = __check_book_info(
            isbn, book_name, book_cover, book_type, author, author_country, press, published_date, page_number, price,
            score, heat
        )
        if code < 0:
            return msg
        new_book = Book(
            ISBN=isbn,
            book_name=book_name,
            book_cover=book_cover,
            introduction=introduction if introduction is not None else '',
            book_type=book_type,
            author=author,
            author_country=author_country if author_country is not None else '',
            press=press,
            published_date=date.fromisoformat(published_date),
            page_number=page_number if page_number != '' else None,
            price=price,
            score=score if score != '' else None
        )
        if heat is not None and heat != '':
            new_book.heat = heat
        new_book.save()
        save_to_frontend('../se_teamwork/src/assets', new_book.book_cover)
        return JsonResponse({'errno': 0, 'msg': '添加成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})


@csrf_exempt
@login_required
@admin_required
def delete_book(request):
    """
    刪除書籍, 只接受POST請求, Body所需的字段為:\n
    **# 必填項**\n
    'ISBN': ISBN

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'POST':
        isbn = request.POST.get('ISBN')
        if isbn is None or len(str(isbn)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必要信息缺失, 请检查后重新提交'})
        try:
            Book.objects.get(ISBN=isbn).delete()
            return JsonResponse({'errno': 0, 'msg': '刪除成功'})
        except Book.DoesNotExist:
            return JsonResponse({'errno': 942, 'msg': '书籍不存在'})
    else:
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})


@csrf_exempt
@login_required
@admin_required
def update_book_info(request):
    """
    更新指定ISBN號的對應書籍信息, 只接受POST請求, Body所需的字段為:\n
    'ISBN': ISBN\n
    **# 以下所有的字段都是非必填的, 要改哪個填哪個**\n
    'book_name': 書名\n
    'book_cover': 封面文件\n
    'introduction': 簡介\n
    'book_type': 書籍類型\n
    'author': 作者姓名\n
    'author_country': 作者國籍\n
    'press': 出版社名\n
    'published_date': 出版日期(格式: YYYY-MM-DD)\n
    'page_number': 頁數\n
    'price': 價格\n
    'score': 評分\n
    'heat': 熱門度

    :param request:
    :return:
    """
    if request.method == 'POST':
        isbn = request.POST.get('ISBN')
        if isbn is None or len(str(isbn)) == 0:
            return JsonResponse({'errno': 911, 'msg': '必要信息缺失, 请检查后重新提交'})
        try:
            book = Book.objects.get(ISBN=isbn)
        except Book.DoesNotExist:
            return JsonResponse({'errno': 942, 'msg': '书籍不存在'})
        info = {
            'book_name': request.POST.get('book_name'),
            'introduction': request.POST.get('introduction'),
            'book_type': request.POST.get('book_type'),
            'author': request.POST.get('author'),
            'author_country': request.POST.get('author_country'),
            'press': request.POST.get('press'),
            'published_date': request.POST.get('published_date'),
            'page_number': request.POST.get('page_number'),
            'price': request.POST.get('price'),
            'score': request.POST.get('score'),
            'heat': request.POST.get('heat')
        }
        for key in info:
            if info[key] is None or len(str(info[key])) == 0:
                info[key] = book.__dict__[key]
        book_cover = request.FILES.get('book_cover')
        code, msg = __check_book_info(
            isbn,
            info['book_name'],
            book_cover,
            info['book_type'],
            info['author'],
            info['author_country'],
            info['press'],
            info['published_date'],
            info['page_number'],
            info['price'],
            info['score'],
            info['heat'],
            skip_check_duplicates=True
        )
        if code < 0:
            return msg
        book.book_name = info['book_name']
        if book_cover is not None:
            book.book_cover = book_cover
        book.introduction = info['introduction']
        book.book_type = info['book_type']
        book.author = info['author']
        book.author_country = info['author_country']
        book.press = info['press']
        book.published_date = date.fromisoformat(info['published_date'])
        book.page_number = info['page_number']
        book.price = info['price']
        book.score = info['score']
        book.heat = info['heat']
        book.save()
        save_to_frontend('../se_teamwork/src/assets', book.book_cover)
        return JsonResponse({'errno': 0, 'msg': '更新成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})


@csrf_exempt
def get_book_info_by_key(request, raw=False):
    """
    取得指定屬性同時包含指定關鍵詞的信息的對應書籍信息, **可选** 根据关键字排序和选择升序降序(是否反转), 只接受GET請求, Params格式為:\n
    ?屬性名=關鍵詞[&...][&sort_by=屬性名&reverse=(True or False)]

    :param raw: bool = False, 是否返回原始数据
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
            'ISBN': request.GET.get('ISBN'),
            'book_name': request.GET.get('book_name'),
            'introduction': request.GET.get('introduction'),
            'book_type': request.GET.get('book_type'),
            'author': request.GET.get('author'),
            'author_country': request.GET.get('author_country'),
            'press': request.GET.get('press'),
            'published_date': request.GET.get('published_date'),
            'page_number': request.GET.get('page_number'),
            'price': request.GET.get('price'),
            'score': request.GET.get('score'),
            'heat': request.GET.get('heat')
        }
        if not any(info.values()):
            if raw:
                return []
            return JsonResponse({'errno': 911, 'msg': '必要信息缺失, 请检查后重新提交'})
        books = list(filter(lambda x: __search(info, x), Book.objects.all()))
        sort_by = request.GET.get('sort_by')
        reverse = request.GET.get('reverse')
        if sort_by is not None and sort_by != '':
            if sort_by not in Book.__dict__:
                if raw:
                    return []
                return JsonResponse({'errno': 934, 'msg': '排序字段不存在'})
            if reverse in ['True', 'true', 't', 'T', 'TRUE', '1', 'Yes', 'yes', 'YES', 'y', 'Y', '1']:
                reverse = True
            else:
                reverse = False
            books.sort(key=lambda x: (x.__dict__[sort_by], x.heat, x.score, x.price, x.published_date, x.ISBN),
                       reverse=reverse)
        if raw:
            return list(map(lambda x: x.to_dict(), books))
        if len(books) == 0:
            return JsonResponse({'errno': 946, 'msg': '找不到符合条件的结果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), books))})
    else:
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})


@csrf_exempt
def get_book_info(request, raw=False):
    """
    根據關鍵字進行模糊搜索, 每個關鍵字之間使用','分隔\n
    只要滿足屬性中同時包含所有關鍵字的書籍都會被選出\n
    如果提供的keyword為空則默認返回所有書籍的信息\n
    **可选** 根据关键字排序和选择升序降序(是否反转)\n
    只接受GET請求, Params格式為:\n
    ?keyword=value1[,value2,...][&sort_by=屬性名&reverse=(True or False)]

    :param raw: bool = False, 是否返回原始数据
    :param request: WSGIRequest
    :return: JsonResponse
    """

    def __search(__keywords, obj):
        _ = obj.to_dict()
        for key in _:
            if key == 'book_cover':
                continue
            for __keyword in __keywords:
                if __keyword not in str(_[key]):
                    break
            else:
                return True
        return False

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword is None or keyword == '':
            if raw:
                return list(map(lambda x: x.to_dict(), Book.objects.all()))
            return JsonResponse(
                {'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), Book.objects.all()))}
            )
        keywords = str(keyword).split(',')
        books = list(filter(lambda x: __search(keywords, x), Book.objects.all()))
        sort_by = request.GET.get('sort_by')
        reverse = request.GET.get('reverse')
        if sort_by is not None and sort_by != '':
            if sort_by not in Book.__dict__:
                if raw:
                    return []
                return JsonResponse({'errno': 934, 'msg': '排序字段不存在'})
            if reverse in ['True', 'true', 't', 'T', 'TRUE', '1', 'Yes', 'yes', 'YES', 'y', 'Y', '1']:
                reverse = True
            else:
                reverse = False
            books.sort(key=lambda x: (x.__dict__[sort_by], x.heat, x.score, x.price, x.published_date, x.ISBN),
                       reverse=reverse)
        if raw:
            return list(map(lambda x: x.to_dict(), books))
        if len(books) == 0:
            return JsonResponse({'errno': 946, 'msg': '找不到符合条件的结果'})
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': list(map(lambda x: x.to_dict(), books))})
    else:
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})


@csrf_exempt
def get_book_info_by_isbn(request, raw=False):
    """
    取得指定ISBN號的書籍信息, 並為熱度值+1, 只接受GET請求, Params格式為:\n
    ?ISBN=書籍ISBN

    :param raw: bool = False, 是否返回原始数据
    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method == 'GET':
        isbn = request.GET.get('ISBN')
        if not isbn:
            if raw:
                return []
            return JsonResponse({'errno': 911, 'msg': '必要信息缺失, 请检查后重新提交'})
        try:
            book = Book.objects.get(ISBN=isbn)
        except Book.DoesNotExist:
            if raw:
                return []
            return JsonResponse({'errno': 946, 'msg': '找不到符合条件的结果'})
        book.heat += 1
        book.save()
        if raw:
            return [book.to_dict()]
        return JsonResponse({'errno': 0, 'msg': '查詢成功', 'data': [book.to_dict()]})
    else:
        return JsonResponse({'errno': 916, 'msg': '请求方式错误, 只接受GET请求'})


@csrf_exempt
@login_required
def set_book_score(request):
    """
    设置指定ISBN號的書籍的評分, 并自动计算平均值后写回数据库, 需要重新更新书籍展示页面的评分数据, 只接受POST請求, body所需字段:\n
    'ISBN': 書籍ISBN\n
    'score': 書籍评分

    :param request: WSGIRequest
    :return: JsonResponse
    """
    if request.method != 'POST':
        return JsonResponse({'errno': 901, 'msg': '请求方式错误, 只接受POST请求'})
    isbn = request.POST.get('ISBN')
    score = request.POST.get('score')
    if not isbn or not score:
        return JsonResponse({'errno': 911, 'msg': '必要信息缺失, 请检查后重新提交'})
    try:
        book = Book.objects.get(ISBN=isbn)
    except Book.DoesNotExist:
        return JsonResponse({'errno': 942, 'msg': '書籍不存在'})
    try:
        score = float(score)
        if score < 0 or score > 5:
            raise ValueError()
    except ValueError:
        return JsonResponse({'errno': 941, 'msg': '评分不合法'})
    if not book.score:
        book.score = score
    else:
        book.score = (float(book.score) * book.score_num_cnt + score) / (book.score_num_cnt + 1)
    book.score_num_cnt += 1
    book.save()
    return JsonResponse({'errno': 0, 'msg': '评分成功'})
