from rest_framework import views

from users.serializers import UserSerializer


class UserViewSet(views.ModelViewSet):
    serializer_class = UserSerializer


