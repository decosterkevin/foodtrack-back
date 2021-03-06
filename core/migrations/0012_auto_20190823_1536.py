# Generated by Django 2.2.4 on 2019-08-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190823_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='')),
                ('name', models.CharField(default='', max_length=120)),
            ],
        ),
        migrations.RemoveField(
            model_name='productorprofile',
            name='pictures',
        ),
        migrations.AddField(
            model_name='productorprofile',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='core.MyImage'),
        ),
    ]
