# Generated by Django 4.1.3 on 2023-03-20 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_admin_banners'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='admin_banners',
            new_name='AdminBanners',
        ),
    ]
