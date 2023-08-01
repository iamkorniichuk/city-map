from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView, LogoutView, LogoutAllView
from knox.settings import knox_settings

from .serializers import UserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = knox_settings.USER_SERIALIZER
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token,
            }
        )
