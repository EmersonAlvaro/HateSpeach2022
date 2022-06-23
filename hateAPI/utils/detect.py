# importing libraries 

import os, sys
from statistics import mode
import numpy
import tensorflow as tf
import re
import tensorflow_text as text
import logging
from queue import Queue
from threading import Thread
from time import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings.config import *
from core.load_model import Bert_Model_Tensorflow
from core.load_model import Bert_Model_Pytorch
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
tf.get_logger().setLevel(logging.ERROR)


# if default_model =="tensorflow":


# elif default_model =="pytorch":
#     # Model class must be defined somewhere
#     model = Bert_Model_Pytorch()
   
class Detector(Thread):

    def __init__(self, text) :
        Thread.__init__(self, daemon=True) 
        self.model = Bert_Model_Tensorflow()
        self.text = text
        self.text_cleaned = None
        self.model_predition = None
        self.start()

    def clean_text(self, tweet) :
        if not isinstance(tweet, str) :
            return 'DATA TO REMOVE'
        lower_cased = tweet.lower() # Put in lower case for easier processing
        removed_mentions_email = re.sub('[^ ]?@[^ ]*', '', lower_cased) # Remove mentions and e-mails
        
        url_pattern = re.compile(r'https?://\S+|www\.\S+') # find urls
        removed_urls = url_pattern.sub(r'', removed_mentions_email) # Removes urls
        
        removed_numbers = re.sub('[0-9]', '', removed_urls) # Remove numerical data
        removed_punc = re.sub('[^a-zA-Z ]*', '', removed_numbers) # Remove punctuations
        removed_trailing_spaces = re.sub(' +', ' ', removed_punc).strip() # Removes useless spaces 

        removed_rt = re.sub(' rt ', ' ', removed_trailing_spaces) # Remove 'RT' words in middle of texts
        splitted = removed_rt.split(' ', 1) # = [first word, rest of tweet]
        if splitted[0] == 'rt' : # We remove the rt at beggining of the text (first word)
            try : 
                cleaned_tweet = splitted[1]
            except IndexError : # This means the tweet is smthg like "rt USERNAME". It's useless we can remove it
                cleaned_tweet = 'DATA TO REMOVE'
        else :
            cleaned_tweet = removed_rt      
        return cleaned_tweet 
    

    def run (self):
        self.text_cleaned = self.clean_text(self.text) 
        input = [self.text_cleaned]
        print(" Doing Prediction ")
        model_predition = self.model.predict(input)
        
        print("Prediction Done ")
        self.model_predition = model_predition

        # return self.model_predition, self.text_cleaned
        
    def join(self):
        Thread.join(self)
        return self.model_predition, self.text_cleaned

# def Detector(text):
#     input = [text]
#     model = Bert_Model_Tensorflow()
#     print(" Doing Prediction ")
#     model_predition = model.predict(input)
#     print("Prediction Done ")

#     return model_predition, text

def main() :
    # score, text_c = Detector(text="!!!!!!!!!!!!! RT @ShenikaRoberts: The shit you hear about me might be true or it might be faker than the bitch who told it to ya &#57361;").join()
    # score, text_c = Detector(text="@MarkRoundtreeJr: LMFAOOOO I HATE BLACK PEOPLE https://t.co/RNvD2nLCDR This is why there's black people and niggers")
    # .join() 
    score, text_c = Detector(text=" I love you baby ")
    # .join()

    print("\n")
    print('Results from the saved model:')
    print(f"Text Processed : {text_c}")
    print(f"Prediction : {score} ")
    print("\n")

if __name__ == '__main__' :
    main()


