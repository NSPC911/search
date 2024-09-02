from custom_functions import *
import os
from colorama import Fore, Style, init, Back
from shutil import copyfile
init(strip=False, convert=False, autoreset=True)

# I'm not sure why reqests takes the longest time to import
try:
    from requests import get
except ModuleNotFoundError:
    install("requests")
    from requests import get

config_remote_url = "https://raw.githubusercontent.com/NSPC911/search/main/search.config.json"
config_path = f"{os.path.dirname(os.path.realpath(__file__))}{os.path.sep}search.config.json"
if f"scoop{os.path.sep}apps" in config_path:
    if not os.path.exists(f"{os.path.expanduser("~")}{os.path.sep}scoop{os.path.sep}persist{os.path.sep}search.config.json"):
        copyfile(config_path,f"{os.path.expanduser('~')}{os.path.sep}scoop{os.path.sep}persist{os.path.sep}search.config.json")
    config_path = f"{os.path.expanduser('~')}{os.path.sep}scoop{os.path.sep}persist{os.path.sep}search.config.json"

def config(readorwrite, key, changeto="", is_theme=False):
    cnfg = load_json(config_path)
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
        if listarg[2] in ["reset","update","where"]:
            raise IndexError
    except IndexError:
        if listarg[1] == "reset":
            response = get(config_remote_url)
            if response.status_code == 200:
                dump_json(config_path,response.json())
                print(f"{Fore.GREEN}Reset search.config.json to default from remote")
            else:
                print(f"{Fore.RED}RequestError: Couldn't fetch data from remote for {Fore.YELLOW}config.json")
                print(f"{Fore.RED}Please check your internet connection and try again.")
                exit(1)
            return
        elif listarg[1] == "list":
            print(f"{Fore.GREEN}Listing all keys in search.config.json:")
            for key in load_json(config_path):
                print(f"{Fore.CYAN}{key}{Fore.WHITE} is set as {Fore.MAGENTA}{config('read',key)}")
        elif listarg[1] == "where":
            print(f"{Fore.GREEN}search.config.json is located at {Fore.CYAN}{config_path}")
        else:
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
            print(f"`{Fore.CYAN}{listarg[2]}{Fore.WHITE}` is set as {Fore.MAGENTA}{config('read',listarg[2])}")
            if listarg[2].startswith("clr") and listarg[2].endswith("foreground"):
                print(f"Allowed definitions:\n{Fore.RED}red, {Fore.GREEN}green, {Fore.YELLOW}yellow, {Fore.BLUE}blue, {Fore.MAGENTA}magenta, {Fore.CYAN}cyan, {Fore.WHITE}white, {Fore.BLACK}black\n{Fore.LIGHTBLACK_EX}lightblack_ex, {Fore.LIGHTBLUE_EX}lightblue_ex, {Fore.LIGHTCYAN_EX}lightcyan_ex, {Fore.LIGHTGREEN_EX}lightgreen_ex\n{Fore.LIGHTMAGENTA_EX}lightmagenta_ex, {Fore.LIGHTRED_EX}lightred_ex, {Fore.LIGHTWHITE_EX}lightwhite_ex, {Fore.LIGHTYELLOW_EX}lightyellow_ex{reset()}\nYou cannot see some colors as your terminal's background color is set that way.")
            elif listarg[2].startswith("clr") and listarg[2].endswith("background"):
                print(f"Allowed definitions:\n{Back.RED}red, {Back.GREEN}green, {Back.YELLOW}yellow, {Back.BLUE}blue, {Back.MAGENTA}magenta, {Back.CYAN}cyan, {Back.WHITE}white, {Back.BLACK}black\n{Back.LIGHTBLACK_EX}lightblack_ex, {Back.LIGHTBLUE_EX}lightblue_ex, {Back.LIGHTCYAN_EX}lightcyan_ex, {Back.LIGHTGREEN_EX}lightgreen_ex\n{Back.LIGHTMAGENTA_EX}lightmagenta_ex, {Back.LIGHTRED_EX}lightred_ex, {Back.LIGHTWHITE_EX}lightwhite_ex, {Back.LIGHTYELLOW_EX}lightyellow_ex{reset()}\nYou cannot see some colors as your terminal's background color is set that way.\n\nThe green color stretching from lightyellow_ex seems to be a bug that I can't fix.\nIf you find a fix, please make a PR.")
            elif listarg[2].startswith("clr") and listarg[2].endswith("style"):
                print(f"Allowed definitions: {Style.BRIGHT}BRIGHT, {Style.NORMAL}NORMAL, {Style.DIM}DIM, {Style.RESET_ALL}RESET_ALL")
            elif listarg[2] in ["default.include_filename","default.in_cwd","first_run","easter_errors"]:
                print(f"Allowed definitions: {Fore.GREEN}True, {Fore.RED}False")
            elif listarg[2] == "default.context":
                print(f"Allowed definitions: Any integer above 0")
    except IndexError:
        if listarg[1] == "set":
            print(f"{Fore.RED}FlagError: Expected value to set to `{listarg[2]}` but received None")
            exit(1)
        else:
            print(f"{Fore.RED}FlagError: Expected `list`, `read`, `write`, `update` or `reset` after `--config` but received {listarg[1]}")
            exit(1)
