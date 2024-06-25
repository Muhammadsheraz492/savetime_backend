# Generated by Django 4.1.13 on 2024-06-25 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gig_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image_url', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gig', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='common.gigdata')),
            ],
            options={
                'db_table': 'Gig_images',
            },
        ),
    ]
