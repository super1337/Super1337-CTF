from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>[\w.@+_-]+)$', views.profile, name='profile'),
    url(r'^(?P<username>[\w.@+_-]+)/solved', views.solved, name='solved'),
    url(r'^(?P<username>[\w.@+_-]+)/edit', views.edit, name='edit profile'),
]
