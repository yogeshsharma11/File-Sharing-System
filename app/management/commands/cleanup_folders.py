from django.core.management.base import BaseCommand
from app.models import Folder
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cleanup folders without users'

    def handle(self, *args, **kwargs):
        # Option 1: Delete folders without users
        Folder.objects.filter(user__isnull=True).delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up folders')) 