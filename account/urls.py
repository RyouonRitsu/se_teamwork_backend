from django.urls import path
from account.views import *

urlpatterns = [
    # path('url_name', api_name)
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('get_user_info_by_username', get_user_info_by_username),
    path('get_user_info_by_user_id', get_user_info_by_user_id),
    path('get_user_info', get_user_info),
    path('update_user_info', update_user_info)
]
