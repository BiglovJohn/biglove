# Generated by Django 4.1.1 on 2022-11-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_companies', '0002_companyprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, verbose_name='Название для slug'),
        ),
    ]