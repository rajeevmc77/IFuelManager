# Generated by Django 2.0.3 on 2019-03-24 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obdService', '0007_auto_20190324_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carjsonobddata',
            name='data',
        ),
        migrations.AddField(
            model_name='carjsonobddata',
            name='RPM',
            field=models.CharField(default=' ', max_length=4),
        ),
        migrations.AddField(
            model_name='carjsonobddata',
            name='Speed',
            field=models.CharField(default=' ', max_length=4),
        ),
    ]
