from django.contrib import admin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter
from .models import Camp, RealtyOptions, Reservation, Photos, Favorite, Flat, \
    FurnitureModel, TechniqueModel, Advertising


@admin.register(Camp)
class HolidayHouseObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'realty_name', 'realty_type', 'realty_book_count', 'total_views']
    list_editable = ["realty_type"]
    list_display_links = ['id']
    list_select_related = ['company']
    list_filter = (('created_at', DateRangeFilter), ('realty_price', NumericRangeFilter),
                   ('realty_area', NumericRangeFilter), 'realty_type')
    readonly_fields = ['created_at', 'realty_book_count']
    fieldsets = (
        ('Административная информация', {'fields': ('company', 'created_at', 'slug')}),
        ('Общая информация', {'fields': ('realty_name', 'stars', 'realty_to_city', 'realty_type',
                                         'count_of_persons', 'realty_area', 'full_description')}),
        ('Адрес', {'fields': ('realty_country', 'realty_region', 'realty_city', 'realty_address', 'region_center')}),
        ('Финансовая информация', {'fields': ('realty_price',)}),
        ('Статистическая информация', {'fields': ('realty_book_count', )}),
        ('Рекламный блок', {'fields': ('is_advertised', )}),
        ('Удобства', {'fields': ('options', 'pay_type', 'food_options', 'book_cancel')}),
    )

    prepopulated_fields = {"slug": ("realty_name",)}


@admin.register(RealtyOptions)
class RealtyOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'option_name', 'category']
    search_fields = ('option_name__startswith', 'category__startswith')
    list_filter = ['category']
    readonly_fields = ['views_count']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_booked', 'realty', 'guest', 'check_in', 'check_out', 'total_sum']
    list_display_links = ['id', 'realty', 'guest']
    list_select_related = ['realty', 'guest']
    list_filter = [('total_sum', NumericRangeFilter), ('check_in', DateRangeFilter), ('check_out', NumericRangeFilter),
                   'is_booked']
    search_fields = ('realty__realty_name__startswith', 'guest__name', 'book_number')
    readonly_fields = ['total_sum', 'booked_at', 'canceled_at']
    fieldsets = (
        ('Внешние ключи', {'fields': ('realty', 'guest')}),
        ('Общая информация', {'fields': ('check_in', 'check_out')}),
        ('Финансовая информация', {'fields': ('total_sum', 'is_booked', 'is_canceled')}),
        ('Даты', {'fields': ('booked_at', 'canceled_at')})
    )


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    fields = ('user', 'camps', 'flats')


@admin.register(Flat)
class LongTermRentObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'realty_type', 'total_views']
    list_display_links = ['id',]
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


@admin.register(Advertising)
class AdvertisingModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    fields = ('user', 'image', 'text')


admin.site.site_header = 'BIGLOV'
