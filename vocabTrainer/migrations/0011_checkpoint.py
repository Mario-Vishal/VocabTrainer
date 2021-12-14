# Generated by Django 3.1.3 on 2021-04-18 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocabTrainer', '0010_auto_20210416_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='checkPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_marked', models.BooleanField(default=False)),
                ('word_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocabTrainer.vocabcard')),
            ],
        ),
    ]
