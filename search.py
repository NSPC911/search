import os, sys
from custom_functions import *
from config import *
from colorama import Fore, init # type: ignore
import requests
import argparse

# Initialize colorama
init(strip=False, convert=False, autoreset=True)
remote_url = "https://raw.githubusercontent.com/NSPC911/search/main/"

def found_smth():
    global found
    found = True

def search_dir(directory, term, case_sensitive):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            clear_line()
            relative_file_path = os.path.relpath(file_path, start=os.getcwd())
            print(f"\r{relative_file_path}", end="")
            if not is_binary(file_path):
                search_in_file(file_path, term, case_sensitive)
            elif args.include_filename and term in str(relative_file_path):
                clear_line("-", "\n")
                print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
                found_smth()

def search_in_cwd(term, case_sensitive):
    for item in os.listdir(os.getcwd()):
        clear_line()
        print(f"\r{item}", end="")
        if os.path.isfile(item) and not is_binary(item):
            file_path = os.path.join(os.getcwd(), item)
            search_in_file(file_path, term, case_sensitive)
        elif args.include_filename and term in str(item):
            clear_line("-", "\n")
            print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{item}")
            found_smth()

def search_in_file(file_path, term, case_sensitive):
    if file_path.split(os.path.sep)[-1] != args.file_name and args.file_name != "*":
        return

    if term in str(file_path) and args.include_filename:
        clear_line("-", "\n")
        print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
        found_smth()
    
    samefile = False
    last_printed_line = -1
    printed_line_numbers = []

    with open(file_path, 'r', errors='ignore') as f:
        lines = f.readlines()

    for line_number, line in enumerate(lines, start=1):
        if (term in line if case_sensitive else term.lower() in line.lower()):
            if not samefile:
                clear_line("-", "\n")
                print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
                samefile = True
                found_smth()

            start_line = max(0, line_number - 1 - args.context)
            end_line = min(len(lines), line_number + args.context)
            for i in range(start_line, end_line):
                if i > last_printed_line:
                    if line_number - 1 == i:
                        line_marker = ">"
                        clrs = [config("read","clr.has_term.line_number",is_theme=True), config("read","clr.has_term.line",is_theme=True)]
                    else:
                        line_marker = " "
                        clrs = [config("read","clr.no_term.line_number",is_theme=True), config("read","clr.no_term.line",is_theme=True)]

                    if term in lines[i] and i+1 < line_number or i+1 in printed_line_numbers:
                        pass
                    elif line_number < i+1 and term in lines[i]:
                        break
                    else:
                        print(f"{clrs[0]}{line_marker} {i+1}{Fore.WHITE}\t: {clrs[1]}{lines[i][:-1]}{reset()}")
                        printed_line_numbers.append(i+1)

def main():
    print()
    parser = argparse.ArgumentParser(description=f"Find.exe but {Fore.CYAN}better{Fore.RESET}")
    parser.add_argument("term", nargs="?", help="Term to search for")
    if config("read","default.in_cwd"):
        parser.add_argument("--recursive", action="store_false", default=True, help=f"Search {Fore.YELLOW}in sub-directories{Fore.RESET}")
    else:
        parser.add_argument("--in-cwd", action="store_true", default=False, help=f"Search {Fore.YELLOW}only{Fore.RESET} in the current directory")
    if config("read","default.include_filename"):
        parser.add_argument("--exclude-filename", action="store_false", default=True, help=f"{Fore.YELLOW}Exclude file names{Fore.RESET} from the search")
    else:
        parser.add_argument("--include-filename", action="store_true", default=False, help=f"{Fore.YELLOW}Include file names{Fore.RESET} in the search")
    parser.add_argument("--context", type=int, default=config("read","default.context"), help=f"Number of {Fore.YELLOW}context lines{Fore.RESET} to show")
    parser.add_argument("--file-name", default="*", help=f"Search only in the {Fore.YELLOW}specified file name{Fore.RESET}")
    if config("read","default.case_sensitive"):
        parser.add_argument("--case-insensitive", action="store_false", default=True, help=f"Disable case-sensitive searching")
    else:
        parser.add_argument("--case-sensitive", action="store_true", default=False, help=f"Enable case-sensitive searching")
    parser.add_argument("--config", nargs=argparse.REMAINDER, metavar=('modifier', 'key', 'value'), help="Configure settings: modifier key value")
    parser.add_argument("--update", action="store_true", help="Update files from remote")

    global args
    args = parser.parse_args()
    try:
        args.in_cwd = not args.recursive
    except AttributeError:
        pass
    try:
        args.case_sensitive = not args.case_insensitive
    except AttributeError:
        pass
    try:
        args.include_filename = not args.exclude_filename
    except AttributeError:
        pass
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    if args.config:
        configure(args.config)
        return

    if args.update:
        # Screw you, you are updating everything
        response = requests.get(remote_url + "search.config.json")
        if response.status_code == 200:
            remote_config = response.json()
            current_config = load_json(config_path)
            new_config = {**remote_config, **current_config}
            dump_json(config_path,new_config)
            print(f"{Fore.GREEN}Updated search.config.json from remote!")
        else:
            raise ReferenceError("search.config.json")
        files_to_get = ["config.py", "custom_functions.py", "search.py"]
        for file in files_to_get:
            response = requests.get(remote_url + file)
            if response.status_code == 200:
                with open(file, "w") as f:
                    f.write(response.text)
                print(f"{Fore.GREEN}Updated {file} from remote!")
            else:
                raise ReferenceError(file)
        print(f"{Fore.GREEN}Updated all scripts from remote!")
        return

    global found
    found = False

    if args.in_cwd:
        print(f"{Fore.WHITE}Searching for {Fore.BLUE}{args.term} {Fore.WHITE}in {Fore.YELLOW}{os.getcwd()}")
        search_in_cwd(args.term, args.case_sensitive)
    else:
        print(f"{Fore.WHITE}Searching for {Fore.BLUE}{args.term}")
        search_dir(os.getcwd(), args.term, args.case_sensitive)

    if not found:
        clear_line()
        print(f"\n{Fore.YELLOW}Couldn't find {Fore.BLUE}{args.term}")
    else:
        clear_line("-")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except ReferenceError: # I just use random errors that suit lol
        print(f"{Fore.RED}RequestError: Couldn't fetch data from remote for {Fore.YELLOW}{args.file_name}")
        print(f"{Fore.RED}Please check your internet connection and try again.")
        exit(1)
