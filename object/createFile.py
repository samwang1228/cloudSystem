from venv import create
import cv2
import os
from pydub import AudioSegment
from moviepy.editor import *
import wave
import math
import pyaudio
# import numpy
import numpy as np
import urllib.request

import pandas as pd
class CreateFile():
    def __init__(self,root,video_name):
        self.root=root
        self.video_name=os.path.splitext(video_name)[0] 
        self.video_folder=root+self.video_name+"\\"
        self.voice_folder=self.video_folder+'voice'
        self.v_f=self.video_folder+'video\\'
    
    # voice_path='v1.mp3'
    def createWavFile(self):
        if not os.path.isdir(self.voice_folder): # create voice folder
            os.mkdir(self.voice_folder) 
        video = VideoFileClip(os.path.join(self.root+self.video_name+'.mp4')) # read mp4
        video.audio.write_audiofile(os.path.join(self.voice_folder+'\\'+self.video_name+'.mp3')) # create mp3
        sound = AudioSegment.from_mp3(self.voice_folder+"\\"+self.video_name+'.mp3') # read mp3
        sound.export(self.voice_folder+"\\"+self.video_name+'.wav', format="wav") # create wav

    def createFrame(self):
        if not os.path.isdir(self.video_folder): # create voice folder
            os.mkdir(self.video_folder) 
        if not os.path.isdir(self.v_f): # create voice folder
            os.mkdir(self.v_f) 
        frame_count = 0 
        cap = cv2.VideoCapture(self.root+self.video_name+'.mp4') #你的video 路徑
        if cap.isOpened():
            success = True
        else:
            success = False
            print("讀取失敗!")
        sec=0
        pre_sec=0
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        print(f'fps={fps}')
        while(success):
            success, frame = cap.read()
            if(frame_count% fps==0):
                
                if not os.path.isdir(self.v_f+str(sec)): # create voice folder
                    os.mkdir(self.v_f+str(sec))
                pre_sec=sec
                sec+=fps 
                
            if success is False:
                print("---> 第%d張讀取失敗:" % frame_count)
                break
            # print(f'test{frame}')
            # url = 'http://www.pyimagesearch.com/wp-content/uploads/2015/01/google_logo.png'
            # resp = urllib.request.urlopen(frame)
            # frame = np.asarray(bytearray(frame), dtype="uint8")
            # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
 
            # cv2.imdecode()
            
            # cv2.imdecode(f'{self.video_folder}{str(pre_sec)}\\{str(frame_count)}.jpg')
            # self.f.save(os.path.join(f'{self.video_folder}{str(pre_sec)}'))
            # cv2.imwrite('static\\uploads\\user\\test1\\0\\'+str(pre_sec)+'.jpg',frame) #要寫檔的位置
            cv2.imencode('.jpg', frame)[1].tofile(f'{self.v_f}{str(pre_sec)}\\{str(frame_count)}.jpg') #中文要用這個
            # print("pre",pre_sec) 
             
            # print(frame_count,frame_count%fps)
            frame_count=frame_count+1
        cap.release()
        cv2.destroyAllWindows()
             
    def create(self):
        self.createFrame()
        self.createWavFile()

# iroot='C:\\Users\\user\\Desktop\\project_code\\v2i\\' #影片的位置
# ivideo_name='test1.mp4' #影片的名字
 
# res=CreateFile(root=iroot,video_name=ivideo_name)
# res.create()
        

