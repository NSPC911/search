import os, hashlib, argparse
from zipfile import ZipFile, ZIP_DEFLATED
from colorama import *
init(strip=False, convert=False, autoreset=True)
parser = argparse.ArgumentParser(description=None)
parser.add_argument("--workflow", action="store_true", default=False, help="Enable workflow mode")
args = parser.parse_args()

root_dir = os.path.dirname(os.path.abspath(__file__))
archives_dir = os.path.join(root_dir, 'archives')

os.makedirs(archives_dir, exist_ok=True)

all_files = [
    f for f in os.listdir(root_dir)
    if os.path.isfile(os.path.join(root_dir, f))
]

archive_specs = {
    'bat.zip': [f for f in all_files if f not in ['.gitignore', 'search.sh', 'archive_creator.py', 'search.json', 'notes.json']],
    'bash.zip': [f for f in all_files if f not in ['.gitignore', 'search.bat', 'archive_creator.py', 'search.json', 'notes.json']]
}

for archive_name, files_to_include in archive_specs.items():
    archive_path = os.path.join(archives_dir, archive_name)
    with ZipFile(archive_path, 'w', ZIP_DEFLATED) as archive:
        for file in files_to_include:
            archive.write(os.path.join(root_dir, file), file)

hasher = hashlib.sha256()
with open(f'{archives_dir}/bat.zip', "rb") as f:
    for byte_block in iter(lambda: f.read(4096), b""):
        hasher.update(byte_block)
    bathash = hasher.hexdigest()
hasher = hashlib.sha256()
with open(f'{archives_dir}/bash.zip', "rb") as f:
    for byte_block in iter(lambda: f.read(4096), b""):
        hasher.update(byte_block)
    bashhash = hasher.hexdigest()
print(f"{Fore.YELLOW}SHA256{Fore.WHITE} for {Fore.LIGHTBLUE_EX}bat.zip{Fore.WHITE}  is {Fore.RED}{bathash}")
print(f"{Fore.YELLOW}SHA256{Fore.WHITE} for {Fore.LIGHTBLUE_EX}bash.zip{Fore.WHITE} is {Fore.RED}{bashhash}")

if args.workflow:
    with ZipFile(f'{archives_dir}/bat.zip', 'r', ZIP_DEFLATED) as archive:
        archive.extractall(f'{archives_dir}/bat')
    os.remove(f'{archives_dir}/bat.zip')
    with ZipFile(f'{archives_dir}/bash.zip', 'r', ZIP_DEFLATED) as archive:
        archive.extractall(f'{archives_dir}/bash')
    os.remove(f'{archives_dir}/bash.zip')