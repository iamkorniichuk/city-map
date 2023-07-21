from django.urls import path

from .apps import MediaConfig
from .views import *

app_name = MediaConfig.name

urlpatterns = [
    path("", MediaList.as_view(), name="list"),
]
