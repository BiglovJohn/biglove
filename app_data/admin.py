from django.contrib import admin
from .models import Ip


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ['id']

