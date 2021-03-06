# Generated by Django 2.2.4 on 2019-08-16 14:05

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.TextField()),
                ('street_cp', models.TextField(default='')),
                ('city', models.TextField()),
                ('province', models.TextField()),
                ('code', models.TextField()),
                ('country', models.TextField()),
                ('point', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(6.14569, 46.20222), srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Exploitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pictures', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to=''), blank=True, size=None)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Address')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('product_code', models.CharField(default='', max_length=120)),
                ('picture', models.FileField(upload_to='')),
                ('price', models.FloatField(default=0.0)),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(default='')),
                ('is_deliverable', models.BooleanField(default=True)),
                ('delivery_time_days', models.IntegerField(default=7)),
                ('is_pickup', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exploitation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Exploitation')),
                ('pickup_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pickup_location', to='core.Address')),
            ],
        ),
    ]
