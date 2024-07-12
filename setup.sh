#!/usr/bin/env bash

pip3 install -q 'git+https://github.com/facebookresearch/segment-anything.git'
pip3 install -q dataclasses-json supervision torchvision torch opencv-python shapely
     
HERE=$(pwd)

# Download the weights
if [ ! -d ${HERE}/weights ]; then
    echo "Downloading the weights"
    mkdir -p ${HERE}/weights
    wget -q https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P ${HERE}/weights
fi


if [ ! -d ${HERE}/data ]; then
    # Download the data
    echo "Downloading the data"
    mkdir -p ${HERE}/data
    wget -q https://media.roboflow.com/notebooks/examples/dog.jpeg -P ${HERE}/data
fi

echo "HERE: ${HERE}"
