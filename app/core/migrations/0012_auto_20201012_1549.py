# Generated by Django 3.1.1 on 2020-10-12 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20201012_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='cf',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=12),
        ),
    ]
