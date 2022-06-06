from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from book.models import *
from datetime import date

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
    917:    用戶未登入, 且未提供任何可供查詢的字段
    931:    ISBN已存在
    932:    ISBN過長
    933:    書名過長
    934:    封面地址過長
    935:    書籍類型過長
    936:    作者姓名過長
    937:    作者國籍過長
    938:    出版社名過長
    939:    出版日期不合法
    940:    價格不合法
    941:    評分不合法
    942:    書籍不存在
"""


def __check_book_info(isbn, name, cover, book_type, author, author_country, press, published_date, price, score):
    """
    檢查書籍信息是否合法, 並返回錯誤代碼和jsonResponse, 合法返回0, 否則返回-1, 私有函數, 不可在外部調用, 此函數可忽略

    :param isbn: str
    :param name: str
    :param cover: str
    :param book_type: str
    :param author: str
    :param author_country: str
    :param press: str
    :param published_date: str
    :param price: str
    :param score: str
    :return: tuple(code: int, msg: JsonResponse | None)
    """
    if isbn is None or name is None or cover is None or book_type is None or author is None or press is None or \
            published_date is None or price is None or len(str(isbn)) == 0 or len(str(name)) == 0 or \
            len(str(cover)) == 0 or len(str(book_type)) == 0 or len(str(author)) == 0 or len(str(press)) == 0 or \
            len(str(published_date)) == 0 or len(str(price)) == 0:
        return -1, JsonResponse({'errno': 911, 'msg': '必填字段為空'})
    try:
        _ = Book.objects.get(ISBN=isbn)
        return -1, JsonResponse({'errno': 931, 'msg': 'ISBN已存在'})
    except Book.DoesNotExist:
        if len(str(isbn)) > 20:
            return -1, JsonResponse({'errno': 932, 'msg': 'ISBN過長'})
        if len(str(name)) > 100:
            return -1, JsonResponse({'errno': 933, 'msg': '書名過長'})
        if len(str(cover)) > 500:
            return -1, JsonResponse({'errno': 934, 'msg': '封面地址過長'})
        if len(str(book_type)) > 50:
            return -1, JsonResponse({'errno': 935, 'msg': '書籍類型過長'})
        if len(str(author)) > 50:
            return -1, JsonResponse({'errno': 936, 'msg': '作者姓名過長'})
        if author_country != '' and author_country is not None and len(str(author_country)) > 50:
            return -1, JsonResponse({'errno': 937, 'msg': '作者國籍過長'})
        if len(str(press)) > 50:
            return -1, JsonResponse({'errno': 938, 'msg': '出版社名過長'})
        try:
            _ = date.fromisoformat(published_date)
        except ValueError:
            return -1, JsonResponse({'errno': 939, 'msg': '出版日期不合法'})
        if float(price) < 0:
            return -1, JsonResponse({'errno': 940, 'msg': '價格不合法'})
        if score != '' and score is not None and (float(score) < 0 or float(score) > 10):
            return -1, JsonResponse({'errno': 941, 'msg': '評分不合法'})
        return 0, None


@csrf_exempt
def add_book(request):
    """
    新增書籍, 只接受POST請求, Body所需的字段為:\n
    **# 必填項**\n
    'ISBN': ISBN\n
    'name': 書名\n
    'cover': 封面地址url\n
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
        name = request.POST.get('name')
        cover = request.POST.get('cover')
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
            isbn, name, cover, book_type, author, author_country, press, published_date, price, score
        )
        if code < 0:
            return msg
        new_book = Book(
            ISBN=isbn,
            name=name,
            cover=cover,
            introduction=introduction if introduction is not None else '',
            book_type=book_type,
            author=author,
            author_country=author_country if author_country is not None else '',
            press=press,
            published_date=date.fromisoformat(published_date),
            page_number=page_number,
            price=price,
            score=score,
            heat=heat
        )
        new_book.save()
        return JsonResponse({'errno': 0, 'msg': '添加成功'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤, 只接受POST請求'})


@csrf_exempt
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
            return JsonResponse({'errno': 911, 'msg': '必填字段為空'})
        try:
            Book.objects.get(ISBN=isbn).delete()
            return JsonResponse({'errno': 0, 'msg': '刪除成功'})
        except Book.DoesNotExist:
            return JsonResponse({'errno': 942, 'msg': '書籍不存在'})
    else:
        return JsonResponse({'errno': 901, 'msg': '請求方式錯誤, 只接受POST請求'})
