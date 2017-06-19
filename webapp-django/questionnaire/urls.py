from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^contest/round1/$',views.mcq,name='mcq')
]
