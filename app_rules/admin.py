from django.contrib import admin

from .models import RulesModel


@admin.register(RulesModel)
class RealtyOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'sub_category']
    list_filter = ['category', 'sub_category']
