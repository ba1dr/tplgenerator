
DESCRIPTION = """

"""

import logging

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (DESCRIPTION)

    def add_arguments(self, parser):
        parser.add_argument('-i', '--inputfile', help='Input file', required=True)

    def handle(self, *args, **options):
        pass
