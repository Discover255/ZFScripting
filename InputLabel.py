from flask import Flask, request, redirect
import requests
import sqlite3
import sys, signal

app = Flask(__name__)
URL = "https://jwc.scnu.edu.cn/CheckCode.aspx"

if (__name__ == "__main__"):
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
    if (count>MAXSIZE):
        with open("error.html", "rb") as f:
            return f.read()
    else:
        with open("input.html", "rb") as f:
            return f.read()

@app.route("/image")
def showImg():
    #传输一个全局的request抓取的二进制数据
    return pic

@app.route("/save", methods=["POST"])
def save():
    label = request.form["label"]

    #这一段是保存label和图片，并重新获取图片
    global pic, count
    global MAXSIZE, cursor, conn

    if (count <= MAXSIZE):
        with open("images/"+str(count)+".gif", "wb") as f:
            print("storing image "+str(count))
            f.write(pic)
        print("getting image")
        pic = requests.get(URL).content
        cursor.execute("INSERT INTO main (ind, label) VALUES (\'"+str(count)+"\', \'"+label+"\')")
        conn.commit()
        count += 1
    return redirect("/", code=302)
if (__name__ == "__main__"):
    app.run()