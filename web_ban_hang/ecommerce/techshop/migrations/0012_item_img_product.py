# Generated by Django 3.1.2 on 2020-10-26 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techshop', '0011_auto_20201026_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img_product',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
