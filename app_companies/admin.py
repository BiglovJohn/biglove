from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from .models import CompanyProfile


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'short_company_name', 'inn', 'ogrn', 'company_phone', 'company_email', 'created_at']
    list_display_links = ['id', 'user']
    list_select_related = ['user']
    list_filter = [('created_at', DateRangeFilter), 'type']
    search_fields = ('short_company_name', 'inn__startswith', 'ogrn__startswith', 'company_phone__startswith',
                     'company_email__startswith')
    readonly_fields = ['created_at']

    fieldsets = (
        ('Общая информация', {'fields': ('user', 'slug', 'created_at', 'type')}),
        ('Реквизиты компании', {'fields': ('full_company_name', 'short_company_name', 'legal_address', 'actual_address',
                                           'inn', 'kpp', 'ogrn', 'bank_account', 'bank_name', 'kor_account', 'bic',
                                           'director', 'company_phone', 'company_email')}),
    )

