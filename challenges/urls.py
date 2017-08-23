from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^(?P<challenge_slug>[-A-Za-z0-9_]+)/$', views.challenge, name='challenge')
]
