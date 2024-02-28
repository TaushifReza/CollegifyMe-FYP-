# Generated by Django 5.0 on 2024-02-27 08:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_studentfriends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='cover_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='coverImage'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='profileImage'),
        ),
    ]