#!/bin/bash

echo "setup conda environment..." 
#conda deactivate
# conda create -y --name hsEnv
# conda install --force-reinstall -y -q --name hsEnv -c conda-forge --file requirements.txt
# conda install -c conda-forge pytesseract
# conda activate hsEnv


# curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
# bash Miniconda3-latest-Linux-x86_64.sh

# conda init 

# source ~/.bashrc

# conda -V

# conda create --name hateSpeachEnv


# conda deactivate
conda activate hateSpeachEnv

pip install --upgrade pip

python3 -m pip install -r requirements.txt

playwright install  
tox
playwright install-deps