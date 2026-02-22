import django_filters
from .models import Advertisement

class AdvertisementFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()  # DateFromToRangeFilter для диапазона дат
    
    class Meta:
        model = Advertisement
        fields = ['status', 'created_at']
