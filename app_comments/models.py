from django.db import models
from app_profiler.models import CustomUser
from app_premises.models import Camp


class Comments(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    realty = models.ForeignKey(to=Camp, on_delete=models.CASCADE, verbose_name='Объект недвижимости')
    comment_text = models.TextField(max_length=1000, verbose_name='Комментарий')
    publish_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        """Определение параметров в мета классе комментария"""
        db_table = 'comments_db'
        ordering = ['publish_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
