from django.core.management.base import BaseCommand
from forum.models import DiscussionCategory

class Command(BaseCommand):
    help = 'Seeds predefined discussion categories for the forum'

    def handle(self, *args, **kwargs):
        categories = [
            "Child's Condition & Diagnosis",
            "Therapy & Treatment",
            "Education & Learning Support",
            "Parenting & Daily Life",
            "Community & Socialization",
            "Legal & Financial Assistance",
            "Technology & Accessibility"
        ]

        for name in categories:
            DiscussionCategory.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("✅ Forum categories have been successfully seeded."))
