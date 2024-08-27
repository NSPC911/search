import os
import sys
#import time
from colorama import Fore, Style, init
import re
from custom_functions import *

# Initialize colorama
init(autoreset=True)

def found_smth():
    global found
    found = True

def search_dir(directory, term):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            clear_line()
            relative_file_path = os.path.relpath(file_path, start=os.getcwd())
            print(f"\r{relative_file_path}", end="")
            if not is_binary(file_path):
                search_in_file(file_path, term)
            elif formatted_args[2] and term in str(relative_file_path):
                clear_line("-", "\n")
                print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
                samefile = True
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
        return
    samefile = False
    last_printed_line = -1
    printed_line_numbers = []
    if formatted_args[2] and term in str(file_path):
        clear_line("-", "\n")
        print(f"\r{Fore.WHITE}Found {Fore.YELLOW}{term} {Fore.WHITE}in {Fore.GREEN}{os.path.relpath(file_path, start=os.getcwd())}")
        samefile = True
        found_smth()
    with open(file_path, 'r', errors='ignore') as f:
        lines = f.readlines()
    for line_number, line in enumerate(lines, start=1):
        if term in line:
            if not samefile:
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
                        clrs = [Fore.CYAN, Fore.GREEN]
                    else:
                        # When line doesn't have the term
                        line_marker = " "
                        clrs = [Fore.BLUE, Fore.RED]
                    if (term in lines[i] and i+1 < line_number) or i+1 in printed_line_numbers:
                        pass
                    elif line_number < i+1 and term in lines[i]:
                        break
                    else:
                        print(f"{clrs[0]}{line_marker} {i+1}{Fore.WHITE}\t: {clrs[1]}{lines[i][:-1]}")
                        printed_line_numbers.append(i+1)

def main():
    try:
        arg = sys.stdin.read().strip()
        listarg = [""]
        index = 0
        wait_until = -1
        is_flag = False 
        unicode_regex = r'\\u[0-9a-fA-F]{4}'
        notunicode_regex = r'\\u(?![0-9a-fA-F]{4})'
        if re.search(notunicode_regex, arg):
            print(f"{Fore.RED}ValueError: Invalid Unicode Escape sequence found. Please fix it before trying again.")
            exit(1)
        arg = re.sub(unicode_regex, replace_unicode, arg)
        for i in range (len(arg)):
            if is_flag and arg[i] == " ":
                is_flag = False
                if listarg[index] != "":
                    index += 1
                    listarg.append("")
            elif arg[i] == "-" and not is_flag:
                is_flag = True
                index += 1
                listarg.append(arg[i])
            elif arg[i] == '`':
                index += 1
                listarg.append("")
            elif arg[i+1:i+3] == "--" and arg[i] == " ":
                pass
            else:
                listarg[index] += arg[i]
        listarg = list(filter(None, listarg))
        global formatted_args
        formatted_args = ["<term>", False, False, 0, "*"]
        for i in range(len(listarg)):
            is_flag = False
            if i == 0:
                formatted_args[0] = listarg[0].strip()
            if listarg[i] == "--in-cwd":
                is_flag = True
                formatted_args[1] = True
            if listarg[i] == "--include-filename":
                is_flag = True
                formatted_args[2] = True
            if listarg[i] == "--help":
                is_flag = True
            if listarg[i] == "--context":
                is_flag = True
                try:
                    if int(listarg[i+1]) < 0:
                        raise OverflowError
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
            if listarg[i] == "--file-name":
                is_flag = True
                try:
                    formatted_args[4] = listarg[i+1]
                except IndexError:
                    print(f"{Fore.RED}FlagError: Expected more after `--file-name` but received None")
                    exit(1)
            if not is_flag and listarg[i][:2] == "--":
                print(f"{Fore.YELLOW}Skipping unknown flag {Fore.BLUE}{listarg[i]}")
        
        if listarg[0] == "ECHO is on." or "--help" in arg:
            print(f"\n{Fore.WHITE}Usage: search <term> [--in-file <file>] [--in-cwd] [--include-filename] [--context <int>]")
            print(f"{Fore.GREEN}Tool to search for a given term in a directory/file and return its line number.")
            print(f"{Fore.YELLOW}Always searches in current directory recursively unless specified{Fore.RESET}.")
            print(f"{Fore.BLUE}<term>\t\t\t:{Fore.WHITE} Term you want to search for.{Fore.YELLOW} (required)")
            print(f"{Fore.RED}--in-cwd\t\t:{Fore.WHITE} Search without entering into sub-directories.")
            print(f"{Fore.RED}--include-filename\t:{Fore.WHITE} Search includes file names.")
            print(f"{Fore.RED}--context\t\t:{Fore.WHITE} Shows more lines based on your integer.")
            print(f"{Fore.RED}--file-name\t\t:{Fore.WHITE} Searches only in the specified file name.")
            exit(0)
        
        global found
        found = False
        print()
        
        if formatted_args[1] == True:
            print(f"{Fore.WHITE}Searching for {Fore.BLUE}{listarg[0]} {Fore.WHITE}in {Fore.YELLOW}{os.getcwd()}")
        else:
            print(f"{Fore.WHITE}Searching for {Fore.BLUE}{listarg[0]}")
        
        if formatted_args[1] == True:
            search_in_cwd(formatted_args[0])
        else:
            search_dir(os.getcwd(), formatted_args[0])
        if not found:
            clear_line()
            print(f"\n{Fore.YELLOW}Couldn't find {Fore.BLUE}{formatted_args[0]}")
        else:
            clear_line("-")
            print()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
