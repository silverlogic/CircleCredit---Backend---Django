from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = User
        fields = ('name', 'stars', 'job', 'id')
        read_only_fields = ('id',)
