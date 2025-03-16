# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("delete/<str:id>", views.delete),
    path("query_page", views.query_page),
    path("query_date", views.query_date),
]

# urlpatterns += router.urls
