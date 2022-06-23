import os, sys
import tensorflow as tf
import torch
import numpy as np
from time import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings.config import *
from core.bert_model_pytorch import *

import transformers
from transformers import BertTokenizer
import torch.nn as nn
from transformers import BertModel
import torch.nn.functional as F
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
tf.get_logger().setLevel(logging.ERROR)

def map_output(out):
    if out == 0:
        return "Hate Speach"
    elif out == 1:
        return "Offensive language"
    elif out == 2:
        return "No Hate Speach"
    else:
        return None

class Bert_Model_Tensorflow:
    
    def __init__(self):
        self.load_model()
        # self.reloaded_model.summary()

    def load_model(self):
        print(" Loading tensorflow model..........................")

        self.reloaded_model = tf.keras.models.load_model(tensorflow_model_path)
        
        print("Model read for prediction............ ")
   
    def predict(self, input):
        model_predition = self.reloaded_model.predict(input)     
        
        return map_output(np.argmax(model_predition.flatten(), axis=-1))


# Work in progress .......
class Bert_Model_Pytorch:
    
    def __init__(self):
        self.device = torch.device('cpu')
        self.reloaded_model = BertClassifier()
        self.reloaded_model.load_state_dict(torch.load(pytorch_model_path, map_location=self.device))
        self.reloaded_model.eval()
    
    def predict(self, input_text):
        
        input_ids, attention_masks = bert_encoding_text(input_text)
    
        with torch.no_grad():
            model_predition = self.reloaded_model(input_ids, attention_masks )
        
        a , model_predition = torch.max(model_predition,  dim=1)
        model_predition = F.softmax(model_predition, dim=1)
        # .cpu().numpy()
        print(a)
                
        # return torch.sigmoid(model_predition)
        return model_predition
        # return map_output(min(1, model_predition))
