#!/usr/bin/env python
import os
import sys
from __init__ import InitThread

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devicemgt.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    print 123

    InitThread()