from rest_framework import generics
from rest_framework.response import Response

from .models import Media
from .serializers import MediaSerializer


class MediaList(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def create(self, request, *args, **kwargs):
        media = request.FILES.getlist("media")
        return Response(self.upload_files(media))

    def upload_files(self, media):
        media_objects = []
        for file in media:
            serializer = self.serializer_class(data={"file": file})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            media_objects.append(serializer.data)
        return media_objects
