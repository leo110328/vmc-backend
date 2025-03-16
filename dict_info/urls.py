# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("query", views.query),
    path("delete", views.delete),
]

# urlpatterns += router.urls
