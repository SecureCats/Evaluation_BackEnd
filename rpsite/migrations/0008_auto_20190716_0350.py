# Generated by Django 2.2.3 on 2019-07-16 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpsite', '0007_auto_20190714_0146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='semeser',
            new_name='semester',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='evaluated',
            field=models.BooleanField(default=False, verbose_name='是否已评'),
        ),
    ]
