# Generated by Django 2.2 on 2019-04-25 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obdService', '0015_auto_20190331_0534'),
    ]

    operations = [
        migrations.AddField(
            model_name='carobddata',
            name='MAFLevel',
            field=models.FloatField(default=0),
        ),
    ]
