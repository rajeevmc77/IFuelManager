# Generated by Django 2.0.3 on 2019-03-23 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obdService', '0004_carobddata_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carobddata',
            options={'verbose_name': 'CarOBDData', 'verbose_name_plural': 'CarOBDData'},
        ),
        migrations.AlterModelOptions(
            name='carprofile',
            options={'verbose_name': 'CarProfile', 'verbose_name_plural': 'CarProfile'},
        ),
        migrations.RemoveField(
            model_name='carobddata',
            name='profile',
        ),
    ]
