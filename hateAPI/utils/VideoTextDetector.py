# Import required packages
import cv2
import pytesseract
import os
import re
import sys
import numpy as np
import logging
from queue import Queue
from threading import Thread
from time import time
import threading
import multiprocessing

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings.config import *

class VideoTextDetector(Thread):

    def __init__(self, videoID, seconds=2):
        Thread.__init__(self, daemon=True) 
        self.mp4filename = f"{videoID}.mp4"
        self.textFilename = f"{videoID}.txt"
        self._return = None
        self.queue = Queue(maxsize=0)
        self.num_threads = 5
        self.whole_text = [None]
        self.num_seconds = seconds
        self.start()
        # tesseract dir 
        # pytesseract.pytesseract.tesseract_cmd = '/home/emerson/miniconda3/bin/tesseract'

    def pre_processing(self, frame) :
 
        # Preprocessing the image starts
        invert = cv2.bitwise_not(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

        return dilation

    def clean_text(self, text):
  
        # Post-processing the text : We remove the blanks and newlines
        if text != '\x0c' or text != ' \x0c' :
            # Remove unnecessary \n
            text = re.sub(r'( )?\n( )?(( )?\n( )?)*( )?' , r' ',text)
            # Remove unnecessary new lines
            text = re.sub(r'( )?\x0c( )?(( )?\x0c( )?)*( )?', r' ', text) 
            # Remove trailing spaces
            text = text.strip()
        
        return text

    def frame_to_string (self, queue):
        
        while True:
            result = queue.get()
            frame = result[0]
            thread_id =result[1]
            framenbr =result[2]
            print(f"Process frame {framenbr} Thread_id {thread_id}")

            pre_proc_frame = self.pre_processing(frame)

            contours, hierarchy = cv2.findContours(pre_proc_frame, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            # Creating a copy of image
            im2 = frame.copy()

            # Looping through the identified contours
            # Then rectangular part is cropped and passed on
            # to pytesseract for extracting text from it
            # Extracted text is then written into the text file
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                
                # Drawing a rectangle on copied image
                rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Cropping the text block for giving input to OCR
                cropped = im2[y:y + h, x:x + w]

                # Apply OCR on the cropped image
                text = pytesseract.image_to_string(cropped)
                text_c = self.clean_text(text)
                self.whole_text.insert(thread_id, text_c)
            
            queue.task_done()
    
    def run(self) :

        self.start_time = time()
        print(f'Initialize Ocr text recognition  at {time} ') 
      
        for i in range(self.num_threads):            
            th = threading.Thread(target=self.frame_to_string, args=(self.queue, ))        
            th.setDaemon(True)
            th.start() 

        videopath = str(video_dir.joinpath(self.mp4filename))        
        videocap = cv2.VideoCapture(videopath)

        video_fps = int(videocap.get(cv2.CAP_PROP_FPS)) 
        video_frame_count = int(videocap.get(cv2.CAP_PROP_FRAME_COUNT))

        success, frame = videocap.read()
        framenbr = 0
        i = 0

        while success:

            framenbr += 1
            
            success, frame = videocap.read()
            if not success: # Means we reached the end of video
                break         
            # We process only 1 every 2 seconds (fps times 2)  to avoid redundacies and save time
            # consider that the most video a 24fps.
            if framenbr % (video_fps*2) != 1 :
                continue

            self.queue.put([frame,i, framenbr])
            i +=1

        self.queue.join() 

        self.whole_text = list(filter(None, self.whole_text))
        
        self._return = self.whole_text
        

    def join(self):
        Thread.join(self)
        print(f"Ocr text recognition end at {time()- self.start_time} seconds")
        return self._return


if __name__ == '__main__':
   
    # start_time = time() 
    text_Video = VideoTextDetector(videoID="uBp6qjJtKC0").join()
    print(text_Video)
    # print(f"Program finished in {time()-start_time} seconds")
