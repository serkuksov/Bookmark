from django.urls import path

from bookmarks_app.views import BookmarkListView, BookmarkCreateView

urlpatterns = [
    path("", BookmarkListView.as_view(), name="bookmark_list"),
    path("add_bookmark/", BookmarkCreateView.as_view(), name="add_bookmark"),
]
