# Generated by Django 3.2.6 on 2021-08-12 14:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PLZ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plz', models.CharField(max_length=5)),
                ('name', models.CharField(blank=True, max_length=86, null=True)),
                ('population', models.IntegerField()),
                ('qkm', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name': 'PLZ',
                'verbose_name_plural': 'PLZen',
            },
        ),
    ]
