from django.urls import path
from . import views

urlpatterns = [
    path('insert_fp', views.insert_fp, name='insert_fp'),
    path('wps', views.wps, name='wps'),
]