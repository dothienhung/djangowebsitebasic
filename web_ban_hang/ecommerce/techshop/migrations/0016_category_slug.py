# Generated by Django 3.1.2 on 2020-10-27 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techshop', '0015_auto_20201027_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='cat_id'),
            preserve_default=False,
        ),
    ]
