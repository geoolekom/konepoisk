# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 16:19
from __future__ import unicode_literals

from django.db import migrations, models
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20170217_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to=movies.models.Movie.poster_path, verbose_name='Постер'),
        ),
    ]