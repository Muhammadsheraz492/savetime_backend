# Generated by Django 4.1.13 on 2024-06-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(default='', max_length=100)),
                ('lastname', models.CharField(default='', max_length=100)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('profile_image', models.CharField(blank=True, max_length=225, null=True)),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=200)),
            ],
            options={
                'db_table': 'Buyer_User',
            },
        ),
    ]