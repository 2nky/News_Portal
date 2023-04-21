from .views import Search, PostCreate, PostUpdate
from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
    path("", NewsList.as_view(), name="news_list"),
    path("<int:pk>", NewsDetail.as_view(), name="news_detail"),
    path("search", Search.as_view(), name="news_search"),
    path("create/", PostCreate.as_view(), name="post_create"),
    path("<int:pk>/edit/", PostUpdate.as_view(), name="post_update"),
]
