"""se_teamwork_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('account.urls', 'account'))),
    path('book/', include(('book.urls', 'book'))),
    path('movie/', include(('movie.urls', 'movie'))),
    path('group/', include(('group.urls', 'group'))),
    path('topic/', include(('topic.urls', 'topic'))),
    path('comment/', include(('comment.urls', 'comment'))),
    path('main_page/', include(('main_page.urls', 'main_page'))),
]
