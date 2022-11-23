from django.db import models
import json


class LocationModel(models.Model):
    country = models.CharField(max_length=50, default='Россия', verbose_name='Страна')
    district = models.CharField(max_length=50, verbose_name='Федеральный округ')
    region = models.CharField(max_length=50, verbose_name='Регион')
    city = models.CharField(max_length=50, unique=True, verbose_name='Федеральный округ')

    def __str__(self):
        return self.city

    class Meta:
        """ Определение параметров в мета классе локации """
        db_table = 'location_db'
        ordering = ['city']
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


""" Заполнение БД данными локаций """


# with open('russian-cities.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#     for element_info in data:
#         try:
#             test = LocationModel.objects.get(city=element_info['name'])
#         except LocationModel.DoesNotExist:
#             test = None
#
#         if test is None:
#             LocationModel.objects.create(district=element_info['district'], region=element_info['subject'],
#                                          city=element_info['name'])
#         else:
#             pass

class Ip(models.Model):  # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100)
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.ip

    class Meta:
        db_table = 'ip_addresses_db'
        ordering = ['visited_at']
        verbose_name = 'IP адрес'
        verbose_name_plural = 'IP адреса'
