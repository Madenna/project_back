# Generated by Django 4.2.19 on 2025-04-19 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_alter_equipmentitem_condition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conditiontype',
            old_name='label',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='conditiontype',
            name='key',
        ),
    ]
