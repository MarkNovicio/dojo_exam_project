from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('registration/create', views.create_registration),
    path('user/login', views.login),
    path('user/logout', views.logout)
]