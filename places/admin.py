from django.contrib import admin

from media.admin import MediaInline

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "location")
    inlines = (MediaInline,)
    exclude = ("",)
