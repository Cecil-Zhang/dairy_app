from rest_framework import serializers
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('dairy.users.serializers')

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)  # explicitly declare to override the auto-created unique constraint

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        read_only_fields = ('id', )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        logging.debug(validated_data)
        user = User.objects.create_user(validated_data['username'], email=validated_data['email'], password=validated_data['password'],\
            first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        return user
