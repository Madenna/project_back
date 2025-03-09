from django.core.management.base import BaseCommand
from userauth.models import User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes non-verified users older than 1 hours'

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(hours=1)
        deleted_users = User.objects.filter(is_active=False, date_joined__lt=threshold).delete()
        self.stdout.write(f"Deleted {deleted_users[0]} non-verified users.")
