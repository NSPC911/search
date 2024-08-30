#!/bin/bash

# Check if no arguments are passed
if [ "$#" -eq 0 ]; then
    echo "Run 'search --help' for more info!"
    exit 1
fi

# Execute the Python script with the provided arguments
python3 "$(dirname "$0")/search.py" "$@"