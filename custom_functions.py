import time, traceback, sys
from subprocess import run
from shutil import get_terminal_size as t_size

# If I need a module that isn't installed
def install(module, module_name=""):
    print(f"{module} is not installed!")
    if module_name == "":
    # Using pip instead of subprocess as calling
    # with terminal results in an error
        run([sys.executable, "-m", "pip", "install", module, "--quiet"], check=True)
        #pip.main(["install", module, "--quiet"])
    else:
        run([sys.executable, "-m", "pip", "install", module_name, "--quiet"], check=True)
        #pip.main(["install", module_name, "--quiet"])
    print(f"Installed {module}!")
    time.sleep(1)

# It becomes really slow for some reason, I'm not really sure why
try:
    from ujson import *
except ModuleNotFoundError:
    install("ujson")
    from ujson import *
try:
    from colorama import Fore, init
except ModuleNotFoundError:
    install("colorama")
    from colorama import Fore, init
init(strip=False, convert=False, autoreset=True)

# Simple function to load json from file
def load_json(path):
    with open(path, "r") as file:
        try:
            return loads(file.read())
        except JSONDecodeError:
            print(f"\n{Fore.RED}{path} got a JSON Decode Error!")
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