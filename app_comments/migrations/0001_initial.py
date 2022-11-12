# Generated by Django 4.1.1 on 2022-11-08 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_premises', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=1000, verbose_name='Комментарий')),
                ('publish_at', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')),
                ('realty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_premises.holidayhouseobject', verbose_name='Объект недвижимости')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'comments_db',
                'ordering': ['publish_at'],
            },
        ),
    ]
