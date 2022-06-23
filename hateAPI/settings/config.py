import os
from pathlib import Path 
from zipfile import ZipFile
import logging


logger = logging.getLogger(__name__)

API_DIR = Path(__file__).parent.parent

default_model = "tensorflow"
# default_model = "pytorch"


##################Models path #################
tensorflow_model_path  = API_DIR.joinpath("core/tensorflow/hs_bert")
pytorch_model_path =  API_DIR.joinpath("core/pytorch/bert_torch_dict.pth") 
################ URL PATH TO API ##########################
URL_API = 'http://localhost:8080'

################ PATH FOR STORED DATA ######################
TEMP_DIR = Path(__file__).parent.parent / "temp/"
# saved_model_path = Path(__file__).parent.parent / "core/imdb_bert"

# saved_model_path = API_DIR.joinpath("core/imdb_bert")
bert_tensorflow_zip_file = API_DIR.joinpath("core/tensorflow/hs_bert.zip")
bert_pytorch_zip_file = API_DIR.joinpath("core/pytorch/bert_torch.zip")

video_dir =TEMP_DIR.joinpath ("video/")
audio_dir = TEMP_DIR.joinpath("audio/")
txt_dir =TEMP_DIR.joinpath("text/")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

if not os.path.exists(video_dir):
    os.makedirs(video_dir)

if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

if default_model =="tensorflow" and not os.path.exists(tensorflow_model_path):
    with ZipFile(bert_tensorflow_zip_file, 'r') as zipObj:
        zipObj.extractall(tensorflow_model_path.parent)

# if default_model =="pytorch" and not os.path.exists(tensorflow_model_path):
#     with ZipFile(bert_pytorch_zip_file, 'r') as zipObj:
#         zipObj.extractall(tensorflow_model_path.parent)

################### END #####################
