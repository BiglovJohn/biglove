from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_company', 'created_at']
    readonly_fields = ['created_at', 'status', 'book_count']
    list_filter = ['is_active', 'is_company']
    search_fields = ('email__startswith', 'phone__startswith')
    fieldsets = (
        ('Учетные данные пользователя', {'fields': ('email', 'password', 'created_at')}),
        ('Статусы', {'fields': ('is_superuser', 'is_staff', 'is_company', 'is_active')}),
        ('Общая информация', {'fields': ('first_name', 'last_name', 'middle_name', 'slug', 'phone', 'gender', 'birthday', 'telegram')}),
        ('Паспортные данные', {'fields': ('passport_series', 'passport_number', 'passport_who', 'passport_code',
                                          'passport_date')}),
        ('Статистическая информация', {'fields': ('status', 'book_count')}),
        ('Доступы и группы', {'fields': ('groups', 'user_permissions')}),
        ('Реквизиты компании', {'fields': ('full_company_name', 'short_company_name', 'nds', 'legal_address',
                                           'actual_address', 'inn', 'kpp', 'ogrn', 'bank_account', 'bank_name',
                                           'kor_account', 'bic')
                                }
         ),
    )

    def mark_as_junior_plus(self, request, queryset):
        queryset.update(guest_status='D')

    def mark_as_middle(self, request, queryset):
        queryset.update(guest_status='m')

    def mark_as_middle_plus(self, request, queryset):
        queryset.update(guest_status='M')

    def mark_as_senior(self, request, queryset):
        queryset.update(guest_status='s')

    mark_as_junior_plus.short_description = 'Поревести всех в статус Джун+'
    mark_as_middle.short_description = 'Поревести всех в статус Мид'
    mark_as_middle_plus.short_description = 'Поревести всех в статус Мид+'
    mark_as_senior.short_description = 'Поревести всех в статус Синьор'


# @admin.register(Guest)
# class GuestAdmin(admin.ModelAdmin):
#     list_display = ['id', 'referring_user', 'guest_status', 'first_name', 'last_name', 'phone_number', 'email',
#                     'guest_book_count']
#     search_fields = ('first_name__startswith', 'last_name__startswith', 'phone_number__startswith',
#                      'email__startswith')
#     list_filter = ['guest_status', 'guest_gender']
#     list_display_links = ['id', 'referring_user']
#     list_select_related = ['referring_user']
#     readonly_fields = ['guest_status', 'guest_book_count']
#     fieldsets = (
#         ('Общая информация', {'fields': ('first_name', 'last_name', 'guest_gender', 'guest_birthday', 'phone_number',
#                                          'email')}
#          ),
#         ('Статистическая информация', {'fields': ('guest_status', 'guest_book_count')}
#          )
#     )
#
#     actions = ['mark_as_junior_plus', 'mark_as_middle', 'mark_as_middle_plus', 'mark_as_senior']
#
#     def mark_as_junior_plus(self, request, queryset):
#         queryset.update(guest_status='D')
#
#     def mark_as_middle(self, request, queryset):
#         queryset.update(guest_status='m')
#
#     def mark_as_middle_plus(self, request, queryset):
#         queryset.update(guest_status='M')
#
#     def mark_as_senior(self, request, queryset):
#         queryset.update(guest_status='s')
#
#     mark_as_junior_plus.short_description = 'Поревести всех в статус Джун+'
#     mark_as_middle.short_description = 'Поревести всех в статус Мид'
#     mark_as_middle_plus.short_description = 'Поревести всех в статус Мид+'
#     mark_as_senior.short_description = 'Поревести всех в статус Синьор'
