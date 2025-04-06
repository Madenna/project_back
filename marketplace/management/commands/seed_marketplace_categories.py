from django.core.management.base import BaseCommand
from marketplace.models import EquipmentCategory

class Command(BaseCommand):
    help = "Seeds predefined main categories for the marketplace"

    def handle(self, *args, **kwargs):
        categories = [
            "Mobility Aids",
            "Communication Devices",
            "Therapy Equipment",
            "Daily Living Aids",
            "Medical Devices",
            "Positioning & Seating",
            "Orthotics & Prosthetics",
            "Educational Tools",
            "Transport Equipment",
            "Miscellaneous",
        ]

        for name in categories:
            obj, created = EquipmentCategory.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created category: {name}"))
            else:
                self.stdout.write(f"⚠️ Already exists: {name}")
