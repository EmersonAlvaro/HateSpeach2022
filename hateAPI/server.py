from numpy import source
from utils.VideoSpeechRecognizer import *
from utils.detect import *
from utils.VideoDownload import *
from utils.VideoTextDetector import *


from settings.config import *

import bottle, json
from bottle import route, run,  get, post, request, response, hook
# from gevent import monkey; monkey.patch_all()
# from paste import httpserver

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@route('/', method='GET')
def greetings():
  return "Hi, I am the HateSpeach RESTful API\n"  

@route('/detect', method='POST')
def do_detections():
  
  try:    

    # 1- receive the url through http request.
    # 2- Download the video to /video file
    # ----------- tiktok_crawl.py-----------------   
    
    videoURL = request.forms.get("link")
    videoSource = request.forms.get("videoSource")
      
    print(videoURL)

    logger.info("Request Started .......")

    videoID = VideoDownload(url=videoURL, videoSource=videoSource)
    # print(videoID)
    # 3- Read video file 
    # 3- convert to audio
    # 4- convert to text
    # ------transcripit.py-------------------------

    text_with_chunks  =  VideoSpeechRecognizer(videoID=videoID).join()
  
    # 5- pre-processing the text
    # 6- make predition using bert. 
    # -----------detect.py-------------------------
    
    prediction, text_clean  = Detector(text=text_with_chunks).join()
    # prediction, text_clean  = Detector(text_with_chunks)

    myResponse = {
      "transcript_Video": text_clean,
      "videoID" : videoID, 
      "video_Source" : videoSource, 
      "link" : videoURL,
      "prediction" : prediction
    }

    # 7- send response
    return json.dumps(myResponse)


  except Exception as e:
    response.status = 400
    return "Detection failed"

if __name__ == '__main__':
    run(host='localhost', port=8080, server='gunicorn', timeout = 600, reload=True, workers=1, debug=True)
    # run(host='localhost', port=8080, server='paste')
    # run(host='localhost', port=8080)

app = bottle.default_app()
# application = bottle.default_app()