import zipfile
import os

# Directories and file paths
root_dir = os.path.dirname(os.path.abspath(__file__))
archives_dir = os.path.join(root_dir, 'archives')

# Ensure the archives directory exists
os.makedirs(archives_dir, exist_ok=True)

# List of all files in the root directory
all_files = [
    f for f in os.listdir(root_dir)
    if os.path.isfile(os.path.join(root_dir, f))
]

# Archive file specifications
archive_specs = {
    'bat.zip': [f for f in all_files if f not in ['.gitignore', 'search.sh']],
    'bash.zip': [f for f in all_files if f not in ['.gitignore', 'search.bat']],
    'scoop.zip': [f for f in all_files if f not in ['.gitignore', 'search.bat', 'search.sh']]
}

# Create archives based on the specifications
for archive_name, files_to_include in archive_specs.items():
    archive_path = os.path.join(archives_dir, archive_name)
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in files_to_include:
            archive.write(os.path.join(root_dir, file), file)

print("Archives created successfully!")
