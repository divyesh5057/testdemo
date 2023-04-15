# Generated by Django 4.1.3 on 2023-03-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_count_user_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image_url',
            new_name='profilei_image',
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
