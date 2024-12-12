import zipfile, os, hashlib
from colorama import *
init(strip=False, convert=False, autoreset=True)


root_dir = os.path.dirname(os.path.abspath(__file__))
archives_dir = os.path.join(root_dir, 'archives')

os.makedirs(archives_dir, exist_ok=True)

all_files = [
    f for f in os.listdir(root_dir)
    if os.path.isfile(os.path.join(root_dir, f))
]

archive_specs = {
    'bat.zip': [f for f in all_files if f not in ['.gitignore', 'search.sh', 'archive_creator.py', 'search.json']],
    'bash.zip': [f for f in all_files if f not in ['.gitignore', 'search.bat', 'archive_creator.py', 'search.json']]
}

for archive_name, files_to_include in archive_specs.items():
    archive_path = os.path.join(archives_dir, archive_name)
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
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
print(f"{Fore.YELLOW}SHA256{Fore.WHITE} for {Fore.BLUE}bat.zip{Fore.WHITE}  is {Fore.RED}{bathash}")
print(f"{Fore.YELLOW}SHA256{Fore.WHITE} for {Fore.BLUE}bash.zip{Fore.WHITE} is {Fore.RED}{bashhash}")
