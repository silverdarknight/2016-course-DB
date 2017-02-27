# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addNum', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bookId', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('bookName', models.CharField(max_length=40)),
                ('bookPublisher', models.CharField(max_length=40)),
                ('bookAuthor', models.CharField(max_length=50)),
                ('bookIntroduction', models.TextField()),
                ('bookPrice', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookNum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookNum', models.IntegerField()),
                ('bookId', models.ForeignKey(to='main.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('TypeNum', models.IntegerField(serialize=False, primary_key=True)),
                ('TypeName', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BorrowItem',
            fields=[
                ('borrowItemId', models.IntegerField(serialize=False, primary_key=True)),
                ('hasReturned', models.BooleanField(default=False)),
                ('bookId', models.ForeignKey(to='main.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaffInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staffName', models.CharField(max_length=30)),
                ('staffId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=25)),
                ('userSex', models.BooleanField(default=True)),
                ('userAge', models.IntegerField()),
                ('userPhoneNum', models.CharField(max_length=12, null=True, blank=True)),
                ('userRegistTime', models.DateField(auto_now_add=True)),
                ('userId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='borrowitem',
            name='staffId',
            field=models.ForeignKey(to='main.StaffInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='borrowitem',
            name='userId',
            field=models.ForeignKey(to='main.UserInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='bookType',
            field=models.ForeignKey(to='main.BookType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='additem',
            name='bookId',
            field=models.ForeignKey(to='main.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='additem',
            name='staffId',
            field=models.ForeignKey(to='main.StaffInfo'),
            preserve_default=True,
        ),
    ]
