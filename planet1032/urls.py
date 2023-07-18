"""planet1032 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views
from .models import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home,name='home'),
    path('signup/', views.signup),
    path('signin/', views.signin),
    path('signout/',views.signout, name='signout'),
    path('block_main/',views.blockmain),
    path('upload_articles/',views.upload),
    path('homepage/',views.homepage),
    path('myuploads/',views.myuploads),
    path('editworks/<int:article_id>/',views.editworks,name='editworks'),
    path('deleteimage/<int:image_id>/', views.deleteimage, name='deleteimage'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('accountUpdate', views.accountUpdate, name='accountUpdate'),
    path('myfavourites/', views.favorites, name='myfavourites'),
    path('toggle_favorite/<int:article_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle_like/<int:article_id>/', views.toggle_like, name='toggle_like'),
    path('toggle_dislike/<int:article_id>/', views.toggle_dislike, name='toggle_dislike'),
    path('mymessages/', views.mymessages, name='myfavourites'),

    #path('upload_article/', views.upload_article, name='upload_article'),
    path('upload_chapter/<int:article_id>/', views.upload_chapter, name='upload_chapter'),
    
    
    path('articles/<int:article_id>/<int:chapter_order>/', views.article_detail, name='chapter_detail'),
    path('articles_detail/<int:article_id>/<int:chapter_order>/', views.article_detail, name='article_detail'),
    # 单篇文章地址
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    
    path('article_detail_nochapter/<int:article_id>/', views.article_detail, name='article_detail_nochapter'),
    path('edu_articles/', views.article_list, name='article_list'),
    path('graphics/',views.graphics_list),
    path('fiction/',views.ff),
    path('commercial/',views.commercial),
    path('staff_main/',views.staff_main),
    path('blacklist/',views.blacklist),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)