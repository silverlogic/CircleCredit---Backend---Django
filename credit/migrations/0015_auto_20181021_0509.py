# Generated by Django 2.1.2 on 2018-10-21 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0014_auto_20181021_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('ACTIVE', 'active'), ('PAID', 'paid')], default='PENDING', max_length=12),
        ),
        migrations.AlterField(
            model_name='vouch',
            name='status',
            field=models.CharField(choices=[('INVITED', 'invited'), ('ACCEPTED', 'accepted'), ('DECLINED', 'declined')], default='INVITED', max_length=12),
        ),
    ]
