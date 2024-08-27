import os
import importlib
import pip
from pip import main
import time
import traceback
from colorama import Fore, Style, init, Back
from shutil import get_terminal_size as t_size
import re

# If I need a module that isn't installed
def check(module, module_name=""):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        print(f"{module} is not installed!")
        if module_name == "":
            # Using pip instead of subprocess as calling
            # with terminal results in an error
            pip.main(["install", module])
        else:
            # Using pip instead of subprocess as calling
            # with terminal results in an error
            pip.main(["install", module_name])
        time.sleep(1)


check("json5", "json-five")
from json5 import *

# Simple function to load json from file
def load_json(path):
    with open(path, "r") as file:
        try:
            return loads(file.read())
        except JSONDecodeError:
            print(f"\n{Fore.RED}{path} got a JSON Decode Error")
            print(f"{Fore.YELLOW}{traceback.format_exc()}")
            exit()


# Simple function to save json into file
def dump_json(path, dictionary):
    the_json = dumps(dictionary, indent=2)
    the_json = the_json.replace(r"\/","/")
    with open(path, "w") as file:
        file.write(the_json)

# Function to clear a line
def clear_line(withchar=' ', end=""):
    print(f"\r{t_size().columns * withchar}", end=end)

# Function to check whether a file is binary
def is_binary(file_path):
    try:
        with open(file_path, 'rb') as f:
            for byte in f.read(1024):
                if byte > 127:
                    return True
        return False
    except:
        return True


def config(readorwrite, key, changeto=""):
    cnfg = load_json(f"{os.path.dirname(os.path.realpath(__file__))}/search.config.json")
    if readorwrite == "read":
        if "clr" in key:
            if "foreground" in key:
                return Fore.__dict__[cnfg[key].upper()]
            elif "background" in key:
                return Back.__dict__[cnfg[key].upper()]
        else:
            return cnfg[key]
    elif readorwrite == "write":
        cnfg[key] = changeto
        dump_json("search.config.json",cnfg)

def replace_unicode(match):
    return chr(int(match.group(0)[2:], 16))

def reset():
    return f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}" 