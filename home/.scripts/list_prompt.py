# A dmenu list prompt script.
# Gives a dmenu with items taken from a yml file.
# For example:
# `./list_prompt $HOME/.config/shortcuts/file.yml

import subprocess
import yaml
import sys
import jsonschema
import dmenu

from yaml import scanner
from jsonschema import validate
from os import path
from pathlib import Path

WAL_CACHE_DIR = path.join(str(Path.home()), '.cache/wal/')

def manage_call(command_array, shell):
    subprocess.run(command_array, shell=shell)

def build_command(option):
    command_array = []
    shell = True
    if option['command'] != '/bin/sh':
        shell = False
        command_array.append(option['command'])
    command_array.extend(option['args'])
    return [ command_array, shell ]

def list_prompt(param_dict):
    title = param_dict['title']
    options = param_dict['options']
    option_labels = options.keys()
    with open(path.join(WAL_CACHE_DIR, 'colors.yml'), 'r') as wal_file:
        wal_params = yaml.safe_load(wal_file)
        choice = dmenu.show(
            prompt=title,
            items=options,
            background=wal_params['colors']['color0'],
            foreground=wal_params['colors']['color15'],
            background_selected=wal_params['colors']['color1'],
            foreground_selected=wal_params['colors']['color15'],
            font="terminus",
            case_insensitive=True
        )
        [ command_array, shell ] = build_command(options[choice])
        manage_call(command_array, shell)       


schema = """
type: object
additionalProperties: false
properties:
  title:
    type: string
  options:
    type: object
    patternProperties:
      "^.*$":
        type: object
        additionalProperties: false
        properties:
            command:
                type: string
            args:
                type: array
                items:
                    type: string
"""

def main():
    args = sys.argv
    if len(args) < 2:
        print("A param is required")
        sys.exit(1)
    file_path = args[1]
    if not path.isfile(file_path):
        print("The specified file at {} does not exist".format(file_path))
        sys.exit(1)
    with open(file_path, "r") as argfile:
        try:
            loaded = yaml.safe_load(argfile)
            validate(loaded, yaml.safe_load(schema))
            list_prompt(loaded)
        except scanner.ScannerError:
            print("Failed to parse yaml file")
            sys.exit(1)
        except jsonschema.exceptions.ValidationError:
            print("Failed to validate yaml file")
            sys.exit(1)
        except Exception as e:
            print("Failed unexpectedly")
            print(e)
            sys.exit(1)

if __name__ == "__main__":
    main()
