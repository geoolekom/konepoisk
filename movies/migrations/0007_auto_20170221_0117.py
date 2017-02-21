# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20170219_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'verbose_name': 'Актер', 'verbose_name_plural': 'Актеры'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'verbose_name': 'Фильм', 'verbose_name_plural': 'Фильмы'},
        ),
        migrations.AddField(
            model_name='movie',
            name='box_office',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сборы'),
        ),
        migrations.AddField(
            model_name='movie',
            name='budget',
            field=models.IntegerField(blank=True, null=True, verbose_name='Бюджет'),
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год выпуска'),
        ),
    ]
