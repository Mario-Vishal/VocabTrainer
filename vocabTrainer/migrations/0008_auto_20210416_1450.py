# Generated by Django 3.1.3 on 2021-04-16 09:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vocabTrainer', '0007_auto_20210416_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabcard',
            name='date_added',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
