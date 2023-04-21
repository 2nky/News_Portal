from .views import (
    Search,
    ATCreate,
    ATUpdate,
    ATDelete,
)
from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
    path("", NewsList.as_view(), name="news_list"),
    path("<int:pk>", NewsDetail.as_view(), name="news_detail"),
    path("search", Search.as_view(), name="news_search"),
    path("create/", ATCreate.as_view(), name="articles_create"),
    path("<int:pk>/edit/", ATUpdate.as_view(), name="articles_update"),
    path("<int:pk>/delete/", ATDelete.as_view(), name="articles_delete"),
]
