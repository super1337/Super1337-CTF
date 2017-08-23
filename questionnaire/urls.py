from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<quiz_slug>[-A-Za-z0-9_]+)/$', views.quiz, name='quiz'),
    url(r'^(?P<quiz_slug>[-A-Za-z0-9_]+)/(?P<question_slug>[-A-Za-z0-9_]+)/$', views.question, name='question')
]
