# coding: utf-8
# 
# 程序功能 ：实时抓取屏幕鼠标为中心的 416x416 画面，并注册热键
#      F9  ：Zoom Out
#      F10 ：Zoom In
#      F11 ：保存 416x416 画面
#      ESC : 退出


import numpy as np              #数据处理的库numpy
import cv2                      #图像处理的库OpenCv
import pyautogui as pag         #截屏库

import time, os
import win32con
import ctypes
import ctypes.wintypes
import threading

RUN    = False
EXIT   = False
ZOOM   = 100    # percentage

user32 = ctypes.windll.user32  #加载user32.dll
id_F9  = 109 #注册热键的唯一id，用来区分热键
id_F10 = 110
id_F11 = 111
id_ESC = 112


class Hotkey(threading.Thread):  #创建一个Thread.threading的扩展类  
    def run(self):  
        global EXIT  #定义全局变量，这个可以在不同线程间共用。
        global RUN   #定义全局变量，这个可以在不同线程间共用。
        global ZOOM

        if not user32.RegisterHotKey(None, id_F9, 0, win32con.VK_F9):    # 注册快捷键F7并判断是否成功，该热键用于执行一次需要执行的内容。  
            print("Unable to register id :", id_F9) # 返回一个错误信息
            
        if not user32.RegisterHotKey(None, id_F10, 0, win32con.VK_F10):    # 注册快捷键F8并判断是否成功，该热键用于执行一次需要执行的内容。  
            print("Unable to register id :", id_F10) # 返回一个错误信息
            
        if not user32.RegisterHotKey(None, id_F11, 0, win32con.VK_F11):    # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。  
            print("Unable to register id :", id_F11) # 返回一个错误信息

        if not user32.RegisterHotKey(None, id_ESC, 0, win32con.VK_ESCAPE):  # 注册快捷键F10并判断是否成功，该热键用于结束程序，且最好这么结束，否则影响下一次注册热键。  
            print("Unable to register id :", id_ESC)

        #以下为检测热键是否被按下，并在最后释放快捷键  
        try:  
            msg = ctypes.wintypes.MSG()  

            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:

                    if msg.message == win32con.WM_HOTKEY:  
                        if msg.wParam == id_F9:
                            ZOOM += 5
                            print("Zoom=%d%%" % (ZOOM))
                        elif msg.wParam == id_F10:
                            ZOOM = max(5,ZOOM-5)
                            print("Zoom=%d%%" % (ZOOM))
                        elif msg.wParam == id_F11:
                            RUN = True
                        elif msg.wParam == id_ESC:
                            EXIT=True
                            return

                    user32.TranslateMessage(ctypes.byref(msg))  
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            #必须得释放热键，否则下次就会注册失败，所以当程序异常退出，没有释放热键，
            #那么下次很可能就没办法注册成功了，这时可以换一个热键测试
            user32.UnregisterHotKey(None, id_F9)
            user32.UnregisterHotKey(None, id_F10)
            user32.UnregisterHotKey(None, id_F11)
            user32.UnregisterHotKey(None, id_ESC)


YoloSize=416
#YoloHalf=208
Scr_W, Scr_H = pag.size()
print("Screen : %d x %d"%(Scr_W, Scr_H))
FileNo = int(input("请输入图片起始编号(cap目录中):"))
curPath = os.path.dirname(__file__)


hotkey = Hotkey()  
hotkey.start()
b=True
while(b) :
    YoloHalf = int(YoloSize * ZOOM / 200)
    YoloHalf_2 = YoloHalf + YoloHalf
    mX, mY = pag.position()
    mX = min(max(YoloHalf,mX),Scr_W-YoloHalf)
    mY = min(max(YoloHalf,mY),Scr_H-YoloHalf)

    #print(mX-YoloHalf,mY-YoloHalf,YoloSize,YoloSize)
    bt = time.time()
    
    scr = np.array(pag.screenshot(region=(mX-YoloHalf,mY-YoloHalf,YoloHalf_2,YoloHalf_2)))
    img = cv2.cvtColor(scr,cv2.COLOR_BGR2RGB)
    if ZOOM != 100 :
        img = cv2.resize(img,(YoloSize,YoloSize))


    #print(img.shape[:2])
    et = time.time()
    cv2.imshow('rec',img)
    cv2.waitKey(10)
    if RUN==True:
        #这里放你要用热键启动执行的代码
        print("Hotkey = F11 , Save img %5d.jpg" % (FileNo))
        fn = os.path.abspath(os.path.join(curPath, "cap/%05d.jpg"%(FileNo)))
        cv2.imwrite(fn,img)
        FileNo+=1
        #print(et-bt)

        RUN=False
    elif EXIT==True:
        b=False
    time.sleep(0.1)

cv2.destroyAllWindows()
