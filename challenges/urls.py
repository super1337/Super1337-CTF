from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^(?P<challenge_name>[a-z0-9.-]+)/$', views.challenge, name='challenge')
]
