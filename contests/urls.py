from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<contest_slug>[-A-Za-z0-9_]+)/$', views.contest_view, name='contest_view'),
    url(r'^(?P<contest_slug>[-A-Za-z0-9_]+)/register/$', views.contest_register, name='contest_register'),
    url(r'^(?P<contest_slug>[-A-Za-z0-9_]+)/(?P<challenge_slug>[-A-Za-z0-9_]+)/$',
        views.challenge_solve, name='challenge_solve')
]
