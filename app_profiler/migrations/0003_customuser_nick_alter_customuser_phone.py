# Generated by Django 4.1.1 on 2022-11-04 09:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profiler', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nick',
            field=models.CharField(blank=True, max_length=30, verbose_name='Имя для slug'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='', help_text='Номер телефона', max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^(\\+\\d{7})?,?\\s?\\d{8,13}')]),
        ),
    ]
