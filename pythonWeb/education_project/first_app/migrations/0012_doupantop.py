# Generated by Django 2.0.6 on 2019-05-15 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0011_auto_20190420_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoupanTop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_column='title', max_length=100, null=True)),
                ('movieInfo', models.CharField(blank=True, db_column='movieInfo', max_length=100, null=True)),
                ('star', models.CharField(blank=True, db_column='star', max_length=100, null=True)),
                ('quote', models.CharField(blank=True, db_column='quote', max_length=100, null=True)),
            ],
            options={
                'verbose_name': '豆瓣',
                'verbose_name_plural': '豆瓣',
                'ordering': ['title'],
            },
        ),
    ]
