import requests
import numpy
import DataTool
import pickle
import time
from PIL import Image
import io
import numpy as np
from bs4 import BeautifulSoup

class SessionManager:
#每次起一个session
#成功之前可以重复地单步尝试
# 尝试可以返回一个boolean，成功为true，失败为false
#还可以封装一个多步地直到成功的登录行为
    CAPTCHA = "https://jwc.scnu.edu.cn/CheckCode.aspx"
    postURL = "https://jwc.scnu.edu.cn/default2.aspx"
    indexURL = "https://jwc.scnu.edu.cn/"
    username = "20153201034"
    password = "ygv369ok"

    def __init__(self):
        self.session = requests.session()
        with open("W.dump", "rb") as f:
            self.Wt = pickle.load(f)

    def getVIEWSATE(self, html):
        soup = BeautifulSoup(html)
        return soup.find(attrs={"name": "__VIEWSTATE"}).get("value")

    def tryOnce(self):
        page = self.session.get(self.indexURL).content
        time_before = time.time()
        pic = self.session.get(self.CAPTCHA).content
        img = Image.open(io.BytesIO(pic))
        sub = DataTool.preProc(img)
        sub = np.concatenate((sub, np.ones((4, 1), dtype=np.uint8)), axis=1)#对图像加一个行/列的1，为了之后的计算
        code = ""
        for j in sub:
            y = np.argmax(np.dot(self.Wt.T, j))
            code = code + DataTool.getKey(y)
        time_after = time.time()
        VIEWSTATE = self.getVIEWSATE(page)
        formData = {"__VIEWSTATE": VIEWSTATE, 
                    "txtUserName": self.username, 
                    "Textbox1":    "",
                    "TextBox2":    self.password, 
                    "txtSecretCode":code, 
                    "RadioButtonList1": "学生", 
                    "Button1": "", 
                    "lbLanguage": "", 
                    "hidPdrs": "", 
                    "hidsc": "", 
        }
        login = self.session.post(self.postURL, data=formData)
        if (BeautifulSoup(login.content).title.text == "正方教务管理系统"):
            return True
        else:
            return False

    def login(self):
        while(not self.tryOnce()):
            continue
        print("Login!")
        return True

if (__name__ == "__main__"):
    s = SessionManager()
    s.login()