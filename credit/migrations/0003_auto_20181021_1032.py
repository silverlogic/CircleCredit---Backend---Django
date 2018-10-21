# Generated by Django 2.1.2 on 2018-10-21 10:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0002_auto_20181021_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 20, 10, 32, 2, 974131, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='loan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='investments', to='credit.Loan'),
        ),
    ]