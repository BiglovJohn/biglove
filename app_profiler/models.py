from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager
from pytils.translit import slugify
from django.urls import reverse

from app_premises.models import HolidayHouseObject
from app_ltrent.models import LongTermRentObject
from django.conf import settings

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

phone_regex = RegexValidator(regex=r'^(\+\d{7})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='Имя для slug')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=12, default='', help_text='Номер телефона')

    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
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

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
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


class Favorite(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    hotel_objects = models.ManyToManyField(
        to=HolidayHouseObject,
        blank=True,
        related_name='favorite_hotels',
        verbose_name='Избранные отели'
    )
    long_term_objects = models.ManyToManyField(
        to=LongTermRentObject,
        blank=True,
        related_name='favorite_lt_objects',
        verbose_name='Избранное жильё'
    )

    class Meta:
        db_table = 'favorite_list_db'
        verbose_name = 'Избранныё'
        verbose_name_plural = 'Избранные'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = CustomUser.objects.get(id=instance.id)
        Favorite.objects.create(user=user)
