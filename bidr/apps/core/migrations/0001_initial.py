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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('name', models.CharField(blank=True, verbose_name='Full Name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='Email Address', max_length=75, unique=True)),
                ('phone_number', models.CharField(verbose_name='Phone Number', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, verbose_name='groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'Bidr User',
                'verbose_name_plural': 'Bidr Users',
            },
            bases=(models.Model,),
        ),
    ]
