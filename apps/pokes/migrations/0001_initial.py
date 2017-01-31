# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pokee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated', to='login.User')),
                ('poker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiator', to='login.User')),
            ],
        ),
    ]
