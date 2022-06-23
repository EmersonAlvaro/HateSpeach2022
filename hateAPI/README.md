# hateSpeach RestFull API


# Description
In this project we intend to create a RESTFUll API for dectetion of hateSpeach.
This project is part of semester project in EURECOM

# Overview
The HateSpeach is based on client-server arquitecture power by Machine Learning Model
![Alt text](overview.jpeg?raw=true "Title")

# # How to Run the project

# 1 - Install python create virtaulenv/conda and install packages: 
    $  make setup_env 
    $  make setup_conda 
    
# 2 - Start Server
    $ make run_server

# Module Structure

```bash
├── hateAPI
│   ├── core
│   │   └── imdb_bert
│   │       ├── assets
│   │       └── variables
│   ├── settings
│   ├── temp
│   │   ├── audio
│   │   ├── text
│   │   └── video
│   └── utils
```