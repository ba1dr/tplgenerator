#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    dirname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(dirname))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{os.path.basename(dirname)}.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
