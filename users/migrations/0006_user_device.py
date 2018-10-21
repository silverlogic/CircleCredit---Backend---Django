# Generated by Django 2.1.2 on 2018-10-21 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_django', '0003_auto_20170313_1314'),
        ('users', '0005_auto_20181021_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='fcm_django.FCMDevice'),
        ),
    ]