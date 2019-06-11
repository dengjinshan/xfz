from rest_framework import serializers

from apps.xfzauth.models import User


class UserSeralizers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'telephone', 'email', 'username', 'is_active', 'is_staff']