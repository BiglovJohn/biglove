from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from pytils.translit import slugify

_MANAGER_TYPE = [
    ('c', 'Юридическое лицо'),
    ('i', 'Индивидуальный предприниматель'),
    ('p', 'Самозанятый'),
]


class CompanyProfile(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Управляющий')

    slug = models.SlugField(max_length=30, unique=True, verbose_name='Название для slug')

    type = models.CharField(max_length=1, default='c', choices=_MANAGER_TYPE, verbose_name='Форма управления')
    full_company_name = models.CharField(max_length=100, blank=True, verbose_name='Полное наименование')
    short_company_name = models.CharField(max_length=100, blank=True, verbose_name='Сокращенное наименование')
    legal_address = models.CharField(max_length=250, blank=True, verbose_name='Юридический адрес')
    actual_address = models.CharField(max_length=250, blank=True, verbose_name='Фактический адрес')
    inn = models.CharField(max_length=10, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, blank=True, verbose_name='КПП')
    ogrn = models.CharField(max_length=13, blank=True, verbose_name='ОГРН')
    bank_account = models.CharField(max_length=22, blank=True, verbose_name='Рассчётный счёт')
    bank_name = models.CharField(max_length=200, blank=True, verbose_name='Наименование банка')
    kor_account = models.CharField(max_length=22, blank=True, verbose_name='Корреспондентский счёт')
    bic = models.CharField(max_length=9, blank=True, verbose_name='БИК')

    director = models.CharField(max_length=50, verbose_name='Руководитель')
    company_phone = models.CharField(max_length=10, verbose_name='Номер телефона')
    company_email = models.CharField(max_length=50, verbose_name='Email')
    created_at = models.DateTimeField(default=timezone.now,
                                      auto_created=timezone.now,
                                      verbose_name='Дата создания'
                                      )

    def __str__(self):
        return self.short_company_name

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if self.slug is None:
            self.slug = slugify(self.id)
        return super().save(*args, **kwargs)

    class Meta:
        """Определение параметров в мета классе альбом"""
        db_table = 'company_db'
        ordering = ['created_at']
        verbose_name = 'Профиль компании'
        verbose_name_plural = 'Профили компаний'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_company:
            CompanyProfile.objects.create(user=instance)
        elif instance.is_superuser:
            CompanyProfile.objects.create(user=instance)
            # Guest.objects.create(referring_user=instance, first_name=instance.first_name,
            # last_name=instance.last_name, email=instance.email)
        # else: Guest.objects.create(referring_user=instance, first_name=instance.first_name,
        # last_name=instance.last_name, email=instance.email)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.save()


# class Guest(models.Model): referring_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
# on_delete=models.CASCADE, verbose_name='Пользователь') first_name = models.CharField(max_length=50,
# verbose_name='Имя') last_name = models.CharField(max_length=50, verbose_name='Фамилия') phone_number =
# models.CharField(max_length=10, verbose_name='Номер телефона') email = models.CharField(max_length=50, blank=True,
# null=True, verbose_name='Электронная почта') guest_birthday = models.DateField(default=timezone.now, blank=True,
# verbose_name='Дата рождения') guest_gender = models.CharField(max_length=1, choices=_GENDER, blank=True,
# verbose_name='Пол') guest_book_count = models.PositiveIntegerField(default=0, verbose_name='Бронирований')
# guest_status = models.CharField(max_length=1, choices=_LOYALTY_SYSTEM, default='d', verbose_name='Статус клиента')
#
#     def __str__(self):
#         return self.first_name + ' ' + self.last_name
#
#     class Meta:
#         """Определение параметров в мета классе альбом"""
#         db_table = 'guest_db'
#         ordering = ['last_name']
#         verbose_name = 'Гость'
#         verbose_name_plural = 'Гости'
