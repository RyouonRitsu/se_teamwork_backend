from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    path('register', register),
    path('login', login),
    path('logout', logout)
]
