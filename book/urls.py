from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('add_book', add_book),
    path('delete_book', delete_book),
    path('update_book_info', update_book_info),
    path('get_book_info_by_key', get_book_info_by_key),
    path('get_book_info', get_book_info),
    path('get_book_info_by_isbn', get_book_info_by_isbn)
]
