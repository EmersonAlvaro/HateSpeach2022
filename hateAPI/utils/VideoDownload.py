import os
from posixpath import split
import sys
from turtle import down
from numpy import source
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytube
from TikTokApi import TikTokApi

from settings.config import *
# made it a function so that you can call it from any script and just pass in
# the url in ""


def downloadYoutube(url):

    id = url.split("/")[-1]

    print(f"Downloading Video {id} from  Youtube")

    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    print(video.title)
    video.download(filename=video_dir.joinpath(id+".mp4"))
    
    return id


def downloadTikTok(url):

    id = url.split("/")[-1]
    id = id.split("?")[0]

    print(f"Downloading Video {id} from  TikTok")

    with TikTokApi() as api:
        video = api.video(id=id)
        # Bytes of the TikTok video
        video_data = video.bytes()
        with open(video_dir.joinpath(id+".mp4"), "wb") as out_file:
            out_file.write(video_data)
    return id

def downloadFacebook(url):
    pass

def downloadInstagram(url):
    pass

def VideoDownload (url, videoSource="TikTok"):

    if videoSource == "TikTok":
        return downloadTikTok(url)

    elif videoSource == "Facebook":
        return downloadFacebook(url)

    elif videoSource == "Instagram":
        return downloadInstagram(url)

    elif videoSource == "Youtube":
        return downloadYoutube(url)

    else:
        return " Error Source Not Valid"


# if __name__ == '__main__' :
#     # th = VideoDownload(url ="https://www.tiktok.com/@debbraahworld/video/7104965788838153477?is_from_webapp=1&sender_device=pc", videoSource = "TikTok").run()
#     th = VideoDownload(url ="https://youtu.be/uBp6qjJtKC0", videoSource = "Youtube")
#     # .run()
#     print(th)