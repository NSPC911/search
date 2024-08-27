import os
import importlib
import pip
from pip import main
import time
import traceback
from colorama import Fore, Style, init
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
            clrprint(f"\n{path} got a JSON Decode Error", clr="red")
            clrprint(traceback.format_exc(), clr="yellow")
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

clrs_colorama = {"Fore.RED": Fore.RED, }
def config(readorwrite, key, changeto):
    cnfg = load_json("search.config.json")
    if readorwrite == "read":
        if "line.clr" in key:
            if cnfg[key] is list:
                for i in range(len(cnfg)):
                    pass
        else:
            return cnfg[key]
    elif readorwrite == "write":
        cnfg[key] = changeto
        dump_json("search.config.json",cnfg)

def replace_unicode(match):
    return chr(int(match.group(0)[2:], 16))