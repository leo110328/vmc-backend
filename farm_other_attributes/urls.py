# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("delete/<str:id>", views.delete),
    path("query_page", views.query_page),
    path("query_info", views.query_info),
    path("query_date", views.query_date),
    path("query_all_antibiotic", views.query_all_antibiotic),
    path("query_all_bacterialType", views.query_all_bacterialType),
]

# urlpatterns += router.urls
