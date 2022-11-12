from django.contrib import admin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter
from .models import LongTermRentObject, FurnitureModel, TechniqueModel, LongTermPhotos


@admin.register(LongTermRentObject)
class LongTermRentObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_company_name', 'realty_type']
    list_display_links = ['id', 'short_company_name']
    list_select_related = ['company']
    list_filter = (('created_at', DateRangeFilter), ('realty_price', NumericRangeFilter), 'realty_type')
    readonly_fields = ['created_at']
    fieldsets = (
        ('Административная информация', {'fields': ('company', 'created_at', 'is_advertised', 'is_active')}),
        ('Параметры жилья', {'fields': ('realty_type', 'rooms_count', 'floor_count', 'realty_area', 'full_description',
                                        'bathroom', 'children', 'animals', 'smoke', 'furniture', 'technique')}),
        ('Адрес', {'fields': ('realty_country', 'realty_region', 'realty_city', 'city_area', 'micro_city_area',
                              'realty_address', 'house_number', 'house_korpus', 'floor')}),
        ('Финансовая информация', {'fields': ('realty_price', 'deposit')}),
    )


@admin.register(FurnitureModel)
class FurnitureModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']


@admin.register(TechniqueModel)
class TechniqueModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']


@admin.register(LongTermPhotos)
class LongTermPhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'long_term_obj', 'created_at']
