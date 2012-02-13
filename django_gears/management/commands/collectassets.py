from django.core.management.base import NoArgsCommand
from django_gears.settings import environment


class Command(NoArgsCommand):

    help = 'Collect assets in a single location.'

    def handle_noargs(self, **options):
        environment.save()
