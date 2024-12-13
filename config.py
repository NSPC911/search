from custom_functions import *
import os
from colorama import Fore, Style, init, Back
from shutil import copyfile
init(strip=False, convert=False, autoreset=True)

sep = os.path.sep
config_remote_url = "https://raw.githubusercontent.com/NSPC911/search/main/config.json"
config_path = f"{os.path.dirname(os.path.realpath(__file__))}{sep}config.json"
# Just exists I guess...
if f"scoop{sep}apps" in config_path:
    if not os.path.exists(f"{os.path.expanduser("~")}{sep}scoop{sep}persist{sep}config.json"):
        copyfile(config_path,f"{os.path.expanduser('~')}{sep}scoop{sep}persist{sep}search{sep}config.json")
    config_path = f"{os.path.expanduser('~')}{sep}scoop{sep}persist{sep}search{sep}config.json"

def config(readorset:str, key:str, changeto="", is_theme:bool=False):
    cnfg = load_json(config_path)
    if readorset == "read":
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
                print(f"{Fore.RED}KeyError: `{key}` not found in config.json")
                exit(1)
    elif readorset == "set":
        try:
            cnfg[key] # Check whether exists
            cnfg[key] = changeto
            dump_json(config_path,cnfg)
            print(f"{Fore.GREEN}Set `{Fore.CYAN}{key}{Fore.GREEN}` to {Fore.MAGENTA}{changeto}")
        except KeyError:
            print(f"{Fore.RED}KeyError: `{key}` not found in config.json")
            exit(1)


def reset():
    return f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}" 

if config("read","default.context") < 0:
    print(f"{Fore.RED}RangeError: `default.context` in config.json is less than 0.")
    exit(0)

def configure(listarg):
    try:
        listarg[0]
    except IndexError:
        print(f"Supported arguments for {Fore.LIGHTBLUE_EX}--config{Fore.WHITE}")
        print(f"  {Fore.LIGHTBLUE_EX}set{Fore.WHITE}\t[{Fore.LIGHTBLUE_EX}key{Fore.WHITE}]\t[{Fore.LIGHTBLUE_EX}value{Fore.WHITE}]")
        print("\tSet a key to the value given")
        print(f"  {Fore.CYAN}read{Fore.WHITE}\t[{Fore.CYAN}key{Fore.WHITE}]")
        print("\tOutput the current value for the key")
        print(f"  {Fore.YELLOW}where{Fore.WHITE}")
        print("\tLocate where the config is found at")
        print(f"  {Fore.GREEN}list{Fore.WHITE}")
        print("\tList the keys and their corresponsing values")
        print(f"  {Fore.LIGHTBLACK_EX}reset{Fore.WHITE}")
        print("\tReset the config")
        exit(1)
    if listarg[0] == "reset":
        import requests
        try:
            response = requests.get(config_remote_url)
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}ConnectionError: Max retries exceeded, likely due to no connection.")
            print(f"{Fore.YELLOW}\tTurn off Flight Mode and connect to a WiFi, or restart your device.")
            exit(1)
        if response.status_code == 200:
            dump_json(config_path,response.json())
            print(f"{Fore.GREEN}Reset config.json to default from remote")
        else:
            print(f"{Fore.RED}RequestError: Couldn't fetch data from remote for {Fore.YELLOW}config.json")
            print(f"{Fore.RED}Please check your internet connection and try again.")
            exit(1)
        return
    elif listarg[0] == "list":
        print(f"{' ' * 16}Key{' ' * 16} |     Value")
        print(f'{"-" * 52}')
        bools = config("read", "config.env.type.boolean")
        for key in load_json(config_path):
            if "env" in key:
                continue # Ya don't need to see environment variables
            if "foreground" in key:
                print(f"{Fore.CYAN}{key}{Fore.WHITE}{" " * (35 - len(key))} | {Fore.__dict__[config('read',key).upper()]}{config('read',key)}")
            elif "background" in key:
                print(f"{Fore.CYAN}{key}{Fore.WHITE}{" " * (35 - len(key))} | {Back.__dict__[config('read',key).upper()]}{config('read',key)}")
            elif "style" in key:
                print(f"{Fore.CYAN}{key}{Fore.WHITE}{" " * (35 - len(key))} | {Style.__dict__[config('read',key).upper()]}{config('read',key)}")
            elif key in bools:
                readed = config('read',key)
                print(f"{Fore.CYAN}{key}{Fore.WHITE}{" " * (35 - len(key))} | {Fore.LIGHTGREEN_EX if readed == True else Fore.LIGHTRED_EX}{readed}")
            else:
                print(f"{Fore.CYAN}{key}{Fore.WHITE}{" " * (35 - len(key))} | {Fore.MAGENTA}{config('read',key)}")
        exit(0)
    elif listarg[0] == "where":
        print(f"{Fore.GREEN}config.json is located at {Fore.CYAN}{config_path}")
        exit(0)
    try:
        last = listarg.pop().split()
        listarg.extend(last)
        if listarg[0] == "set":
            if listarg[1] in config("read", "config.env.type.boolean"):
                if listarg[2].lower() in ["true","false"]:
                    config("set",listarg[1],listarg[2].lower()=="true")
                else:
                    print(f"Allowed definitions: {Fore.GREEN}True{reset()}, {Fore.RED}False")
                    exit(1)
            elif listarg[1] == "default.context" and listarg[2].isnumeric():
                config("set",listarg[1],int(listarg[2]))
            elif listarg[1] == "default.context":
                print(f"Allowed definitions: Any integer above 0")
                exit(1)
            elif listarg[1].startswith("clr") and (listarg[1].endswith("foreground") or listarg[1].endswith("background")) and listarg[2].lower() in ["red","green","yellow","blue","magenta","cyan","white","black","lightblack_ex","lightblue_ex","lightcyan_ex","lightgreen_ex","lightmagenta_ex","lightred_ex","lightwhite_ex","lightyellow_ex","reset"]:
                config("set",listarg[1],listarg[2].lower())
            elif listarg[1].startswith("clr") and listarg[1].endswith("foreground"):
                print(f"Allowed definitions:\n{Fore.RED}red, {Fore.GREEN}green, {Fore.YELLOW}yellow, {Fore.LIGHTBLUE_EX}blue, {Fore.MAGENTA}magenta, {Fore.CYAN}cyan, {Fore.WHITE}white, {Fore.BLACK}black\n{Fore.LIGHTBLACK_EX}lightblack_ex, {Fore.LIGHTBLUE_EX}lightblue_ex, {Fore.LIGHTCYAN_EX}lightcyan_ex, {Fore.LIGHTGREEN_EX}lightgreen_ex\n{Fore.LIGHTMAGENTA_EX}lightmagenta_ex, {Fore.LIGHTRED_EX}lightred_ex, {Fore.LIGHTWHITE_EX}lightwhite_ex, {Fore.LIGHTYELLOW_EX}lightyellow_ex, {Fore.RESET}reset")
                print("You may see some colors as your terminal's background color is set that way.")
                exit(1)
            elif listarg[1].startswith("clr") and listarg[1].endswith("background"):
                print(f"Allowed definitions:\n{Back.RED}red{reset()}, {Back.GREEN}green{reset()}, {Back.YELLOW}yellow{reset()}, {Back.BLUE}blue{reset()}, {Back.MAGENTA}magenta{reset()}, {Back.CYAN}cyan{reset()}, {Back.WHITE}white{reset()}, {Back.BLACK}black\n{Back.LIGHTBLACK_EX}lightblack_ex{reset()}, {Back.LIGHTBLUE_EX}lightblue_ex{reset()}, {Back.LIGHTCYAN_EX}lightcyan_ex{reset()}, {Back.LIGHTGREEN_EX}lightgreen_ex{reset()}\n{Back.LIGHTMAGENTA_EX}lightmagenta_ex{reset()}, {Back.LIGHTRED_EX}lightred_ex{reset()}, {Back.LIGHTWHITE_EX}lightwhite_ex{reset()}, {Back.LIGHTYELLOW_EX}lightyellow_ex{reset()}, {Back.RESET}reset")
                print("You may see some colors as your terminal's background color is set that way.")
                exit(1)
            elif listarg[1].startswith("clr") and listarg[1].endswith("style") and listarg[2].lower() in ["bright","normal","dim","reset_all"]:
                config("set",listarg[1],listarg[2].lower())
            elif listarg[1].startswith("clr") and listarg[1].endswith("style"):
                print(f"Allowed definitions: {Style.BRIGHT}BRIGHT{reset()}, {Style.NORMAL}NORMAL{reset()}, {Style.DIM}DIM{reset()}, {Style.RESET_ALL}RESET_ALL")
                exit(1)
            elif "env" in listarg[1]:
                print(f"{Fore.RED}ConfigError: Cannot change env variables in config.json")
                exit(1)
            elif listarg[1] == "default.ignore_dirs":
                print(f"{Fore.RED}ConfigError: Cannot change `{Fore.LIGHTBLUE_EX}default.ignore_dirs{Fore.RED}` yet in config.json")
                print("This feature is still in development.")
                exit(1)
            else:
                if listarg[2].isnumeric():
                    config("set",listarg[1],int(listarg[2]))
                else:
                    config("set",listarg[1],listarg[2].lower())
        elif listarg[0] == "read":
            print(f"`{Fore.CYAN}{listarg[1]}{Fore.WHITE}` is set as {Fore.MAGENTA}{config('read',listarg[1])}")
            if listarg[1].startswith("clr") and listarg[1].endswith("foreground"):
                print(f"Allowed definitions:\n{Fore.RED}red{reset()}, {Fore.GREEN}green{reset()}, {Fore.YELLOW}yellow{reset()}, {Fore.LIGHTBLUE_EX}blue{reset()}, {Fore.MAGENTA}magenta{reset()}, {Fore.CYAN}cyan{reset()}, {Fore.WHITE}white{reset()}, {Fore.BLACK}black\n{Fore.LIGHTBLACK_EX}lightblack_ex{reset()}, {Fore.LIGHTBLUE_EX}lightblue_ex{reset()}, {Fore.LIGHTCYAN_EX}lightcyan_ex{reset()}, {Fore.LIGHTGREEN_EX}lightgreen_ex\n{Fore.LIGHTMAGENTA_EX}lightmagenta_ex{reset()}, {Fore.LIGHTRED_EX}lightred_ex{reset()}, {Fore.LIGHTWHITE_EX}lightwhite_ex{reset()}, {Fore.LIGHTYELLOW_EX}lightyellow_ex{reset()}\nYou cannot see some colors as your terminal's background color is set that way.")
            elif listarg[1].startswith("clr") and listarg[1].endswith("background"):
                print(f"Allowed definitions:\n{Back.RED}red, {Back.GREEN}green, {Back.YELLOW}yellow, {Back.BLUE}blue, {Back.MAGENTA}magenta, {Back.CYAN}cyan, {Back.WHITE}white, {Back.BLACK}black\n{Back.LIGHTBLACK_EX}lightblack_ex, {Back.LIGHTBLUE_EX}lightblue_ex, {Back.LIGHTCYAN_EX}lightcyan_ex, {Back.LIGHTGREEN_EX}lightgreen_ex\n{Back.LIGHTMAGENTA_EX}lightmagenta_ex, {Back.LIGHTRED_EX}lightred_ex, {Back.LIGHTWHITE_EX}lightwhite_ex, {Back.LIGHTYELLOW_EX}lightyellow_ex{reset()}\nYou cannot see some colors as your terminal's background color is set that way.\n\nThe green color stretching from lightyellow_ex seems to be a bug that I can't fix.\nIf you find a fix, please make a PR.")
            elif listarg[1].startswith("clr") and listarg[1].endswith("style"):
                print(f"Allowed definitions: {Style.BRIGHT}BRIGHT, {Style.NORMAL}NORMAL, {Style.DIM}DIM, {Style.RESET_ALL}RESET_ALL")
            elif listarg[1] in ["default.include_filename","default.in_cwd","default.case_sensitive","updater.canary"]:
                print(f"Allowed definitions: {Fore.GREEN}True, {Fore.RED}False")
            elif listarg[1] == "default.context":
                print(f"Allowed definitions: Any integer above 0")
            exit(0)
        else:
            print(f"{Fore.RED}FlagError: Expected {Fore.YELLOW}`list`{Fore.RED}, {Fore.YELLOW}`read`{Fore.RED} or {Fore.YELLOW}`set`{Fore.RED} after {Fore.YELLOW}`--config`{Fore.RED} but received {Fore.YELLOW}{listarg[0]}{Fore.RED}")
            exit(1)
    except IndexError:
        if listarg[0] == "set":
            try:
                print(f"{Fore.RED}FlagError: Expected value to set to {Back.LIGHTBLACK_EX}`{listarg[1]}`{Back.RESET} but received None")
                exit(1)
            except IndexError:
                print(f"{Fore.RED}FlagError: Expected key but received None")
        elif listarg[0] == "read":
            print(f"{Fore.RED}FlagError: Expected key but received None")