# Generated by Django 2.2.4 on 2019-08-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_product_exploitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.TextField(default=''),
        ),
    ]
