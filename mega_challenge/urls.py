from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.challenge, name='challenge'),
]
