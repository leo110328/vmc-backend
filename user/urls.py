# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("get_code_add", views.get_code_add),
    path("change_password", views.change_password),
    path("reset_password", views.reset_password),
    path("get_code_reset", views.get_code_reset),
    path("query_page", views.query_page),
    path("delete", views.delete),
    path("login", views.login),
    path("logout", views.logout),
]

# urlpatterns += router.urls
