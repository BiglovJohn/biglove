# Generated by Django 4.1.1 on 2022-11-18 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_rules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, verbose_name='Категория')),
                ('sub_category', models.CharField(max_length=50, verbose_name='Подкатегория')),
                ('text', models.TextField(max_length=10000, verbose_name='Текст правил')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Политика конфиденциальности',
                'verbose_name_plural': 'Политика конфиденциальности',
                'db_table': 'privacy_policy_db',
                'ordering': ['id'],
            },
        ),
    ]
