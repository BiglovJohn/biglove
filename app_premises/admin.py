from django.contrib import admin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter

from .models import RealtyObject, RealtyOptions, Reservation, Photos


@admin.register(RealtyObject)
class RealtyObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_company_name', 'realty_name', 'realty_type', 'realty_price', 'realty_area',
                    'realty_book_count']
    list_display_links = ['id', 'short_company_name']
    list_select_related = ['company']
    list_filter = (('created_at', DateRangeFilter), ('realty_price', NumericRangeFilter),
                   ('realty_area', NumericRangeFilter), 'realty_type')
    readonly_fields = ['created_at', 'realty_book_count']
    fieldsets = (
        ('Административная информация', {'fields': ('company', 'created_at', 'slug', 'is_advertised')}),
        ('Общая информация', {'fields': ('realty_name', 'realty_to_city', 'realty_type',
                                         'count_of_persons', 'realty_area', 'full_description')}),
        ('Адрес', {'fields': ('realty_country', 'realty_region', 'realty_city', 'realty_address')}),
        ('Финансовая информация', {'fields': ('realty_price',)}),
        ('Статистическая информация', {'fields': ('realty_book_count',)}),
        ('Удобства', {'fields': ('options', 'pay_type', 'food_options', 'book_cancel')}),
    )

    prepopulated_fields = {"slug": ("realty_name",)}


@admin.register(RealtyOptions)
class RealtyOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'option_name', 'category']
    search_fields = ('option_name__startswith', 'category__startswith')
    list_filter = ['category']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_booked', 'realty', 'guest', 'check_in', 'check_out', 'total_sum']
    list_display_links = ['id', 'realty', 'guest']
    list_select_related = ['realty', 'guest']
    list_filter = [('total_sum', NumericRangeFilter), ('check_in', DateRangeFilter), ('check_out', NumericRangeFilter),
                   'is_booked']
    search_fields = ('realty__realty_name__startswith', 'guest__name', 'book_number')
    readonly_fields = ['total_sum']
    fieldsets = (
        ('Внешние ключи', {'fields': ('realty', 'guest')}),
        ('Общая информация', {'fields': ('check_in', 'check_out')}),
        ('Финансовая информация', {'fields': ('total_sum', 'is_booked')}),
    )


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'realty_obj', 'created_at']


admin.site.site_header = 'CHILL'
