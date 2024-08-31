from colorama import Fore, Style, init, Back
import os
from custom_functions import *
from shutil import copyfile
import requests

url = "https://raw.githubusercontent.com/NSPC911/search/main/search.config.json"

init(strip=False, convert=False, autoreset=True)

config_path = f"{os.path.dirname(os.path.realpath(__file__))}{os.path.sep}search.config.json"
def config(readorwrite, key, changeto="", is_theme=False):
    cnfg = load_json(config_path) # Will be changeable
    if readorwrite == "read":
        if is_theme:
            # Invalid Foreground Color
            try:
                fg_color = Fore.__dict__[cnfg[f'{key}.foreground'].upper()]
            except KeyError:
                print(f"{Fore.RED}ConfigError: Invalid color for `{Fore.MAGENTA}{key}.{Style.BRIGHT}foreground{Fore.RED}{Style.NORMAL}` in config.")
                print(f"{Fore.YELLOW}Refer to https://pypi.org/project/colorama/ for valid colors.")
                exit(1)
            # Invalid Background Color
            try:
                bg_color = Back.__dict__[cnfg[f'{key}.background'].upper()]
            except KeyError:
                print(f"{Fore.RED}ConfigError: Invalid color for `{Fore.MAGENTA}{key}.{Style.BRIGHT}background{Fore.RED}{Style.NORMAL}` in config.")
                print(f"{Fore.YELLOW}Refer to https://pypi.org/project/colorama/ for valid colors.")
                exit(1)
            # Invalid Style Type
            try:
                style = Style.__dict__[cnfg[f'{key}.style'].upper()]
            except KeyError:
                print(f"{Fore.RED}ConfigError: Invalid color for `{Fore.MAGENTA}{key}.{Style.BRIGHT}style{Fore.RED}{Style.NORMAL}` in config.")
                print(f"{Fore.YELLOW}Refer to https://pypi.org/project/colorama/ for valid styles.")
                exit(1)
            return f"{fg_color}{bg_color}{style}"
        else:
            try:
                return cnfg[key]
            except KeyError:
                print(f"{Fore.RED}KeyError: `{key}` not found in search.config.json")
                exit(1)
    elif readorwrite == "write":
        cnfg[key] = changeto
        dump_json("search.config.json",cnfg)
        print(f"{Fore.GREEN}Set `{Fore.CYAN}{key}{Fore.GREEN}` to {Fore.MAGENTA}{changeto}")


def reset():
    return f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}" 

if config("read","default.context") < 0:
    print(f"{Fore.RED}RangeError: `default.context` in search.config.json is less than 0.")
    exit(0)

def configure(listarg):
    try:
        listarg[1]
    except IndexError:
        print(f"{Fore.RED}FlagError: Expected modifier keyword after `--config` but received None")
        exit(1)
    try:
        listarg[2]
    except IndexError:
        if listarg[1] == "update":
            response = requests.get(url)
            if response.status_code == 200:
                remote_config = response.json()
                current_config = load_json(config_path)
                new_config = {**remote_config, **current_config}
                dump_json(config_path,new_config)
                print(f"{Fore.GREEN}Updated search.config.json from `{Fore.BLUE}{url}{Fore.GREEN}`")
            else:
                print(f"{Fore.RED}RequestError: Couldn't fetch data from {url}")
                exit(1)
            return
        elif listarg[1] == "reset":
            response = requests.get(url)
            if response.status_code == 200:
                dump_json(config_path,response.json())
                print(f"{Fore.GREEN}Reset search.config.json to default from `{Fore.BLUE}{url}{Fore.GREEN}`")
            else:
                print(f"{Fore.RED}RequestError: Couldn't fetch data from {url}")
                exit(1)
            return
        elif listarg[1] != "list":
            print(f"{Fore.RED}FlagError: Expected key to `{listarg[1]}` but received None")
            exit(1)
    try:
        last = listarg.pop().split()
        listarg.extend(last)
        if listarg[1] == "set":
            if listarg[3].lower() == "true":
                config("write",listarg[2],True)
            elif listarg[3].lower() == "false":
                config("write",listarg[2],False)
            else:
                if listarg[3].isnumeric():
                    config("write",listarg[2],int(listarg[3]))
                else:
                    config("write",listarg[2],listarg[3].lower())
        elif listarg[1] == "read":
            raise IndexError
        elif listarg[1] == "list":
            raise IndexError
    except IndexError:
        if listarg[1] == "set":
            print(f"{Fore.RED}FlagError: Expected value to set to `{listarg[2]}` but received None")
            exit(1)
        elif listarg[1] == "read":
            print(f"`{Fore.CYAN}{listarg[2]}{Fore.WHITE}` is set as {Fore.MAGENTA}{config('read',listarg[2])}")
            if listarg[2].startswith("clr") and (listarg[2].endswith("foreground") or listarg[2].endswith("background")):
                print(f"Allowed definitions: {Fore.RED}red, {Fore.GREEN}green, {Fore.YELLOW}yellow, {Fore.BLUE}blue, {Fore.MAGENTA}magenta, {Fore.CYAN}cyan, {Fore.WHITE}white, {Fore.BLACK}black")
            elif listarg[2].startswith("clr") and listarg[2].endswith("style"):
                print(f"Allowed definitions: {Style.BRIGHT}BRIGHT, {Style.NORMAL}NORMAL, {Style.DIM}DIM, {Style.RESET_ALL}RESET_ALL")
            elif listarg[2] in ["default.include_filename","default.in_cwd","first_run","easter_errors"]:
                print(f"Allowed definitions: {Fore.MAGENTA}True, {Fore.MAGENTA}False")
            elif listarg[2] == "default.context":
                print(f"Allowed definitions: Any integer above 0")
        elif listarg[1] == "list":
            print(f"{Fore.GREEN}Listing all keys in search.config.json:")
            for key in load_json(config_path):
                print(f"{Fore.CYAN}{key}{Fore.WHITE} is set as {Fore.MAGENTA}{config('read',key)}")
        else:
            print(f"{Fore.RED}FlagError: Expected `list`, `read` or `write` after `--config` but received {listarg[1]}")
            exit(1)

if f"scoop{os.path.sep}apps" in config_path:
    if not os.path.exists(f"{os.path.expanduser("~")}{os.path.sep}persist{os.path.sep}search.config.json"):
        copyfile(config_path,f"{os.path.expanduser('~')}{os.path.sep}persist{os.path.sep}search.config.json")
        config_path = f"{os.path.expanduser('~')}{os.path.sep}persist{os.path.sep}search.config.json"
    
    