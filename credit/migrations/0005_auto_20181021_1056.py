# Generated by Django 2.1.2 on 2018-10-21 10:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0004_auto_20181021_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 20, 10, 56, 23, 331099, tzinfo=utc), null=True),
        ),
    ]
