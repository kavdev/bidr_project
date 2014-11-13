#!/usr/bin/env python

import sys

if __name__ == "__main__":

    # Load the Heroku environment.
    from herokuapp.env import load_env
    load_env(__file__, "bidr")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
