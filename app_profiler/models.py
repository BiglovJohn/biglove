from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phone_field import PhoneField

from .managers import UserManager


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
    ('c', 'Юридическое лицо'),
    ('i', 'Индивидуальный предприниматель'),
    ('p', 'Самозанятый'),
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')
    phone = PhoneField(blank=True, help_text='Номер телефона')

    birthday = models.DateField(default=timezone.now, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=_GENDER, default='m', blank=True, verbose_name='Пол')
    book_count = models.PositiveIntegerField(default=0, verbose_name='Бронирований')
    status = models.CharField(max_length=1, choices=_LOYALTY_SYSTEM, default='d', verbose_name='Статус клиента')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_company = models.BooleanField(default=False, verbose_name='Компания')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_superuser = models.BooleanField(default=False, verbose_name='Статус Администратора')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'app_profiler_customuser'
        ordering = ['created_at']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
