# Generated by Django 3.1.3 on 2021-04-15 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabTrainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabcard',
            name='vocab_synonyms',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
