# Generated by Django 2.2.3 on 2019-07-13 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpsite', '0004_auto_20190713_0648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='semaster',
        ),
    ]