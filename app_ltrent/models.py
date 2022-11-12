from django.db import models
from django.core.validators import FileExtensionValidator
from app_premises.models import RealtyObjectBaseClass
from app_companies.models import CompanyProfile

_REALTY_TYPE = [
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


def user_directory_path(instance, filename):
    """ Путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename> """
    return f'{instance.long_term_obj}/{filename}'


def max_value(image_file):
    """ Валидатор для ограничения размера загружаемой картинки """
    if image_file.size >= 1024 * 1024:
        raise ValueError('Максимальный размер файла 1 Мб')


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


class LongTermRentObject(RealtyObjectBaseClass):
    _BATHROOM = [
        ('a', 'Совмещенный'),
        ('b', 'Раздельный'),
    ]

    company = models.ForeignKey(to=CompanyProfile, default=1, on_delete=models.CASCADE, related_name='lt_companies',
                                verbose_name='Пользователь')
    # district = models.CharField(max_length=10, verbose_name='Федеральный округ')
    rooms_count = models.PositiveIntegerField(default=1, verbose_name='Количество комнат')
    house_number = models.CharField(max_length=10, default='', verbose_name='Номер дома')
    house_korpus = models.CharField(max_length=10, default='', blank=True, verbose_name='Корпус, литер, блок')
    floor = models.PositiveIntegerField(default=1, verbose_name='Этаж')
    floor_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='Количество этажей')
    city_area = models.CharField(max_length=50, blank=True, verbose_name='Район города')
    micro_city_area = models.CharField(max_length=50, blank=True, verbose_name='Микрорайон города')
    bathroom = models.CharField(max_length=1, blank=True, choices=_BATHROOM, default='a', verbose_name='Санузел')
    deposit = models.PositiveIntegerField(null=True, blank=True, verbose_name='Залог')
    realty_area = models.FloatField(blank=True, null=True, verbose_name='Площадь')
    realty_type = models.CharField(max_length=2, choices=_REALTY_TYPE, verbose_name='Тип объекта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=False, verbose_name='Активно')
    children = models.BooleanField(blank=True, default=False, verbose_name='Можно с детьми')
    animals = models.BooleanField(blank=True, default=False, verbose_name='Можно с животными')
    smoke = models.BooleanField(blank=True, default=False, verbose_name='Можно курить')

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

    def short_company_name(self):
        if len(self.company.short_company_name) > 25:
            return self.company.short_company_name[:25] + '...'
        else:
            return self.company.short_company_name

    class Meta:
        """ Определение параметров в мета классе альбом """
        db_table = 'long_term_rent_db'
        ordering = ['created_at']
        verbose_name = 'Жильё'
        verbose_name_plural = 'Жильё'


class LongTermPhotos(models.Model):
    """ Класс для описания модели фото """

    long_term_obj = models.ForeignKey(to=LongTermRentObject,
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
        db_table = 'long_term_photo_db'
        ordering = ['created_at']
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
