# Generated by Django 4.1.1 on 2022-11-28 14:50

import app_profiler.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='Имя для slug')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Фамилия')),
                ('phone', models.CharField(blank=True, default='', help_text='Номер телефона', max_length=12)),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('m', 'Мужской'), ('w', 'Женский')], default='m', max_length=1, verbose_name='Пол')),
                ('book_count', models.PositiveIntegerField(default=0, verbose_name='Бронирований')),
                ('status', models.CharField(choices=[('d', 'Джун'), ('D', 'Джун+'), ('m', 'Мид'), ('M', 'Мид+'), ('s', 'Синьор')], default='d', max_length=1, verbose_name='Статус клиента')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('is_company', models.BooleanField(default=False, verbose_name='Компания')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Статус персонала')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Статус Администратора')),
                ('type', models.CharField(blank=True, choices=[('c', 'Организация'), ('p', 'Самозанятый')], max_length=1, verbose_name='Форма управления')),
                ('nds', models.CharField(blank=True, choices=[('y', 'с НДС'), ('n', 'без НДС')], max_length=1, verbose_name='НДС')),
                ('full_company_name', models.CharField(blank=True, max_length=100, verbose_name='Полное наименование')),
                ('short_company_name', models.CharField(blank=True, max_length=100, verbose_name='Сокращенное наименование')),
                ('legal_address', models.CharField(blank=True, max_length=250, verbose_name='Юридический адрес')),
                ('actual_address', models.CharField(blank=True, max_length=250, verbose_name='Фактический адрес')),
                ('inn', models.CharField(blank=True, max_length=10, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, max_length=9, verbose_name='КПП')),
                ('ogrn', models.CharField(blank=True, max_length=13, verbose_name='ОГРН')),
                ('bank_account', models.CharField(blank=True, max_length=22, verbose_name='Рассчётный счёт')),
                ('bank_name', models.CharField(blank=True, max_length=200, verbose_name='Наименование банка')),
                ('kor_account', models.CharField(blank=True, max_length=22, verbose_name='Корреспондентский счёт')),
                ('bic', models.CharField(blank=True, max_length=9, verbose_name='БИК')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('passport_series', models.IntegerField(blank=True, null=True, verbose_name='Серия паспорта')),
                ('passport_number', models.IntegerField(blank=True, null=True, verbose_name='Номер паспорта')),
                ('passport_who', models.CharField(blank=True, max_length=100, null=True, verbose_name='Кем выдан')),
                ('passport_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Код подразделения')),
                ('passport_date', models.DateField(blank=True, null=True, verbose_name='Дата выдачи паспорта')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'accounts_db',
                'ordering': ['created_at'],
            },
            managers=[
                ('objects', app_profiler.managers.UserManager()),
            ],
        ),
    ]
