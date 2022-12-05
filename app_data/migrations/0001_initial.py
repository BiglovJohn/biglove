# Generated by Django 4.1.1 on 2022-11-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
                ('visited_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'IP адрес',
                'verbose_name_plural': 'IP адреса',
                'db_table': 'ip_addresses_db',
                'ordering': ['visited_at'],
            },
        ),
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='Россия', max_length=50, verbose_name='Страна')),
                ('district', models.CharField(max_length=50, verbose_name='Федеральный округ')),
                ('region', models.CharField(max_length=50, verbose_name='Регион')),
                ('city', models.CharField(max_length=50, unique=True, verbose_name='Федеральный округ')),
            ],
            options={
                'verbose_name': 'Локация',
                'verbose_name_plural': 'Локации',
                'db_table': 'location_db',
                'ordering': ['city'],
            },
        ),
    ]
