# Generated by Django 4.1.3 on 2022-11-14 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_product_product_type_alter_product_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_img',
            new_name='profile_image',
        ),
    ]