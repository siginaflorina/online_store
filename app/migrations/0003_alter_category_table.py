# Generated by Django 4.1.3 on 2022-11-09 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_category_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='app_category',
        ),
    ]
