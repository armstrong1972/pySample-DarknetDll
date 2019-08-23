# coding: utf-8
# 
# 程序功能 ：调用 DarkNet DLL，识别图片中的物体

import os
import cv2
import time
from yolo import *

def dect_image(picPath,winName) :
    prev_time = time.time()
    curPath = os.path.dirname(__file__)
    picPath  = os.path.abspath(os.path.join(curPath, picPath))
    
    img = cv2.imread(picPath)
    dets = Detect_Image(img)
    #print(id(dets))
    cvShowDetections(dets, img)
    cv2.imshow(winName, img)
    print("Time = %.2fs" % (time.time()-prev_time))


if __name__ == "__main__":
    Init_YOLO3()

    n = 0
    b = True
    while b :
        n += 1
        if n>6 :
            n=1
        picPath    = "./img/jj%03d.jpg" % n
        dect_image(picPath,os.path.basename(picPath))

        k = cv2.waitKey(0)
        if k ==27 :
            b = False
              
    cv2.destroyAllWindows()
