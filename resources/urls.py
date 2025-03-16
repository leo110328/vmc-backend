# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("addFile", views.addFile),
    path("query_page", views.query_page),
    path("delete/<str:id>", views.delete),
    path("downloadFile/<str:id>", views.download),
]

# urlpatterns += router.urls
