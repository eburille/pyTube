from pytube import YouTube 

import os
import shutil

from moviepy.editor import *

def Download(link: str):
  #Create a folder for temporary archives
  os.chdir("./")
  os.mkdir("Temporary Folder from PyTube")


  #Responsible to initializate download, getting URL and path
  Youtube_link = link
  download_Folder = "./Temporary Folder from PyTube"
  getVideo = YouTube(Youtube_link) 



  #Download video that will be used as audio
  videoStream = getVideo.streams.filter(
                res = "360p", 
                file_extension = "mp4").first()
  videoStream.download(download_Folder) 
  
  

  #Rename video that will be used as audio
  videoTitle = videoStream.title
  removable = '|'

  for letra in removable:
    if letra in videoTitle:
      videoTitle = videoTitle.replace(letra, '')

  os.chdir( "./Temporary Folder from PyTube")
  os.rename(f'{videoTitle}' + ".mp4", "audioFile.mp4")


  #Download video in preset quality

  videoStream = getVideo.streams.filter(
    only_video = True,  
    file_extension = "mp4").first()
  videoStream.download(".") 
  

  #Join the audio to video 
  clip = VideoFileClip(f'{videoTitle}' + ".mp4")
  audioclip = AudioFileClip("audioFile.mp4")
  videoclip = clip.set_audio(audioclip)

  os.chdir('..')
  videoclip.write_videofile(f'{videoTitle}' + ".mp4")

  #Remove temporary folder
  shutil.rmtree("Temporary Folder from PyTube")
  
  print(f'{videoTitle}' + ".mp4")
  return f'{videoTitle}' + ".mp4"

if __name__ == '__main__':
    link = 'https://youtu.be/w4znPtZsIRI'
    print(link)
    Download(link)