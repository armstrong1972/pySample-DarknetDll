# -*- coding: utf-8 -*-
import os;
import random
import shutil;

CLASSES = {}

def CreateImageListTextFile(path_Images,v_per):
    filelist = os.listdir(path_Images);  # 该文件夹下所有的文件（包括文件夹）
    filelist.sort()

    for files in filelist:  # 遍历所有文件
        Olddir = os.path.join(path_Images, files);  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue
        fn , ext =  os.path.splitext(files)
        if ext == ".txt" :
            f_txt = os.path.abspath(os.path.join(path_Images,files))
            f_jpg = os.path.abspath(os.path.join(path_Images,fn + '.jpg'))
            if os.path.isfile(f_jpg) :
                f = open(f_txt, 'r')
                for line in f.readlines():
                    cid,x,y,w,h = line.split()
                    #print(cid)
                    CLASSES.setdefault(cid,set()).add(f_jpg)

    #print(len(CLASSES))

    fT = open(txtf_TrainID, 'w')
    fV = open(txtf_ValidID, 'w')

    for cls in CLASSES :
        n = len(CLASSES[cls])
        v = int(n * v_per / 100)
        print(cls,n,v)

        i=0
        for jpg in CLASSES[cls]:
            flg = "Training"
            if random.randint(0,99) <= v_per :
                i += 1
                if i<=v :
                    flg = "Validate"

            if flg == "Training" :
                fT.write(jpg)
                fT.write("\n")
            else :
                fV.write(jpg)
                fV.write("\n")
                    
    fT.close()
    fV.close()
 
#curPath = os.getcwd()
curPath = os.path.dirname(__file__)
txtf_TrainID = os.path.abspath(os.path.join(curPath, "trainImages.txt"))
txtf_ValidID = os.path.abspath(os.path.join(curPath, "validImages.txt"))

path_Images  = ""
while path_Images == "":
    path_Images = input("\n[Note : You can drag the folder to this window !]\nMaterials(created by labelImg.exe) Path :")
    if not os.path.isdir(path_Images) :
        path_Images  = ""


try :
    val_Per = int(input("Input the % of Validate Sets (default=30%) :"))
except :
    val_Per = 30

print("\nValidate Sets : %d%%" %(val_Per))
CreateImageListTextFile(path_Images,val_Per) 

print("trainImages.txt && validImages.txt have been created!\nPls copy follow 2 lines to your xxx.data file : \n")
print("train = " + txtf_TrainID)
print("valid = " + txtf_ValidID)
print("\n")