from django.urls import path

from .views import ListPostByCategory, PostDetailView, PostsListView, SearchBlogView

urlpatterns = [
    path("list/", PostsListView.as_view()),
    path("category/", ListPostByCategory.as_view()),
    path("detail/<slug>", PostDetailView.as_view()),
    path("search", SearchBlogView.as_view()),
]
