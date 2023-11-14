from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from bookmarks_app.forms import BookmarkForm
from bookmarks_app.models import Bookmark


class BookmarkListView(LoginRequiredMixin, ListView):
    """Отображение списка закладок пользователя"""

    model = Bookmark

    def get_queryset(self):
        queryset: QuerySet[Bookmark] = super().get_queryset()
        return queryset.filter(user=self.request.user)


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    """Добавление новых закладок"""

    model = Bookmark
    form_class = BookmarkForm
    success_url = reverse_lazy("bookmark_list")

    def get_form(self):
        form = super().get_form()
        form.instance.user = self.request.user
        return form
