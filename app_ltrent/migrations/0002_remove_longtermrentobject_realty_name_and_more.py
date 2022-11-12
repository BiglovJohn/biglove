# Generated by Django 4.1.1 on 2022-11-08 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ltrent', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='longtermrentobject',
            name='realty_name',
        ),
        migrations.RemoveField(
            model_name='longtermrentobject',
            name='realty_to_city',
        ),
        migrations.AlterField(
            model_name='longtermrentobject',
            name='realty_type',
            field=models.CharField(choices=[('h', 'Отель'), ('c', 'Хостел'), ('a', 'Апартаменты'), ('ah', 'Апарт-отель'), ('gh', 'Гостевой дом'), ('k', 'Коттедж'), ('v', 'Вилла'), ('kp', 'Кемпинг'), ('gp', 'Глэмпинг'), ('kv', 'Квартира'), ('dm', 'Дом')], max_length=2, verbose_name='Тип объекта'),
        ),
    ]