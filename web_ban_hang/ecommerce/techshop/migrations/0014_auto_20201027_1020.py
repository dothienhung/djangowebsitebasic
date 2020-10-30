# Generated by Django 3.1.2 on 2020-10-27 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techshop', '0013_auto_20201027_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_title', models.CharField(blank=True, max_length=100, null=True)),
                ('item_catagory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='techshop.item')),
            ],
        ),
    ]
