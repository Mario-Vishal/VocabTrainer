# Generated by Django 3.1.3 on 2021-04-19 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabTrainer', '0014_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='word_id',
            field=models.IntegerField(),
        ),
    ]
