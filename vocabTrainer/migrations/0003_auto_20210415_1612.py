# Generated by Django 3.1.3 on 2021-04-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabTrainer', '0002_auto_20210415_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocabcard',
            name='vocab_learn',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vocabcard',
            name='vocab_word_bookmarked',
            field=models.BooleanField(default=False),
        ),
    ]
