from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        user = self.request.user
        friends = user.friends
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

