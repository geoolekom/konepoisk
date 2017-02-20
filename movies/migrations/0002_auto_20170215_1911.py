# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Название')),
                ('age', models.IntegerField(verbose_name='Возраст')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActorMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Название')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удален?'),
        ),
        migrations.AddField(
            model_name='movie',
            name='title',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='actormovie',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Genre', verbose_name='Жанр'),
        ),
    ]
