# importing libraries 
from ast import Return
import chunk
import speech_recognition as sr 
import os 
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import AudioFileClip
from pydub.utils import make_chunks
import logging
from queue import Queue
from threading import Thread
from time import time
import threading
import multiprocessing
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings.config import *
from utils.VideoTextDetector import *


class VideoSpeechRecognizer(Thread) :

    def __init__(self, videoID, deleteFilesWhenFinish = False) :
        # create a speech recognition object
        Thread.__init__(self, daemon=True) 
        self.r = sr.Recognizer()
        self.mp4filename = f"{videoID}.mp4"
        self.wavfilename = f"{videoID}.wav"
        self.textFilename = f"{videoID}.txt"
        self.videoID = videoID
        self.deleteFilesWhenFinish = deleteFilesWhenFinish
        self._return = None
        self.audio_txt = None
        self.ocr_text = None
        self.whole_text = [" "]
        self.queue = Queue(maxsize=0)
        self.num_threads = 5
        self.start_time = time()
        self.start()
    

    # convert a large (?) video file mp4 into audio file wav
    def convert_mp4_to_wav(self) :
  
        path_video = str(video_dir.joinpath(self.mp4filename))
        
        audioclip = AudioFileClip(path_video) # Create AudioFileClip instance from module moviepy
        path_audio = str(audio_dir.joinpath(self.wavfilename))
            
        audioclip.write_audiofile(path_audio) # Write wav file 

        return None


    def get_small_audio_transcription(self, queue):

        while True:
            result = queue.get()
            filename = result[0]
            thread_id =result[1]
    
            text = "Error happened"
            # open the file
            with sr.AudioFile(filename) as source:
                # listen for the data (load audio to memory)
                audio_data = self.r.record(source)
                # try recognize (convert from speech to text)

                try:
                    text = self.r.recognize_google(audio_data)
                    text = f"{text.capitalize()}. "
                    print(f'Processing chunck{thread_id}')
                    self.whole_text.insert(thread_id, text)
                except Exception:
                    pass
                # except sr.UnknownValueError as e:
                #     print("Error:", str(e))
                    
            queue.task_done()

    # a function that splits the audio file into chunks
    # and applies speech recognition
    def get_large_audio_transcription(self):
  
        # open the audio file using pydub
        sound = AudioSegment.from_wav(str(audio_dir.joinpath(self.wavfilename)))
          
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500, )
        #chunks = make_chunks(sound, 5000) #Make chunks of millisec
        
        folder_name = str(audio_dir.joinpath(self.videoID))
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        
        for i in range(self.num_threads):
            
            th = threading.Thread(target=self.get_small_audio_transcription, args=(self.queue, ))        
            th.setDaemon(True)
            th.start()            
        
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            
            self.queue.put([chunk_filename,i-1])
            
            # self.get_small_audio_transcription(filename=chunk_filename)
            # whole_text += "\n" + text
        
        self.queue.join()
            
        # return the text for all chunks detected
        return self.whole_text
    
    def save_text(self, text):
        with open(str(txt_dir.joinpath(self.textFilename)), 'w') as f:
            f.write(text)

    def run(self):

        self.start_time = time()
        print(f'Initialize Audio to text at {self.start_time} ')    

        self.convert_mp4_to_wav()
        self.audio_txt = self.get_large_audio_transcription()
        self.ocr_text = VideoTextDetector(videoID=self.videoID).join()
       
        self._return = '\n'.join(self.audio_txt) +"\n" +'\n'.join(self.ocr_text) 
        
        self.save_text(self._return)

    def delete_when_finish(self):
        videopath = video_dir.joinpath(self.mp4filename)
        audiopath = audio_dir.joinpath(self.wavfilename)
        txtpath = txt_dir.joinpath(self.textFilename)
        chunkpath = audio_dir.joinpath(self.videoID)

        #Delete Video
        if os.path.exists(videopath):
            os.remove(videopath)
        #Delete Audio
        if os.path.exists(audiopath):
            os.remove(audiopath)
        #Delete Text
        if os.path.exists(txtpath):
            os.remove(txtpath)
        #Delete Chunck
        if os.path.exists(chunkpath):
            shutil.rmtree(chunkpath, ignore_errors=False, onerror=None) 
        

    def join(self):
        Thread.join(self)
        #Remove all temporar files
        if(self.deleteFilesWhenFinish):
            self.delete_when_finish()      
        
        print(f"Audio to text  end at {time()- self.start_time} seconds")
     
        return self._return

if __name__ == '__main__':
    text_with_chunks =  VideoSpeechRecognizer(videoID="OYAn7-rECE0").join()
    # text_with_chunks = VSRThread.join()
    print(text_with_chunks)