# Generated by Django 2.1.2 on 2018-10-21 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='device',
        ),
    ]