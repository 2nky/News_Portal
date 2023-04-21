from .views import (
    Search,
    NWCreate,
    NWUpdate,
    NWDelete,
)
from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
    path("", NewsList.as_view(), name="news_list"),
    path("<int:pk>", NewsDetail.as_view(), name="news_detail"),
    path("search", Search.as_view(), name="news_search"),
    path("create/", NWCreate.as_view(), name="news_create"),
    path("<int:pk>/edit/", NWUpdate.as_view(), name="news_update"),
    path("<int:pk>/delete/", NWDelete.as_view(), name="news_delete"),
]
