# Generated by Django 4.1.13 on 2024-06-18 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='GigMetaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=100)),
                ('has_nested_gig_metadata', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'GigMetaData',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('has_nested_gig_metadata', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ServiceType',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('has_nested_gig_metadata', models.BooleanField()),
                ('service_type', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_subcategories', to='common.category')),
                ('service_type_data', models.ManyToManyField(related_name='subcategories', to='common.servicetype')),
            ],
            options={
                'db_table': 'Subcategory',
            },
        ),
        migrations.AddField(
            model_name='servicetype',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_types', to='common.subcategory'),
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gig_meta_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_options', to='common.gigmetadata')),
            ],
            options={
                'db_table': 'Options',
            },
        ),
        migrations.AddField(
            model_name='gigmetadata',
            name='options',
            field=models.ManyToManyField(related_name='metadata', to='common.options'),
        ),
        migrations.AddField(
            model_name='gigmetadata',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='common.servicetype'),
        ),
        migrations.AddField(
            model_name='gigmetadata',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='common.subcategory'),
        ),
        migrations.AddField(
            model_name='category',
            name='sub_categories',
            field=models.ManyToManyField(related_name='categories', to='common.subcategory'),
        ),
    ]