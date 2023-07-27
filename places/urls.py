from django.urls import path

from .apps import PlacesConfig
from .views import *

app_name = PlacesConfig.name


urlpatterns = [
    path("", PlaceList.as_view(), name="list"),
    path("<slug:slug>", PlaceDetail.as_view(), name="detail"),
]
