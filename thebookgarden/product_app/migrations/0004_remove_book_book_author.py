# Generated by Django 3.0.4 on 2020-11-13 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_auto_20201113_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_author',
        ),
    ]