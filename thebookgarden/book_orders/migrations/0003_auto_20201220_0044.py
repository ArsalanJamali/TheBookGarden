# Generated by Django 3.0.4 on 2020-12-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_orders', '0002_auto_20201219_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(choices=[(0, 'Not Paid'), (1, 'Paid')], default=0),
        ),
    ]