import os
from posixpath import split
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import threading
import time
from threading import Thread
from queue import Queue
from datetime import datetime
from settings.config import *


class Seerver_test(Thread):
    
    def __init__(self, threadID, url, videoSource = "TikTok"):
        Thread.__init__(self, daemon=False)
        self.url =url
        self.videoSource = videoSource
        self.threadID = threadID
        self._return = None
        self.start()

    def run(self):

        print('Initialize thread -{thread_id} at {time} ' .format(thread_id =self.threadID, time= time.asctime() ))

        self.session = requests.Session()

        self.data = {
            "link": self.url, 
            "videoSource": self.videoSource
        }

        try:
            self.response = self.session.post(url=URL_API + "/detect", data=self.data)                
            print(self.response.status_code)

            self.response = self.response.content

        except:
            self.response = requests.exceptions.RequestException
        
        self._return = self.response
        print('Exiting thread - {thread_id} at {time} ' .format(thread_id =self.threadID, time = time.asctime()))

        self.session.close()

        return None

    def join(self):
        return self._return


if __name__ == '__main__':
    th = Seerver_test(threadID=6 ,url="https://youtu.be/uBp6qjJtKC0", videoSource="Youtube")
    print(th.join())
