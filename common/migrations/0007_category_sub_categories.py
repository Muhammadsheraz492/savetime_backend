# Generated by Django 4.1.13 on 2024-06-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_remove_category_sub_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sub_categories',
            field=models.ManyToManyField(related_name='categories', to='common.subcategory'),
        ),
    ]
