from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Advertisement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator', 'status', 'created_at']
        read_only_fields = ['creator', 'created_at']
