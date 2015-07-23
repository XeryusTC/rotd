from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from recipes import factories

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = factories.RecipeFactory()
        r.save()
