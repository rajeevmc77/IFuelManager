# Generated by Django 2.0.3 on 2019-03-22 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obdService', '0003_carobddata_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='carobddata',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obdService.CarProfile'),
        ),
    ]
