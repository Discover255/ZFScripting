#-*- coding:utf-8-*-
import numpy as np
import dataTool
import pickle
import requests
from PIL import Image
import io
from bs4 import BeautifulSoup
import time

X = dataTool.X
Y = dataTool.Y
imgSize = 21*12
sumData = dataTool.sumData
W = np.random.rand(imgSize+1, 36)*0.0001
X = np.concatenate((X, np.ones((X.shape[0], 1))), axis=1)
delta = 5
L = 0.0001
alpha = 0.00002
URL = "https://jwc.scnu.edu.cn/CheckCode.aspx"

def save(W):
    with open("W.dump", "wb") as f:
        pickle.dump(W, f)

def train(X, Y):
    ac = np.zeros(sumData)
    global W
    while (np.sum(ac)*100/sumData) <= 99.0:
        loss = 0.0
        dW = np.zeros((imgSize+1, 36))
        ac = np.ones(sumData)
        for i in range(sumData):
            z = np.dot(W.T, X[i])
            dz = np.zeros(36)
            for j in range(z.shape[0]):
                if j == Y[i]:
                    continue
                margin = z[j] - z[Y[i]] + delta
                if margin - delta > 0:
                    ac[i] = 0
                if margin > 0:
                    loss += float(margin)
                    dz[j] = 1
                    dW[:, j] += X[i]
                    dW[:,int(Y[i])] = (-X[i])
            

        loss /= sumData
        dW /= sumData

        #regularization
        print("loss: "+str(loss)+" accuracy: "+str(np.sum(ac)*100/sumData)+"%")
        loss += L * np.sum(dW * dW)
        dW += L * W
        W -= alpha * dW

def getVIEWSATE(html):
    soup = BeautifulSoup(html)
    return soup.find(attrs={"name": "__VIEWSTATE"}).get("value")

def test(num):
    username = "2015"
    password = ""
    count = 0
    with open("W.dump", "rb") as f:
        Wt = pickle.load(f)
    for i in range(num):
        session = requests.session()
        page = session.get("https://jwc.scnu.edu.cn/").content
        pic = session.get(URL).content
        img = Image.open(io.BytesIO(pic))
        sub = dataTool.preProc(img)
        sub = np.concatenate((sub, np.ones((4, 1), dtype=np.uint8)), axis=1)
        code = ""
        for i in sub:
            y = np.argmax(np.dot(Wt.T, i))
            code = code + dataTool.getKey(y)
        VIEWSTATE = getVIEWSATE(page)
        formData = {"__VIEWSTATE": VIEWSTATE, 
                    "txtUserName": username, 
                    "Textbox1":    "",
                    "TextBox2":    password, 
                    "txtSecretCode":code, 
                    "RadioButtonList1": "学生", 
                    "Button1": "", 
                    "lbLanguage": "", 
                    "hidPdrs": "", 
                    "hidsc": "", 
        }
        login = session.post("https://jwc.scnu.edu.cn/default2.aspx", data=formData)
        if (BeautifulSoup(login.content).title.text == "正方教务管理系统"):
            print("success and code is "+code)
            count += 1
        else:
            print("failed and code is "+code)
        
    print("accuracy: "+str(count*100/num))


if (__name__ == "__main__"):
    train(X, Y)
    save(W)
    #test(20)