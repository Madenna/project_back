from django.core.management.base import BaseCommand
from information.models import InfoCategory

class Command(BaseCommand):
    help = "Seeds default Info Hub categories"

    def handle(self, *args, **kwargs):
        default_categories = ["News", "Specialists", "Therapy Centers"]
        for name in default_categories:
            category, created = InfoCategory.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created category: {name}"))
            else:
                self.stdout.write(f"ℹ️ Already exists: {name}")