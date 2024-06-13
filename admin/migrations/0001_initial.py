# Generated by Django 4.1.13 on 2024-06-13 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100)),
                ('random_access_point', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=200)),
                ('action', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_At')),
            ],
        ),
        migrations.CreateModel(
            name='Admin_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=200)),
                ('devices', models.ManyToManyField(related_name='user_devices', to='admin.admin_device')),
            ],
        ),
        migrations.AddField(
            model_name='admin_device',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_devices', to='admin.admin_user'),
        ),
    ]