# Generated by Django 2.2.4 on 2019-08-21 09:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20190821_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorprofile',
            name='pictures',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to=''), default=list, size=None),
        ),
    ]
