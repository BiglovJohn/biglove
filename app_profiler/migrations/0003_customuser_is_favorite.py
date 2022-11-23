# Generated by Django 4.1.1 on 2022-11-18 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_premises', '0009_remove_holidayhouseobject_is_favorites'),
        ('app_profiler', '0002_alter_customuser_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_favorite',
            field=models.ManyToManyField(related_name='favorite', to='app_premises.holidayhouseobject', verbose_name='Избранные'),
        ),
    ]