# Generated by Django 2.2.6 on 2019-12-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busTicketBooking', '0004_auto_20191208_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
