from django.conf.urls import url
from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('/result/', views.result, name='result'),
    path('/result/message', views.message, name='message')
   ]
