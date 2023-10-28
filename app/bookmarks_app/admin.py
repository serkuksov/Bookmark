from django.contrib import admin

from .models import Bookmark


@admin.register(Bookmark)
class AdminPatternTask(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "description",
        "created_at",
    )
