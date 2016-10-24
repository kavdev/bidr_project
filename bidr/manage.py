#!/usr/bin/env python
import ast
import os
from pathlib import Path
import site
import sys

from colorama import init as color_init
from dotenv import find_dotenv, load_dotenv
from termcolor import colored


def get_env_variable(name, default=None, console=False):
    """ Gets the specified environment variable.

    :param name: The name of the variable.
    :type name: str
    :param console: Whether or not this is run via the console or from within django.
    :type console: bool
    :returns: The value of the specified variable.
    :raises: **ImproperlyConfigured** when the specified variable does not exist.

    """

    try:
        variable = os.environ[name]
    except KeyError:
        if default is not None:
            return default

        error_msg = "The {variable_name} environment variable is not set!\n".format(variable_name=name)

        if console:
            color_init()
            sys.stderr.write(colored(text="ImproperlyConfigured: " + error_msg, color='red', attrs=['bold']))
            sys.exit(1)
        else:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(error_msg)
    else:
        try:
            return ast.literal_eval(variable)
        except:
            return variable


def activate_env():
    """ Activates the virtual environment for this project."""

    filepath = Path(__file__).resolve()
    repo_name = filepath.parents[1].name
    project_name = filepath.parents[0].name

    # Add the app's directory to the PYTHONPATH
    sys.path.append(str(filepath.parents[1]))
    sys.path.append(str(filepath.parents[1].joinpath(project_name)))

    if "WORKON_HOME" in os.environ:  # Only activate the environment if virtualenvwrapper is installed.
        # Add the site-packages of the chosen virtualenv to work with
        virtualenv_home = Path(get_env_variable("WORKON_HOME", console=True))
        site.addsitedir(str(virtualenv_home.joinpath(repo_name, "Lib", "site-packages")))

        # Load .env file
        load_dotenv(find_dotenv())

        # Activate the virtual env
        activate_env = virtualenv_home.joinpath(repo_name, "bin", "activate_this.py")

        exec(compile(open(str(activate_env)).read(), str(activate_env), 'exec'), dict(__file__=str(activate_env)))


if __name__ == "__main__":
    if "test" in sys.argv:
        # Switch to the test settings file
        os.environ["DJANGO_SETTINGS_MODULE"] = "bidr.settings.test"

    color_init()
    activate_env()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
