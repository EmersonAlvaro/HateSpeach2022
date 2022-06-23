#!/bin/bash

echo "setup pythone Virtualenv environment..." 

sudo apt-get update

# # Install Virtualenv
python3 -m pip install --upgrade pip

# # Delete old virtualenv
rm -rf venv

# python3 -m venv --system-site-packages ./venv

source venv/bin/activate

# #Install all requirements
python3 -m pip install -r requirements.txt -q

# #Tesseratc installl 

pip install pytesseract
pip install tox

tox
