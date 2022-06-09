from django.urls import path
from .views import *

#
# urlpatterns = [
#     # path('url_name', api_name)
#     path('register', register),
#     path('login', login),
#     path('logout', logout),
#     path('get_user_info_by_username', get_user_info_by_username),
#     path('get_user_info_by_user_id', get_user_info_by_user_id),
#     path('get_user_info', get_user_info),
#     path('update_user_info', update_user_info)
# ]
urlpatterns = [
    # path('url_name', api_name)
    path('get_topic_by_id', get_topic_by_id),
    path('get_all_topics', get_all_topics),
    path('get_all_topics_by_user', get_all_topics_by_user),
    path('join_topic', join_topic),
    path('leave_topic', leave_topic),
    path('create_topic', create_topic),
    path('write_diary', write_diary),
    path('like_diary', like_diary),
    path('dislike_diary', dislike_diary),
    path('get_all_diary_by_heat', get_all_diary_by_heat),
    path('get_all_diary_by_time', get_all_diary_by_time),
    path('get_diary_by_author_id', get_diary_by_author_id),
    path('get_diary_by_id', get_diary_by_id),
    path('get_diary_info_by_key', get_diary_info_by_key),
    path('get_diary_info', get_diary_info),
    path('get_topic_info', get_topic_info),
    path('get_topic_info_by_key', get_topic_info_by_key),
]
