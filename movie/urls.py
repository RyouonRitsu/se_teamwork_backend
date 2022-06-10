from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('add_movie', add_movie),
    path('delete_movie', delete_movie),
    path('update_movie_info', update_movie_info),
    path('get_movie_info_by_key', get_movie_info_by_key),
    path('get_movie_info', get_movie_info),
    path('get_movie_info_by_id', get_movie_info_by_id),
    path('set_movie_score', set_movie_score),
]
