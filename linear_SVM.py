import numpy as np
import dataTool
import pickle

X = dataTool.X
Y = dataTool.Y
imgSize = 21*12
sumData = dataTool.sumData
W = np.random.rand(imgSize+1, 36)*0.0001
X = np.concatenate((X, np.ones((X.shape[0], 1))), axis=1)
delta = 5
L = 0.0001
alpha = 0.00002

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
                #print(str(margin) + " = " + str(z[j]) + "-" + str(z[Y[i]]) + "+" + str(delta))
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
if (__name__ == "__main__"):
    train(X, Y)
    #save(W)