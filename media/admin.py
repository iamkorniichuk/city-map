from django.utils.html import format_html
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Media


class MediaInline(GenericTabularInline):
    model = Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    exclude = ("content_type", "object_id")
    list_display = ("pk", "attachment_tag")

    def attachment_tag(self, obj):
        html = None
        mime_type = obj.attachment_type
        src = f'src="{obj.attachment.url}"'
        size = 'height="256"'
        if "image" in mime_type:
            html = format_html(f"<img {src} {size}/>")
        elif "video" in mime_type:
            html = format_html(
                f"""<video {size} controls>
                    <source {src} type="{mime_type}"
                </video>"""
            )
        return html

    attachment_tag.short_description = "Attachment"
