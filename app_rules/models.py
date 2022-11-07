from django.db import models


class RulesModel(models.Model):
    category = models.CharField(max_length=50, verbose_name='Категория')
    sub_category = models.CharField(max_length=50, verbose_name='Подкатегория')
    text = models.TextField(max_length=10000, verbose_name='Текст правил')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_category

    class Meta:
        """Определение параметров в мета классе альбом"""
        db_table = 'rules_db'
        ordering = ['id']
        verbose_name = 'Правила'
        verbose_name_plural = 'Правила'
