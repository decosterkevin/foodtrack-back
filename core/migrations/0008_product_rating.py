# Generated by Django 2.2.4 on 2019-08-21 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190821_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=6.0, max_digits=3),
        ),
    ]
