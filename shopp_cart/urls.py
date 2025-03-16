# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add_commodity", views.add_commodity),
    path("del_commodity", views.delete_commodity),
    path("clear_commodity", views.clear_commodity),
    path("clear_cart", views.clear_cart),
    path("query_page", views.query_page),
]

# urlpatterns += router.urls
