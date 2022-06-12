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
    path('get_group_by_id', get_group_by_id),
    path('get_all_groups', get_all_groups),
    path('join_group', join_group),
    path('leave_group', leave_group),
    path(' create_group', create_group),
    path('get_groups_by_user', get_groups_by_user),
    path('get_post_by_id', get_post_by_id),
    path('send_post', send_post),
    path('get_posts_by_group_id', get_posts_by_group_id),
    path('remove_post', remove_post),
    path('get_posts_by_user', get_posts_by_user),
    path('like_post', like_post),
    path('dislike_post', dislike_post),
    path('get_group_info_by_key', get_group_info_by_key),
    path('get_group_info', get_group_info),
    path('get_post_info', get_post_info),
    path('get_post_info_by_key', get_post_info_by_key),
    path('apply_group_admin', apply_group_admin),
    path('upload_img', upload_img),
    path('top_post_by_id', top_post_by_id),
    path('get_top_posts', get_top_posts),
    path('feature_post_by_id', feature_post_by_id),
    path('get_feature_posts', get_featured_posts),
]
