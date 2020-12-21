from django.urls import path

from . import views

urlpatterns = [
    path('groups', views.groups_index),
    path('groups/create', views.create_group),
    path('groups/<int:group_id>', views.show_group),
    path('groups/<int:group_id>/delete', views.delete_group),
    path('groups/<int:group_id>/join', views.join_group),
    path('groups/<int:group_id>/leave', views.leave_group),
]