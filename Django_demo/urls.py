"""
URL configuration for Django_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from Django_demo import settings
# from app01 import views
from app02 import views

urlpatterns = [
    # path('silk/', include('silk.urls', namespace='silk')),
    # path('admin/', admin.site.urls),

    # app01
    # path('index/', views.index),
    # path('user_list/', views.user_list),
    # path('user_add/', views.user_add),
    # path('tql/', views.tql),
    # path('news/', views.news),
    # path('something/', views.something),
    #
    # # 用户登录
    # path('login/', views.login),
    # path('orm/', views.orm),
    #
    # # 案例：用户管理
    # path('info/list', views.info_list),
    # path('info/add', views.info_add),
    # path('info/delete', views.info_delete),

    # app02
    path('', views.index),
    # 部门列表
    path('depart/list', views.depart_list),
    path('depart/add', views.depart_add),
    path('depart/delete', views.depart_delete),
    path('depart/<int:nid>/edit', views.depart_edit),

    # 用户列表
    path('user/list', views.user_list),
    path('user/add', views.user_add),
    path('user/model/form/add', views.user_model_form_add),
    path('user/<int:nid>/edit', views.user_edit),
    path('user/<int:nid>/delete', views.user_delete),

    # 靓号列表
    path('pretty/list', views.pretty_list),
    path('pretty/add', views.pretty_add),
    path('pretty/<int:nid>/edit', views.pretty_edit),
    path('pretty/<int:nid>/delete', views.pretty_delete),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
