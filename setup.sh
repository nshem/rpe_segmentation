#!/usr/bin/env bash

# activate the virtual environment
source venv/bin/activate

# if the virtual environment is not activated, exit
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate the virtual environment"
    exit 1
fi

# make sure python version is higher than 3.10 and lower than 3.11
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
IFS='.' read -r major minor patch <<< "$PYTHON_VERSION"
if [[ "$major" -eq 3 && "$minor" -lt 12 ]] && [[ "$major" -eq 3 && "$minor" -ge 10 ]]; then
    echo "Python version $PYTHON_VERSION is compatible."
else
    echo "Python version $PYTHON_VERSION is not compatible. Required: >=3.10 and <3.12"
    exit 1
fi

pip3 install -r requirements.txt

# Download the weights
if [ ! -d $(pwd)/weights ]; then
    echo "Downloading the weights"
    mkdir -p $(pwd)/weights
    wget -q https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P $(pwd)/weights
fi