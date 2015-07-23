from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('email')

    def handle(self, *args, **options):
        call_command('createsuperuser', username=options['username'],
                email=options['email'], interactive=False)
        u = User.objects.get(username=options['username'])
        u.set_password(options['password'])
        u.save()
