# Generated by Django 3.1.1 on 2020-09-15 05:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200907_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('g', 'Gents'), ('l', 'Ladies'), ('b', 'Boys'), ('k', 'Kids'), ('c', 'Children'), ('x', 'Giants'), ('i', 'Infant')], max_length=1)),
                ('artid', models.CharField(max_length=12, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('basic', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('active', models.BooleanField(default=True)),
                ('export', models.BooleanField(default=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.article')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.color')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
