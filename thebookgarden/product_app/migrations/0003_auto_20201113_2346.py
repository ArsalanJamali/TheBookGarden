# Generated by Django 3.0.4 on 2020-11-13 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_book_bookimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='book_author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='product_app.Author', verbose_name='Author Name'),
        ),
    ]
