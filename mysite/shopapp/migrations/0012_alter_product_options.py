# Generated by Django 4.1.6 on 2023-06-19 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0011_alter_product_description_alter_product_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price', 'created_at']},
        ),
    ]