#-*- coding:utf-8-*-
import numpy as np
import DataTool
import pickle
import requests
from PIL import Image
import io
from bs4 import BeautifulSoup
import time
import SessionManager
import datetime

X, Y = DataTool.getXY()
imgSize = 21*12
sumData = DataTool.sumData
W = np.random.rand(imgSize+1, 36)*0.0001
X = np.concatenate((X, np.ones((X.shape[0], 1))), axis=1)
delta = 5
L = 0.0001
alpha = 0.00002

def save(W, name="W.dump"):
    with open(name, "wb") as f:
        pickle.dump(W, f)

#这是循环实现的
def train_naive(X, Y):
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
                    dW[:,int(Y[i])] += (-X[i]) #之前忘了带加号
            

        loss /= sumData
        dW /= sumData

        #regularization
        print("loss: "+str(loss)+" accuracy: "+str(np.sum(ac)*100/sumData)+"%")
        loss += L * np.sum(dW * dW)
        dW += L * W
        W -= alpha * dW

#向量实现的
def train_vectorized(X, Y):

    """
    Structured SVM loss function, vectorized implementation.
    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape) # initialize the gradient as zero
    num_train=X.shape[0]
    num_classes = W.shape[1]

    #这里是numpy的一个feature，可以让(h1, w1) dot (h2, w2)得到(h2, w1)
    #具体应该是(h2, w2)拆分成一个个(w2)向量，(w2) dot (h1, w1)就得到一个(w1)向量
    #这些向量叠加h2次，就成了(h2, w1)的矩阵
    #所以这里是m个样本的score构成的矩阵
    scores = np.dot(X, W)
    #这里得到一个500*10的矩阵,表示500个image的ground truth
    #分了两步，先得到了m*1的矩阵
    correct_class_score = scores[np.arange(num_train),Y]
    #重复10次,得到500*10的矩阵,才可以和scores相加相减
    correct_class_score = np.reshape(np.repeat(correct_class_score,num_classes),(num_train,num_classes))
    margin = scores-correct_class_score+delta
    margin[np.arange(num_train),Y]=0

    loss = (np.sum(margin[margin > 0]))/num_train
    loss+=L*np.sum(W*W)

    #gradient
    margin[margin>0]=1
    margin[margin<=0]=0

    row_sum = np.sum(margin, axis=1)                  # 1 by N
    margin[np.arange(num_train), Y] = -row_sum
    dW += np.dot(X.T, margin)     # D by C
    dW/=num_train
    dW += L * W
    return loss, dW

def train_loop(times, name="W.dump"):
    global W
    print("Start training at " + datetime.datetime.now().ctime())
    for i in range(times):
        loss, dW = train_vectorized(X, Y)
        W -= alpha * dW
    print("Train finished")
    save(W, name=name)


def test(num, Wname="W.dump"):
    count = 0
    with open(Wname, "rb") as f:
        Wt = pickle.load(f)
    for i in range(num):
        session = SessionManager.SessionManager()
        res = session.tryOnce()
        if (res):
            print("success")
            count += 1
        else:
            print("failed")
        print("accuracy: %.3f" % float(count*100/(i+1)) + "%")
        time.sleep(2)


if (__name__ == "__main__"):
    # train_naive(X, Y)
    # save(W)
    # train_loop(3000000, name="W.vetorized.dump")
    test(100, Wname="W.vetorized.dump")