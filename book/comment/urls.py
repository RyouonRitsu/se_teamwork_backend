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
    path('send_comment', send_comment),
    path('get_all_comments' , get_all_comments),
    path('remove_comment', remove_comment),
    path('like_comment', like_comment),
    path('dislike_comment', dislike_comment),
    path('show_report', show_report),
]
