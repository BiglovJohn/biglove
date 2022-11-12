from uuid import uuid4
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from pytils.translit import slugify
from django.urls import reverse

#  Внешние импорты
from app_profiler.models import CustomUser
from app_companies.models import CompanyProfile

_REALTY_TYPE = [
    ('h', 'Отель'),
    ('c', 'Хостел'),
    ('a', 'Апартаменты'),
    ('ah', 'Апарт-отель'),
    ('gh', 'Гостевой дом'),
    ('k', 'Коттедж'),
    ('v', 'Вилла'),
    ('kp', 'Кемпинг'),
    ('gp', 'Глэмпинг'),
    ('kv', 'Квартира'),
    ('dm', 'Дом'),
]

_PAY_TYPE = [
    ('o', 'Оплата онлайн'),
    ('c', 'Оплата на месте')
]

_FOOD_OPTIONS = [
    ('a', 'Завтрак включён'),
    ('b', 'Завтрак + обед или ужин включены'),
    ('c', 'Завтрак, обед и ужин включены'),
    ('d', 'Всё включено'),
    ('e', 'Питание не включено'),
]

_BOOK_CANCEL = [
    ('y', 'Беспл. отмена брони'),
    ('n', 'Нет беспл. отмены брони'),
]


def user_directory_path(instance, filename):
    """Путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>"""
    return f'{instance.realty_obj}/{filename}'


def max_value(image_file):
    """Валидатор для ограничения размера загружаемой картинки"""
    if image_file.size >= 1024 * 1024:
        raise ValueError('Максимальный размер файла 1 Мб')


class RealtyOptions(models.Model):
    option_name = models.CharField(max_length=100, verbose_name='Название опции')
    category = models.CharField(max_length=50, blank=True, verbose_name='Гатегория')
    icon_url = models.CharField(max_length=100, blank=True, verbose_name='Иконка')

    def __str__(self):
        return self.option_name

    class Meta:
        db_table = 'options_db'
        ordering = ['id']
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'


class RealtyObjectBaseClass(models.Model):
    realty_country = models.CharField(max_length=250, default='Россия', verbose_name='Страна')
    realty_region = models.CharField(max_length=250, default='Московская область', verbose_name='Регион')
    realty_city = models.CharField(max_length=250, default='Москва', verbose_name='Населенный пункт')
    realty_address = models.CharField(max_length=250, verbose_name='Адрес')
    realty_type = models.CharField(max_length=2, choices=_REALTY_TYPE, verbose_name='Тип объекта')
    full_description = models.TextField(max_length=2000, blank=True, verbose_name='Описание')
    realty_price = models.PositiveIntegerField(verbose_name='Цена')
    is_advertised = models.BooleanField(default=False, verbose_name='Статус продвижения')

    class Meta:
        abstract = True
        ordering = ['id']
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class HolidayHouseObject(RealtyObjectBaseClass):
    company = models.ForeignKey(to=CompanyProfile, default=1, on_delete=models.CASCADE, related_name='hh_companies',
                                verbose_name='Пользователь')
    realty_name = models.CharField(max_length=100, verbose_name='Название объекта')
    slug = models.SlugField(unique=True, default=None, verbose_name="URL")
    count_of_persons = models.PositiveIntegerField(default=1, verbose_name='Количество спальных мест')
    realty_area = models.PositiveIntegerField(blank=True, verbose_name='Площадь')
    region_center = models.CharField(max_length=30, blank=True, verbose_name='Региональный центр')
    realty_to_city = models.CharField(max_length=10, blank=True, verbose_name='Расстояние до города')
    book_cancel = models.CharField(max_length=1, choices=_BOOK_CANCEL, default='n', verbose_name='Отмена бронирования')
    pay_type = models.CharField(max_length=1, choices=_PAY_TYPE, default='o', verbose_name='Способ оплаты')
    food_options = models.CharField(max_length=1, choices=_FOOD_OPTIONS, default='e', verbose_name='Опции питания')
    options = models.ManyToManyField(to=RealtyOptions, blank=True, verbose_name='Опции', related_name='option_list')
    arriving_time = models.TimeField(default='14:00', verbose_name='Время заселения')
    departure_time = models.TimeField(default='12:00', verbose_name='Время выезда')
    realty_book_count = models.PositiveIntegerField(default=0, verbose_name='Бронирований')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.realty_name

    def short_company_name(self):
        if len(self.company.short_company_name) > 25:
            return self.company.short_company_name[:25] + '...'
        else:
            return self.company.short_company_name

    def get_absolute_url(self):
        return reverse("realty_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if self.slug is None:
            self.slug = slugify(self.realty_name)
        return super().save(*args, **kwargs)

    short_company_name.short_description = 'Пользователь'

    class Meta:
        """Определение параметров в мета классе альбом"""
        db_table = 'holiday_house_db'
        ordering = ['created_at']
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимость'


class Reservation(models.Model):
    realty = models.ForeignKey(to=HolidayHouseObject, on_delete=models.CASCADE, verbose_name='Объект недвижимости')
    guest = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Гости')
    book_identifier = models.CharField(max_length=10, default=uuid4, unique=True, verbose_name='Номер бронирования')
    check_in = models.DateField(verbose_name='Дата заезда')
    check_out = models.DateField(verbose_name='Дата выселения')
    is_booked = models.BooleanField(default=False, verbose_name='Бронь')
    total_sum = models.IntegerField(default=0, verbose_name='Сумма')
    booked_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата бронирования')

    def __str__(self):
        return self.realty.realty_name

    class Meta:
        """Определение параметров в мета классе альбом"""
        db_table = 'reservation_db'
        ordering = ['check_in']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class Photos(models.Model):
    """ Класс для описания модели фото """

    realty_obj = models.ForeignKey(to=HolidayHouseObject,
                                   on_delete=models.CASCADE,
                                   default=1,
                                   related_name='photos',
                                   verbose_name='Идентификатор объекта'
                                   )
    photo = models.ImageField(upload_to=user_directory_path,
                              blank=True,
                              validators=[max_value, FileExtensionValidator([
                                  'jpg',
                                  'jpeg',
                                  'png'],
                                  'Поддерживаются файлы JPG, JPEG и PNG')
                                          ],
                              verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата загрузки')

    class Meta:
        """ Определение параметров в мета классе фото """
        db_table = 'db.photo'
        ordering = ['created_at']
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
