# Generated by Django 2.0.3 on 2019-03-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obdService', '0002_carobddata_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='carobddata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
