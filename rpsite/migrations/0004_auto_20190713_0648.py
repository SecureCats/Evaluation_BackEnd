# Generated by Django 2.2.3 on 2019-07-13 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpsite', '0003_auto_20190713_0620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['id']},
        ),
    ]
