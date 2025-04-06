from django.core.management.base import BaseCommand
from marketplace.models import AvailabilityType

class Command(BaseCommand):
    help = "Seeds predefined availability types: Sale, Donation, Exchange"

    def handle(self, *args, **kwargs):
        options = ['Sale', 'Donation', 'Exchange']
        for name in options:
            obj, created = AvailabilityType.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created availability type: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {name}"))
