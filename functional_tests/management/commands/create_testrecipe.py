from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import random
import string
from recipes.models import Recipe

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = Recipe(name=''.join(random.choice(string.ascii_letters) for _
            in range(10)), description='description')
        r.save()
