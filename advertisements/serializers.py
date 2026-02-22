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
    
    def validate(self, data):
        """Проверка на количество открытых объявлений"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем только при создании нового объявления
            if not self.instance:  # Это создание, а не обновление
                open_ads = Advertisement.objects.filter(
                    creator=request.user,
                    status=Advertisement.OPEN
                ).count()
                
                if open_ads >= 10:
                    raise serializers.ValidationError(
                        "У вас не может быть больше 10 открытых объявлений"
                    )
        return data
