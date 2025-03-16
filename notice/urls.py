# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("query_page", views.query_page),
    path("query_page_month", views.query_page_month),
    path("query_latest", views.query_latest),
    path("delete/<str:id>", views.delete),
]

# urlpatterns += router.urls
