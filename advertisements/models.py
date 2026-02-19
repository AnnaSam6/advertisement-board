from django.db import models
from django.contrib.auth.models import User

class Advertisement(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (OPEN, 'Открыто'),
        (CLOSED, 'Закрыто'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='advertisements',
        verbose_name='Создатель'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default=OPEN,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
