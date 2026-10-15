import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    if len(sys.argv) == 1:
        sys.argv.append("runserver")
    execute_from_command_line(sys.argv)
