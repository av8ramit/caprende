#!/usr/bin/env python
'''Basic manager functionality for Django.'''
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caprende.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
