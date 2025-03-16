# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ws/<str:room_name>/<str:token>", views.room, name="room"),
    path("query_page", views.query_page),
    path("query_chat_object", views.query_chat_object),
    path("query_self_page", views.query_self_page),
]