# Generated by Django 2.2.3 on 2019-07-13 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpsite', '0005_remove_evaluation_semaster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationitem',
            name='question',
        ),
    ]
