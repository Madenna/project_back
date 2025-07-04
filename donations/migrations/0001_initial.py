# Generated by Django 4.2.19 on 2025-06-22 15:30

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userauth', '0004_alter_user_temp_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='child_photo')),
                ('purpose', models.TextField()),
                ('goal_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('donated_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('kaspi_code', models.CharField(blank=True, max_length=6, unique=True)),
                ('kaspi_qr', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='kaspi_qr')),
                ('deadline', models.DateField()),
                ('is_approved', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='userauth.child')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DonationConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comment', models.TextField(blank=True)),
                ('donated_at', models.DateTimeField(auto_now_add=True)),
                ('donation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='donations.donationrequest')),
                ('donor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
