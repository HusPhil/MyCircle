from django.core.management.base import BaseCommand
from mycircle_app.models import Circle  # Replace 'mycircle_app' with the name of your app

class Command(BaseCommand):
    help = 'Deletes all existing circles'

    def handle(self, *args, **kwargs):
        try:
            Circle.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted all circles'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
