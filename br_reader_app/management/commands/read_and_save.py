from django.core.management.base import BaseCommand, CommandError
from br_reader_app.capture import Capture
class Command(BaseCommand):
    help = 'Capture and save reading to the database'

    def handle(self, *args, **options):
        capturer = Capture()
        capturer.read_and_save()