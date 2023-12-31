from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("users.urls")),
    path("admin/", admin.site.urls),
    path("media/", include("media.urls")),
    path("places/", include("places.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
