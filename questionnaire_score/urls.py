# chat/urls.py
from django.urls import path

from . import views

# router = DefaultRouter()
# router.register("api", views.CommodityInfoModelViewSet),

urlpatterns = [
    path("add", views.add),
    path("query_total_score", views.query_total_score),
    path("query_answer_list", views.query_answer_list),
    # path("query_date", views.query_date),
]

# urlpatterns += router.urls
