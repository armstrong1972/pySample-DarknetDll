# coding: utf-8
# 
# 程序功能 ：调用 DarkNet DLL，识别图像中的物体

import os
import cv2
import time
import darknet

netMain = None
altNames = None
netW = 0
netH = 0

def cvShowDetections(detections, img):
    h,w = img.shape[:2]
    pw, ph = w/netW, h/netH
    for detection in detections:
        x, y, w, h = int(detection[2][0]*pw), int(detection[2][1]*ph), int(detection[2][2]*pw), int(detection[2][3]*ph)
        #print(x,y,w,h)
        w2 = w >> 1
        h2 = h >> 1
        cv2.rectangle(img, (x-w2,y-h2), (x+w2,y+h2), (0, 255, 0), 1)
        #
        cv2.putText(img,
                    altNames[detection[0]] +
                    " [" + str(round(detection[1] * 100, 1)) + "]",
                    (x-w2, y-h2-5), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    [0, 0, 255], 1)


def Init_YOLO3( configPath = "./mod/yolov3.cfg" ,
                weightPath = "./mod/yolov3.weights" ,
                namesPath  = "./mod/coco.names" ):

    global  netMain, altNames, netW, netH

    curPath = os.path.dirname(__file__)
    configPath = os.path.abspath(os.path.join(curPath, configPath))
    weightPath = os.path.abspath(os.path.join(curPath, weightPath))
    namesPath  = os.path.abspath(os.path.join(curPath, namesPath))

    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" + os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" + os.path.abspath(weightPath)+"`")
    if not os.path.exists(namesPath):
        raise ValueError("Invalid data file path `" + os.path.abspath(namesPath)+"`")
    
    if altNames is None:
        try:
            if os.path.exists(namesPath):
                with open(namesPath,encoding='utf8') as namesFH:
                    namesList = namesFH.read().strip().split("\n")
                    altNames = [x.strip() for x in namesList]
                    #print(altNames)
        except TypeError:
            pass
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
        netW, netH = darknet.network_width(netMain), darknet.network_height(netMain)

        print("Inited the YOLO [%d,%d]" % (netW, netH))


def Detect_Image(img) :
    darknet_image = darknet.make_image(netW, netH, 3)                      

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb,
                                (darknet.network_width(netMain),
                                 darknet.network_height(netMain)),
                                interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image,img_resized.tobytes())

    detections = darknet.detect_image(netMain, altNames, darknet_image, thresh=0.5)
    #print("ID_detections = " , id(detections))
    return detections

