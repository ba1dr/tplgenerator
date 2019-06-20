
DESCRIPTION = """

"""

import sys
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from daphne.cli import CommandLineInterface

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (DESCRIPTION)

    def create_parser(self, prog_name, subcommand):
        cli = CommandLineInterface()
        # we need to add these arguments as they're required by django
        cli.parser.add_argument(
            '--settings',
            help=(
                'The Python path to a settings module, e.g. '
                '"myproject.settings.main". If this isn\'t provided, the '
                'DJANGO_SETTINGS_MODULE environment variable will be used.'
            ),
        )
        cli.parser.add_argument(
            '--pythonpath',
            help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".',
        )
        cli.parser.add_argument('--traceback', action='store_true', help='Raise on CommandError exceptions')
        cli.parser.add_argument(
            '--no-color', action='store_true', dest='no_color',
            help="Don't colorize the command output.",
        )
        return cli.parser

    def run_from_argv(self, argv):
        return super().run_from_argv(argv + ['%s.asgi:application' % settings.APP_NAME, ])

    def handle(self, *args, **options):
        cli = CommandLineInterface()
        argv = sys.argv[2:] + ['%s.asgi:application' % settings.APP_NAME]
        if not options['port']:
            argv += ['-p 8001']
        cli.run(argv)
