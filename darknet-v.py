# coding: utf-8
# 
# 程序功能 ：调用 DarkNet DLL，识别视频中的物体

import os
import cv2
import time
from yolo import *

def dect_video(videoPath,winName) :
    curPath = os.path.dirname(__file__)
    videoPath  = os.path.abspath(os.path.join(curPath, videoPath))

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(videoPath)

    ret = True
    while ret:
        prev_time = time.time()
        ret, img = cap.read()
        if ret :
            dets = Detect_Image(img)
            cvShowDetections(dets, img)
            cv2.imshow(winName, img)

            t= time.time()-prev_time
            print("FPS = %.2f , time=%.2fs" % (1/t,t))

            k = cv2.waitKey(1)
            if k == 27 : #Esc
                ret = False
                
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Init_YOLO3()
    videoPath = "./img/v1.mp4"
    dect_video(videoPath,os.path.basename(videoPath))


                
        
