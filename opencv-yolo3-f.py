# coding: utf-8
# 
# 程序功能 ：调用 Yolo3 库，识别图片中的 object

import cv2 as cv
import numpy as np
import opencv_yolo3 as yolo3
import time

fClasses       = "./mod/coco.names"
modelCfg       = "./mod/yolov3.cfg"
modelWeights   = "./mod/yolov3.weights"
# 初始化对象
bt = time.time()
yolo = yolo3.CV_Yolo3(fClasses)
print(len(yolo3.Yolo3_Classes))
# 设置配置文件
yolo.cv_dnn_init(modelCfg,modelWeights)
t1 = time.time()
print("Time of Init Yolo  :", t1-bt)

image_path  = "./img/jj001.jpg"
img=cv.imread(image_path)
dects, runtime = yolo.yolov3_predict(img) # 识别图片, 返回 对象集 和 运行时间
t2 = time.time()
print("Time of Detect Img :", t2-t1)
#print(dects)

yolo3.Yolo3_ShowInfos(img, dects, runtime)
