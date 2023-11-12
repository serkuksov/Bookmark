from django import forms

from .models import Bookmark


class BookmarkForm(forms.ModelForm):
    """Форма создания закладки"""

    class Meta:
        model = Bookmark
        fields = ("bookmark_url",)

    def clean_bookmark_url(self):
        bookmark_url = self.cleaned_data.get("bookmark_url")
        user = self.instance.user
        if user is not None:
            # Проверить, нет ли уже закладки с такой комбинацией user и url
            if Bookmark.objects.filter(user=user, bookmark_url=bookmark_url).exists():
                raise forms.ValidationError(
                    "Закладка с текущим URL уже существует для данного пользователя"
                )
        return bookmark_url
