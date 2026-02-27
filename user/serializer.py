from rest_framework import serializers
from .services import create_user




class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    
    def create(self, validated_data):
        return create_user(**validated_data)
