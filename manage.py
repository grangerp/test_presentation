#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":  # pragma: no cover
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "test_presentation.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)