"""config URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import accounts.views
import board.views
import reply.views
import user.views
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 크롬 접속기록 자동저장에 의한 오류 주의
    path('board/create', board.views.create), # ID값에 해당 주소로 접근해라
    path('board/list', board.views.list),
    path('', board.views.list),
    path('board/read/<int:bid>', board.views.read),
    path('board/delete/<int:bid>', board.views.delete),
    path('board/update/<int:bid>', board.views.update),
    path('board/search', board.views.search),
    path('board/index', board.views.index),

    path('user/signup', user.views.signup),
    path('user/login', user.views.login),
    path('user/logout', user.views.logout),
    path('activate/<str:uid64>/<str:token>/', user.views.activate, name="activate"),

    path('reply/create/<int:bid>', reply.views.create), # <int:bid> DB의 번호를 받으려는 상황
    # <정수형:이름>의 변수를 생성한 것
    path('reply/delete/<int:bid>', reply.views.delete),
    path('reply/update/<int:bid>', reply.views.update),

    path('like/<int:bid>', board.views.like),

    path('kakaologin', accounts.views.kakaoLoginPage),
    path('oauth/redirect', accounts.views.getcode),
    path('accounts/profile', accounts.views.profile),
    path('accounts/delete', accounts.views.user_delete),
    path('accounts/update', accounts.views.user_update),
    path('password/', accounts.views.password, name='password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 미디어 경로를 추가해준다.