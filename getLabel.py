from flask import Flask, request, redirect
import numpy as np
import requests
import sqlite3
import sys, signal

app = Flask(__name__)
URL = "https://jwc.scnu.edu.cn/CheckCode.aspx"
X = np.zeros((400, 27*11))
Y = np.zeros((400, 1))
print("connecting SQLite")
conn = sqlite3.connect("label.db")
cursor = conn.cursor()
MAXSIZE = 300
print("getting image")
pic = requests.get(URL).content#初始化如果能用XML配置文件就最好了
def int_handler(signum, frame):
    print("closing SQLite connection...")
    cursor.close()
    conn.close()
    sys.exit(0)
signal.signal(signal.SIGINT, int_handler)

cursor.execute("SELECT MAX(ind) FROM main")
count = cursor.fetchall()[0][0] + 1#初始化计数器
if (count>MAXSIZE):
    cursor.close()
    conn.close()
    sys.exit()#退出应该调用函数
print("from index :"+str(count))




@app.route('/')
def mainpage():
    with open("input.html", "rb") as f:
        return f.read()

@app.route("/image")
def showImg():
    #传输一个全局的request抓取的二进制数据
    return pic

@app.route("/save", methods=["POST"])
def save():
    label = request.form["label"]
    global pic
    global MAXSIZE, count, cursor, conn
    with open("images/"+str(count)+".gif", "wb") as f:
        print("storing image "+str(count))
        f.write(pic)
    print("getting image")
    pic = requests.get(URL).content
    cursor.execute("INSERT INTO main (ind, label) VALUES (\'"+str(count)+"\', \'"+label+"\')")
    conn.commit()
    if (count < MAXSIZE):
        count += 1
        print("go on ,and count is "+str(count))
    else:
        print("closing SQLite connection...")
        cursor.close()
        conn.close()
        sys.exit(0)
        #否则返回退出退出页面
    return redirect("/", code=302)
    #存储进Y，并重新爬取

# @app.route("/temp")
# def uhh():
#     return request.form["label"]

app.run()