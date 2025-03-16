# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("query_page", views.query_page),
    path("delete/<str:id>", views.delete),
    path("update/<str:id>", views.update),
    path("detail/<str:id>", views.detail),
]

# urlpatterns += router.urls
