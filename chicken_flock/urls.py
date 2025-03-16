# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("update", views.update),
    path("query_page", views.query_page),
    path("query/<str:id>", views.query),
    path("close/<str:id>", views.close),
    path("add_other_attributes", views.add_other_attributes),
    path("query_all", views.query_all),
    # path("query_all_by_farm", views.query_all_by_farm),
]

# urlpatterns += router.urls
