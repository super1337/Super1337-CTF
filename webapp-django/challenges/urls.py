from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^(?P<name>[a-z0-9.-]+)/$', views.challenge, name='challenge'),
    url(r'textBased/', views.textBased, name='textBased')
]
