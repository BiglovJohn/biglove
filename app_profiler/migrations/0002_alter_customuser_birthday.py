# Generated by Django 4.1.1 on 2022-11-18 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profiler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(blank=True, verbose_name='Дата рождения'),
        ),
    ]