from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'upload/', views.upload, name='upload'),
    url(r'upload2/', views.upload2, name='upload2'),
]
