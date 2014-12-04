#!/usr/bin/env python3.4
import os
import sys

from colorama import init as color_init
from colorama import Fore, Style
from pathlib import Path


def activate_env():
    """ Activates the virtual environment for this project."""

    try:
        virtualenv_dir = Path(os.environ['WORKON_HOME'])
    except KeyError:
        error_msg = "Error: 'WORKON_HOME' is not set."
        sys.stderr.write(Fore.RED + Style.BRIGHT + error_msg + "\n")
        sys.exit(1)

    filepath = Path(__file__).resolve()
    repo_dir = filepath.parents[1].stem

    # Add the app's directory to the PYTHONPATH
    sys.path.append(filepath.parent)

    # Activate the virtual env
    # Check for Windows directory, otherwise use Linux directory
    activate_env = virtualenv_dir.joinpath(repo_dir, "Scripts", "activate_this.py")

    if not activate_env.exists():
        activate_env = virtualenv_dir.joinpath(repo_dir, "bin", "activate_this.py")

    exec(compile(open(activate_env).read(), activate_env, 'exec'), dict(__file__=activate_env))

if __name__ == "__main__":

    # Set this manually in the environment
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    color_init()
    activate_env()

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        sys.stderr.write(Fore.RED + Style.BRIGHT + "Error: Django could not be imported - please make sure it is installed.\nIf you are using a Virtual Environment, please make sure it is activated.\n\n")
        sys.exit(1)

    execute_from_command_line(sys.argv)
