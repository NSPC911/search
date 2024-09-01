import os
import sys
from custom_functions import *
from config import *
from colorama import Fore, Style, Back, init
import re

# Initialize colorama
init(strip=False, convert=False, autoreset=True)

def found_smth():
    global found
    found = True

def search_dir(directory, term):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            clear_line()
            relative_file_path = os.path.relpath(file_path, start=os.getcwd())
            print(f"\r{relative_file_path}", end="")
            if not is_binary(file_path):
                search_in_file(file_path, term)
            elif formatted_args[2] and term in str(relative_file_path):
                # Does this if not binary
                # Yes, there is a seperate code in 
                # search_in_file() but eh
                clear_line("-", "\n")
                print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
                found_smth()

def search_in_cwd(term):
    for item in os.listdir(os.getcwd()):
        clear_line()
        print(f"\r{item}", end="")
        if os.path.isfile(item) and not is_binary(item):
            file_path = os.path.join(os.getcwd(), item)
            search_in_file(file_path, term)
        elif is_binary(item) and formatted_args[2] and term in str(item):
            clear_line("-", "\n")
            print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{item}")
            samefile = True
            found_smth()

def search_in_file(file_path, term):
    if file_path.split(os.path.sep)[-1] != formatted_args[4] and formatted_args[4] != "*":
        # If file name doesn't match
        return
    # More vars!!
    samefile = False
    last_printed_line = -1
    printed_line_numbers = []
    if formatted_args[2] and term in str(file_path):
        # If file name has term
        clear_line("-", "\n")
        print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
        samefile = True
        found_smth()
    
    with open(file_path, 'r', errors='ignore') as f:
        lines = f.readlines()
    
    for line_number, line in enumerate(lines, start=1):
        if term in line:
            if not samefile:
                # Seperates files
                # Probably should make one for hunks
                # because line numbers can jump
                clear_line("-", "\n")
                print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
                samefile = True
                found_smth()
            start_line = max(0, line_number - 1 - formatted_args[3])
            end_line = min(len(lines), line_number + formatted_args[3])
            for i in range(start_line, end_line):
                if i > last_printed_line:
                    if line_number - 1 == i:
                        # When line has term
                        line_marker = ">"
                        clrs = [config("read","clr.has_term.line_number",is_theme=True), config("read","clr.has_term.line",is_theme=True)]
                    else:
                        # When line doesn't have the term
                        line_marker = " "
                        clrs = [config("read","clr.no_term.line_number",is_theme=True), config("read","clr.no_term.line",is_theme=True)]
                    if (term in lines[i] and i+1 < line_number) or i+1 in printed_line_numbers:
                        pass
                    elif line_number < i+1 and term in lines[i]:
                        # So it doesn't reprint the next line when it finds it
                        break
                    else:
                        print(f"{clrs[0]}{line_marker} {i+1}{Fore.WHITE}\t: {clrs[1]}{lines[i][:-1]}{reset()}")
                        printed_line_numbers.append(i+1)

def main():
    try:
        arg = " ".join(sys.argv[1:]).strip()
        print()
        # Unicode thing (yes it supports unicode)
        unicode_regex = r'\\u[0-9a-fA-F]{4}'
        notunicode_regex = r'\\u(?![0-9a-fA-F]{4})'
        if re.search(notunicode_regex, arg):
            print(f"{Fore.RED}ValueError: Invalid Unicode Escape sequence found. Please fix it before trying again.")
            exit(1)
        arg = re.sub(unicode_regex, replace_unicode, arg)

        # More vars, I love vars
        listarg = [""]
        index = 0
        is_flag = False
        was_flag = False

        # Separates the arguments
        # Could have used .split() but it doesn't work with spaces in between quotes
        # And I am extra bored :)
        for i in range (len(arg)):
            if is_flag and arg[i] == " ":
                is_flag = False
                if listarg[index] != "":
                    index += 1
                    listarg.append("")
                was_flag = True
            elif arg[i] == "-" and not is_flag:
                is_flag = True
                index += 1
                listarg.append(arg[i])
            elif arg[i] == '`':
                index += 1
                listarg.append("")
            elif arg[i+1:i+3] == "--" and arg[i] == " ":
                pass
            elif was_flag and arg[i] == " ": 
                was_flag = False
                index += 1
                listarg.append("")
            else:
                listarg[index] += arg[i]
        listarg = list(filter(None, listarg))

        # Makes the arguments more readable
        global formatted_args
        formatted_args = ["", config("read","default.in_cwd"), config("read", "default.include_filename"), config("read","default.context"), "*"]
        was_flag = False
        for i in range(len(listarg)):
            if listarg[i] == "--config":
                configure(listarg)
                exit(0)
            elif listarg[i] == "--in-cwd":
                formatted_args[1] = True
            elif listarg[i] == "--include-filename":
                formatted_args[2] = True
            elif listarg[i] == "--help":
                pass
            elif listarg[i] == "--context":
                try:
                    if int(listarg[i+1]) < 0:
                        raise OverflowError # Honestly unsure why I chose overflow error
                    else:
                        formatted_args[3] = int(listarg[i+1])
                except IndexError:
                    print(f"{Fore.RED}FlagError: Expected more after `--context` but received None")
                    exit(1)
                except ValueError:
                    print(f"{Fore.RED}ValueError: `{listarg[i+1]}` was not an integer")
                    exit(1)
                except OverflowError:
                    print(f"{Fore.RED}RangeError: `{listarg[i+1]}` is smaller than 0")
                    exit(1)
                was_flag = True
            elif listarg[i] == "--file-name":
                try:
                    formatted_args[4] = listarg[i+1]
                except IndexError:
                    print(f"{Fore.RED}FlagError: Expected more after `--file-name` but received None")
                    exit(1)
                was_flag = True
            elif listarg[i][:2] == "--":
                print(f"{Fore.YELLOW}Skipping unknown flag {Fore.BLUE}{listarg[i]}")
            elif was_flag:
                was_flag = False
            else:
                formatted_args[0] += listarg[i].strip()
        
        # Help thing
        try:
            if listarg[0] == "ECHO is on." or "--help" in arg:
                print(f"{Fore.WHITE}Usage: search <term> [--in-cwd] [--include-filename] [--context <int>] [--file-name <file>] [--config <modifier> <key> <value>]")
                print(f"{Fore.GREEN}Tool to search for a given term in a directory/file and return its line number.")
                print(f"{Fore.YELLOW}Always searches in current directory recursively unless specified{Fore.RESET}.")
                print(f"{Fore.BLUE}<term>\t\t\t:{Fore.WHITE} Term you want to search for.{Fore.YELLOW} (required)")
                print(f"{Fore.RED}--in-cwd\t\t:{Fore.WHITE} Search without entering into sub-directories.")
                print(f"{Fore.RED}--include-filename\t:{Fore.WHITE} Search includes file names.")
                print(f"{Fore.RED}--context\t\t:{Fore.WHITE} Shows more lines based on your integer.")
                print(f"{Fore.RED}--file-name\t\t:{Fore.WHITE} Searches only in the specified file name.")
                print(f"{Fore.RED}--config\t\t:{Fore.WHITE} Set or read a config value.")
                print(f"    {Fore.YELLOW}set <key> <value>\t:{Fore.WHITE} Set a value to a key.")
                print(f"    {Fore.YELLOW}read <key>\t\t:{Fore.WHITE} Read a value from a key along with a list of allowed definitions.")
                print(f"    {Fore.YELLOW}list\t\t:{Fore.WHITE} List all the keys and values.")
                print(f"    {Fore.YELLOW}update\t\t:{Fore.WHITE} Merges remote config with local config.")
                print(f"    {Fore.YELLOW}reset\t\t:{Fore.WHITE} Reset the config file to default.")
                exit(0)
        except IndexError:
            print("Run 'search --help' for more info!")
            exit(1)
        
        # Prints another message if not found
        global found
        found = False
        
        # Why do you enable so much random flags :sob:
        if formatted_args[1] and formatted_args[2] and formatted_args[4] != "*" and config("read","easter_errors"):
            print(f"{Fore.RED}EasterError: {Fore.YELLOW}Huh? Your choice of flags is weird.\n")
        
        if formatted_args[1]:
            # Searches in Current Working Directory
            print(f"{Fore.WHITE}Searching for {Fore.BLUE}{formatted_args[0]} {Fore.WHITE}in {Fore.YELLOW}{os.getcwd()}")
            search_in_cwd(formatted_args[0])
        else:
            # Searches in the directory recursively
            print(f"{Fore.WHITE}Searching for {Fore.BLUE}{formatted_args[0]}")
            search_dir(os.getcwd(), formatted_args[0])
        
        if not found:
            clear_line()
            print(f"\n{Fore.YELLOW}Couldn't find {Fore.BLUE}{formatted_args[0]}")
        else:
            clear_line("-")
            print()
    except KeyboardInterrupt:
        # Hate the error, pareses it nicely
        pass

if __name__ == "__main__":
    main()
