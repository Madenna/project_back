# Generated by Django 4.2.19 on 2025-03-25 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
