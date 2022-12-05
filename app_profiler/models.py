from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from pytils.translit import slugify
from django.urls import reverse


_LOYALTY_SYSTEM = [
    ('d', 'Джун'),
    ('D', 'Джун+'),
    ('m', 'Мид'),
    ('M', 'Мид+'),
    ('s', 'Синьор'),
]

_GENDER = [
    ('m', 'Мужской'),
    ('w', 'Женский'),
]

_MANAGER_TYPE = [
    ('c', 'Организация'),
    ('p', 'Самозанятый'),
]

_NDS = [
    ('y', 'с НДС'),
    ('n', 'без НДС')
]

phone_regex = RegexValidator(regex=r'^(\+\d{7})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='Имя для slug')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=12, blank=True, default='', help_text='Номер телефона')

    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=_GENDER, default='m', blank=True, verbose_name='Пол')
    book_count = models.PositiveIntegerField(default=0, verbose_name='Бронирований')
    status = models.CharField(max_length=1, choices=_LOYALTY_SYSTEM, default='d', verbose_name='Статус клиента')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_company = models.BooleanField(default=False, verbose_name='Компания')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_superuser = models.BooleanField(default=False, verbose_name='Статус Администратора')

    """ Часть модели, относящаяся к данным компании """

    type = models.CharField(max_length=1, blank=True, choices=_MANAGER_TYPE, verbose_name='Форма управления')
    nds = models.CharField(max_length=1, blank=True, choices=_NDS, verbose_name='НДС')
    full_company_name = models.CharField(max_length=100, blank=True, verbose_name='Полное наименование')
    short_company_name = models.CharField(max_length=100, blank=True, verbose_name='Сокращенное наименование')
    legal_address = models.CharField(max_length=250, blank=True, verbose_name='Юридический адрес')
    actual_address = models.CharField(max_length=250, blank=True, verbose_name='Фактический адрес')
    inn = models.CharField(max_length=10, blank=True, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, blank=True, verbose_name='КПП')
    ogrn = models.CharField(max_length=13, blank=True, verbose_name='ОГРН')
    bank_account = models.CharField(max_length=22, blank=True, verbose_name='Рассчётный счёт')
    bank_name = models.CharField(max_length=200, blank=True, verbose_name='Наименование банка')
    kor_account = models.CharField(max_length=22, blank=True, verbose_name='Корреспондентский счёт')
    bic = models.CharField(max_length=9, blank=True, verbose_name='БИК')
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Отчество')
    passport_series = models.IntegerField(blank=True, null=True, verbose_name='Серия паспорта')
    passport_number = models.IntegerField(blank=True, null=True, verbose_name='Номер паспорта')
    passport_who = models.CharField(max_length=100, null=True, blank=True, verbose_name='Кем выдан')
    passport_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='Код подразделения')
    passport_date = models.DateField(blank=True, null=True, verbose_name='Дата выдачи паспорта')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts_db'
        ordering = ['created_at']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Возвращает имя пользователя."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправка письма на почту пользователю."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
