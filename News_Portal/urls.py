from django.views.decorators.cache import cache_page

from .views import (
    Search,
    NWCreate,
    NWUpdate,
    NWDelete,
    AddSubscriber,
)
from django.urls import path
from .views import NewsList, NewsDetail, error_view

urlpatterns = [
    path("", NewsList.as_view(), name="news_list"),
    path("error", error_view, name="news_list"),
    path(
        "<int:pk>",
        NewsDetail.as_view(),
        name="news_detail",
    ),
    path("search", Search.as_view(), name="news_search"),
    path("create/", NWCreate.as_view(), name="news_create"),
    path("<int:pk>/edit/", NWUpdate.as_view(), name="news_update"),
    path("<int:pk>/delete/", NWDelete.as_view(), name="news_delete"),
    path("subscribe", AddSubscriber.as_view(), name="subscribe"),
]
