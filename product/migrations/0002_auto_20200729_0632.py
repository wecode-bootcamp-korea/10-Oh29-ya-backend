# Generated by Django 3.0.8 on 2020-07-29 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_subcategory',
            new_name='subcategory',
        ),
        migrations.AlterModelTable(
            name='likeproduct',
            table='likes_products',
        ),
    ]
