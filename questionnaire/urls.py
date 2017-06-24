from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'contest/round1/', views.questions, name='questions'),
    url(r'contest/$', views.contest, name='contest'),
]
