#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Delivery_Project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


'''import os
import sys
import json


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Delivery_Project.settings')

    # # Default environment
    # environment = os.environ.get('DJANGO_ENV', 'development')
    # print(environment)

    if not os.environ.get('DJANGO_ENV'):
        #default environment
        environment = 'development'

        # Look for --env= argument in sys.argv
        print(sys.argv)
        for arg in sys.argv:
            print(arg)
            if arg.startswith('--env='):
                environment = arg.split('=')[1]
                print(environment)
                # Remove --env= argument from sys.argv
                sys.argv.remove(arg)
                os.environ['DJANGO_ENV'] = environment #set the environment variable
                break
    else:
        environment = os.environ.get('DJANGO_ENV')

    # Load configuration from file
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Error: 'config.json' file not found.")
        sys.exit(1)

    # Get the port based on the environment
    port = config.get(environment, {}).get('port', '8000')
    print(port)

    # Ensure 'runserver' is in sys.argv and update the port
    if 'runserver' in sys.argv:
        # Find the index of 'runserver' and update the following argument to the port
        runserver_index = sys.argv.index('runserver')
        if runserver_index + 1 < len(sys.argv):
            sys.argv[runserver_index + 1] = f'0.0.0.0:{port}'
        else:
            sys.argv.append(f'0.0.0.0:{port}')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''