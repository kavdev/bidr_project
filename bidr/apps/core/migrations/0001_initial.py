# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidrUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(
                    verbose_name='superuser status',
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    default=False)
                 ),
                ('name', models.CharField(verbose_name='Full Name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='Email Address', max_length=75, unique=True)),
                ('phone_number', models.CharField(verbose_name='Phone Number', max_length=20)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('ios_device_token', models.CharField(
                    verbose_name='iOS Device Token', blank=True, null=True, max_length=64)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(
                    to='auth.Group', verbose_name='groups', related_query_name='user',
                    related_name='user_set', blank=True,
                    help_text='The groups this user belongs to. A user will get all permissions granted to'
                    ' each of his/her group.')),
                ('user_permissions', models.ManyToManyField(
                    to='auth.Permission', verbose_name='user permissions',
                    related_query_name='user', related_name='user_set', blank=True,
                    help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'Bidr User',
                'verbose_name_plural': 'Bidr Users',
            },
            bases=(models.Model,),
        ),
    ]
