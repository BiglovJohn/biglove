from uuid import uuid4
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytils.translit import slugify
from django.urls import reverse

#  Внешние импорты

from app_data.models import Ip
from app_profiler.models import CustomUser

# _REALTY_TYPE = [
#     ('h', 'Отель'),
#     ('c', 'Хостел'),
#     ('a', 'Апартаменты'),
#     ('ah', 'Апарт-отель'),
#     ('gh', 'Гостевой дом'),
#     ('k', 'Коттедж'),
#     ('v', 'Вилла'),
#     ('kp', 'Кемпинг'),
#     ('gp', 'Глэмпинг'),
#     ('kv', 'Квартира'),
#     ('dm', 'Дом'),
# ]

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
    """Путь, куда будет осуществлена загрузка MEDIA_ROOT/<realty_name>/<filename>"""
    return f'{instance}/{filename}'


def advertising_path(instance, filename):
    """Путь, куда будет осуществлена загрузка MEDIA_ROOT/adv/<realty_name>/<filename>"""
    return f'adv/{filename}'


def max_value(image_file):
    """Валидатор для ограничения размера загружаемой картинки"""
    if image_file.size >= 1024 * 1024:
        raise ValueError('Максимальный размер файла 1 Мб')


class RealtyOptions(models.Model):
    option_name = models.CharField(max_length=100, verbose_name='Название опции')
    category = models.CharField(max_length=50, blank=True, verbose_name='Категория')
    icon_url = models.CharField(max_length=100, blank=True, verbose_name='Иконка')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Искали раз')

    def __str__(self):
        return self.option_name

    class Meta:
        db_table = 'options_db'
        ordering = ['-views_count']
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'


class FurnitureModel(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    category = models.CharField(max_length=40, verbose_name='Категория')
    icon_url = models.CharField(max_length=100, blank=True, verbose_name='Иконка')

    def __str__(self):
        return self.name

    class Meta:
        """ Определение параметров в мета классе """
        db_table = 'furniture_db'
        ordering = ['category']
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'


class TechniqueModel(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    category = models.CharField(max_length=40, verbose_name='Категория')
    icon_url = models.CharField(max_length=100, blank=True, verbose_name='Иконка')

    def __str__(self):
        return self.name

    class Meta:
        """ Определение параметров в мета классе """
        db_table = 'technique_db'
        ordering = ['category']
        verbose_name = 'Техника'
        verbose_name_plural = 'Техника'


class RealtyObjectBaseClass(models.Model):
    company = models.ForeignKey(to=CustomUser, default=1, on_delete=models.CASCADE, verbose_name='Пользователь')
    realty_country = models.CharField(max_length=250, blank=True, verbose_name='Страна')
    realty_region = models.CharField(max_length=250, blank=True, verbose_name='Регион')
    realty_city = models.CharField(max_length=250, blank=True, verbose_name='Населенный пункт')
    realty_address = models.CharField(max_length=250, blank=True, verbose_name='Адрес')
    full_description = models.TextField(max_length=2000, blank=True, verbose_name='Описание')
    realty_price = models.PositiveIntegerField(blank=True, default=0, verbose_name='Цена')
    is_advertised = models.BooleanField(default=False, verbose_name='Статус продвижения')
    views_count = models.ManyToManyField(Ip, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    children = models.BooleanField(blank=True, default=False, verbose_name='Можно с детьми')
    animals = models.BooleanField(blank=True, default=False, verbose_name='Можно с животными')
    smoke = models.BooleanField(blank=True, default=False, verbose_name='Можно курить')
    ind = models.CharField(max_length=6, blank=True, verbose_name='Индекс') #TODO Добавить в админку

    def total_views(self):
        return self.views_count.count()

    class Meta:
        abstract = True
        ordering = ['id']
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Camp(RealtyObjectBaseClass):
    """ Модель альтернативных объектов размещения: кемпинги, глемпинги и прочее """

    _STARS = [
        ('0', 'Нет звезд'),
        ('1', '1 звезда'),
        ('2', '2 звезды'),
        ('3', '3 звезды'),
        ('4', '4 звезды'),
        ('5', '5 звезд'),
    ]

    _REALTY_TYPE = [
        ('k', 'Коттедж'),
        ('kp', 'Кемпинг'),
        ('gp', 'Глэмпинг'),
        ('dm', 'Дом'),
    ]

    realty_name = models.CharField(max_length=100, verbose_name='Название объекта')
    realty_type = models.CharField(max_length=2, blank=True, choices=_REALTY_TYPE, verbose_name='Тип объекта')
    slug = models.SlugField(unique=True, default=None, verbose_name="URL")
    count_of_persons = models.PositiveIntegerField(default=1, verbose_name='Количество спальных мест')
    realty_area = models.PositiveIntegerField(blank=True, default=0, verbose_name='Площадь')
    region_center = models.CharField(max_length=30, blank=True, verbose_name='Региональный центр')
    realty_to_city = models.CharField(max_length=10, blank=True, verbose_name='Расстояние до города')
    book_cancel = models.CharField(max_length=1, choices=_BOOK_CANCEL, default='n', verbose_name='Отмена бронирования')
    pay_type = models.CharField(max_length=1, choices=_PAY_TYPE, default='o', verbose_name='Способ оплаты')
    food_options = models.CharField(max_length=1, choices=_FOOD_OPTIONS, default='e', verbose_name='Опции питания')
    options = models.ManyToManyField(to=RealtyOptions, blank=True, verbose_name='Опции', related_name='option_list')
    arriving_time = models.TimeField(default='14:00', verbose_name='Время заселения с')
    departure_time = models.TimeField(default='09:00', verbose_name='Время выезда с')
    arriving_time_to = models.TimeField(default='23:00', verbose_name='Время заселения до')
    departure_time_to = models.TimeField(default='12:00', verbose_name='Время выезда до')
    realty_book_count = models.PositiveIntegerField(default=0, verbose_name='Бронирований')
    stars = models.CharField(max_length=1, default='0', choices=_STARS, verbose_name='Звёздность') #TODO Добавить в админку

    def __str__(self):
        return self.realty_name

    def get_absolute_url(self):
        return reverse("realty_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if self.slug is None:
            self.slug = slugify(self.realty_name)
        return super().save(*args, **kwargs)

    class Meta:
        """Определение параметров в мета классе альбом"""
        db_table = 'camps_db'
        ordering = ['created_at']
        verbose_name = 'Кемпинг'
        verbose_name_plural = 'Кемпинги'


class Flat(RealtyObjectBaseClass):

    _LT_REALTY_TYPE = [
        ('kv', '1-к комнатная квартира'),
        ('2k', '2-х комнатная квартира'),
        ('3k', '3-х комнатная квартира'),
        ('4k', '4-х комнатная квартира'),
        ('ks', 'Квартира-студия'),
        ('a', 'Апартаменты'),
        ('k', 'Коттедж'),
        ('v', 'Вилла'),
        ('dm', 'Дом'),
    ]

    _BATHROOM = [
        ('a', 'Совмещенный'),
        ('b', 'Раздельный'),
    ]

    rooms_count = models.PositiveIntegerField(default=1, blank=True, verbose_name='Количество комнат')
    house_number = models.CharField(max_length=10, blank=True, default='', verbose_name='Номер дома')
    house_korpus = models.CharField(max_length=10, blank=True, default='', verbose_name='Корпус, литер, блок')
    floor = models.PositiveIntegerField(default=1, blank=True, verbose_name='Этаж')
    floor_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='Количество этажей')
    city_area = models.CharField(max_length=50, blank=True, verbose_name='Район города')
    micro_city_area = models.CharField(max_length=50, blank=True, verbose_name='Микрорайон города')
    bathroom = models.CharField(max_length=1, blank=True, choices=_BATHROOM, default='a', verbose_name='Санузел')
    deposit = models.PositiveIntegerField(null=True, blank=True, verbose_name='Залог')
    realty_area = models.FloatField(blank=True, null=True, verbose_name='Площадь')
    realty_type = models.CharField(max_length=2, choices=_LT_REALTY_TYPE, verbose_name='Тип объекта')

    furniture = models.ManyToManyField(to=FurnitureModel,
                                       blank=True,
                                       verbose_name='Мебель',
                                       related_name='furnitures'
                                       )
    technique = models.ManyToManyField(to=TechniqueModel,
                                       blank=True,
                                       verbose_name='Техника',
                                       related_name='techniques'
                                       )

    def __str__(self):
        return str(self.get_realty_type_display()) + ', ' + str(self.realty_area) + ' м²' + ', г. ' + self.realty_city

    class Meta:
        """ Определение параметров в мета классе альбом """
        db_table = 'flats_db'
        ordering = ['created_at']
        verbose_name = 'Длительный срок'
        verbose_name_plural = 'Длительный срок'


class Reservation(models.Model):
    realty = models.ForeignKey(to=Camp, on_delete=models.CASCADE, verbose_name='Объект недвижимости')
    guest = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Гости')
    book_identifier = models.CharField(max_length=10, default=uuid4, unique=True, verbose_name='Номер бронирования')
    check_in = models.DateField(verbose_name='Дата заезда')
    check_out = models.DateField(verbose_name='Дата выселения')
    is_booked = models.BooleanField(default=False, verbose_name='Бронь')
    total_sum = models.IntegerField(default=0, verbose_name='Сумма')
    booked_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата бронирования')
    is_canceled = models.BooleanField(default=False, verbose_name='Отменённая')
    canceled_at = models.DateTimeField(auto_now=True, verbose_name='Дата отмены')

    def __str__(self):
        return self.realty.realty_name

    class Meta:
        """Определение параметров в мета классе альбом"""
        db_table = 'reservations_db'
        ordering = ['check_in']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class Photos(models.Model):
    """ Класс для описания модели фото """

    flat = models.ForeignKey(to=Flat,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             related_name='flat_photos',
                             verbose_name='Идентификатор квартиры')
    camp = models.ForeignKey(to=Camp,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             related_name='camp_photos',
                             verbose_name='Идентификатор кемпа')
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

    def __str__(self):
        if self.flat:
            return self.flat.realty_name
        elif self.camp:
            return self.camp.realty_name

    class Meta:
        """ Определение параметров в мета классе фото """
        db_table = 'photos_db'
        ordering = ['created_at']
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Favorite(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    camps = models.ManyToManyField(
        to=Camp,
        blank=True,
        related_name='favorite_camps',
        verbose_name='Избранные кемпинги'
    )
    flats = models.ManyToManyField(
        to=Flat,
        blank=True,
        related_name='favorite_flats',
        verbose_name='Избранные квартиры'
    )

    class Meta:
        db_table = 'favorites_db'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = CustomUser.objects.get(id=instance.id)
        Favorite.objects.create(user=user)


class Advertising(models.Model):
    user = models.ForeignKey(to=CustomUser,
                             on_delete=models.CASCADE,
                             verbose_name='Рекламодатель',
                             related_name='advertising'
                             )
    image = models.ImageField(upload_to=advertising_path,
                              blank=True,
                              validators=[max_value, FileExtensionValidator(['jpg', 'jpeg', 'png'],
                                                                            'Поддерживаются файлы JPG, JPEG и PNG')
                                          ],
                              verbose_name='Фотография')
    text = models.TextField(max_length=400, blank=True, verbose_name='Рекламное объявление')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'advertising_db'
        ordering = ['created_at']
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'
