# Generated by Django 2.0.6 on 2019-04-20 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0010_auto_20190420_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ouwang',
            name='ctt',
            field=models.CharField(db_column='content', max_length=10000, verbose_name='文章内容'),
        ),
    ]
