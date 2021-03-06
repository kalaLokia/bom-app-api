# Generated by Django 3.1 on 2020-09-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='brand',
            field=models.CharField(blank=True, choices=[('pride', 'Pride'), ('debongo', 'Debongo'), ('smartak', 'Smartak'), ('stile', 'Stile'), ('lpride', 'L. Pride'), ('disney', 'Disney'), ('batman', 'Batman'), ('kapers', 'Kapers'), ('', 'None')], max_length=25),
        ),
        migrations.AlterField(
            model_name='article',
            name='style',
            field=models.CharField(blank=True, choices=[('v-strap', 'V-STRAP'), ('sandal', 'SANDAL'), ('t-strap', 'T-STRAP'), ('covering', 'COVERING'), ('shoes', 'SHOES'), ('', 'None')], max_length=25),
        ),
    ]
