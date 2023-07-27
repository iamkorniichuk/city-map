from rest_framework import generics

from .models import Place
from .serializers import PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
