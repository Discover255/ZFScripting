import numpy as np
import sqlite3
from PIL import Image

conn = sqlite3.connect("label.db")
cursor = conn.cursor()
cursor.execute("SELECT MAX(ind) FROM main")
sumData = cursor.fetchall()[0][0] + 1
sumData = sumData * 4
#使用灰度图像，丢弃色彩信息
X = np.zeros((sumData, 21*12))
Y = np.zeros((sumData, 1), dtype=int)
mapdict = dict()
for i in range(ord("0"), ord("9")+1):
    mapdict[chr(i)] = i - 48
for i in range(ord("a"), ord("z")+1):
    mapdict[chr(i)] = i - 97 + 10


m = 3
n = 2

def getKey(value):
    return list(mapdict.keys())[list(mapdict.values()).index(value)]

def median(col):
    return np.sort(col)[int(m*n/2)]

def filt(A):
    #[3, 2] symmetric 中值
    #建议的流程：填充->拍扁->对行调用函数，只返回一个值到新的矩阵->按顺序还原
    cols = np.zeros((A.shape[0]*A.shape[1], m*n), dtype=np.uint8)
    height = A.shape[0]
    width  = A.shape[1]
    rightPad = A[:, width-1:width-1-n-1:-1]
    leftPad  = A[height-1:height-1-m-1:-1, :]
    crossPad = A[height-1:height-1-m-1:-1, width-1:width-1-n-1:-1]
    Apad = np.concatenate((np.concatenate((A, rightPad), axis=1), np.concatenate((leftPad, crossPad), axis=1)), axis=0)
    V = np.zeros(27*72, dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            area = Apad[i:(i+m), j:(j+n)]
            area = area.reshape(m*n)
            cols[i*width+j] = area
    V = np.asarray(list(map(median, cols)), dtype=np.uint8)
    V = V.reshape(A.shape)
    return V

def preProc(img):
    img = img.convert("L")
    aimg = np.asarray(img, dtype=np.uint8)
    aimg = filt(aimg)
    sub = np.zeros((4, 21*12), dtype=np.uint8)
    sub[0] = aimg[1:22, 5:17].reshape(21*12)
    sub[1] = aimg[1:22, 17:29].reshape(21*12)
    sub[2] = aimg[1:22, 29:41].reshape(21*12)
    sub[3] = aimg[1:22, 41:53].reshape(21*12)
    return sub

for i in range(int(sumData/4)) :
    img = Image.open("images/"+str(i)+".gif")
    # img = img.convert("L")
    # aimg = np.asarray(img, dtype=np.uint8)
    # aimg = filt(aimg)
    sub = preProc(img)
    for j in range(4):
        X[i*4+j] = sub[j]
    cursor.execute("SELECT label FROM main WHERE ind="+str(i))
    label = cursor.fetchall()[0][0]
    for j in range(4):
        Y[i*4+j] = mapdict[label[j]]
print("ok, and number of data is "+str(sumData))