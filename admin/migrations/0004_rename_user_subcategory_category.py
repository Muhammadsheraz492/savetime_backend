# Generated by Django 4.1.13 on 2024-06-14 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_remove_subcategory_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='user',
            new_name='category',
        ),
    ]