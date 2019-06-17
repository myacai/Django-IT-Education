from django.urls import re_path, include
from .views import *


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^remen$', remen, name='remen'),
    re_path(r'^article/$', article, name='article'),
    re_path(r'^course/$', course, name='cousre'),
    re_path(r'^courseVideo/$', courseVideo, name='courseVideo'),
    re_path(r'my$', my, name='my'),
    re_path(r'^author',author,name='author'),
    re_path(r'^comment',comment,name='comment'),
    re_path(r'userLead', userLead, name='userLead'),
    re_path(r'^login$', login, name='login'),
    re_path(r'^articleAdd$', articleAdd, name='articleAdd'),
    re_path(r'^jingdong$', jingdong, name='jingdong'),
    re_path(r'^ouwang$', ouwang, name='ouwang'),
    re_path(r'^login12306$', login12306, name='login12306$'),
    re_path(r'^douban$', douban, name='douban'),
]
