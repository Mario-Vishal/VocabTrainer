# Generated by Django 3.1.3 on 2021-04-16 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabTrainer', '0009_auto_20210416_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabcard',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]