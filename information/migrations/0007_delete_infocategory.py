# Generated by Django 4.2.19 on 2025-04-26 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_news_newscomment_specialist_specialistcomment_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InfoCategory',
        ),
    ]
