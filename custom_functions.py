import os
import importlib
import pip
from pip import main
import time
import traceback
from colorama import Fore, init
from shutil import get_terminal_size as t_size

init(strip=False, convert=False, autoreset=True)

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


check("ujson")
from ujson import *
check("requests")

# Simple function to load json from file
def load_json(path):
    with open(path, "r") as file:
        try:
            return loads(file.read())
        except JSONDecodeError:
            print(f"\n{Fore.RED}{path} got a JSON5 Decode Error!")
            print(f"Redownload from https://github.com/NSPC911/scripts/blob/main/search.config.json if you can't fix it!")
            print(f"{Fore.YELLOW}{traceback.format_exc()}")
            exit()


# Simple function to save json into file
def dump_json(path, dictionary):
    the_json = dumps(dictionary, indent=4)
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

def replace_unicode(match):
    return chr(int(match.group(0)[2:], 16))