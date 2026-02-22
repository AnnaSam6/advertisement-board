from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError  # ИСПРАВЛЕНО: правильный импорт для ошибки
from django_filters.rest_framework import DjangoFilterBackend
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter  # Добавлено для фильтрации по дате

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter  # ИСПРАВЛЕНО: вместо filterset_fields
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Проверка на количество открытых объявлений
        open_ads = Advertisement.objects.filter(
            creator=self.request.user, 
            status=Advertisement.OPEN
        ).count()
        
        if open_ads >= 10:
            raise ValidationError("У вас не может быть больше 10 открытых объявлений")  # ИСПРАВЛЕНО
        
        serializer.save(creator=self.request.user)
