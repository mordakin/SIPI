# Generated by Django 4.2 on 2023-04-27 13:08
"""1"""
from django.db import migrations, models


class Migration(migrations.Migration):
    """1"""
    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]