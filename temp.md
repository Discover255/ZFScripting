## 模型选择
此处选择linear classifier线性分类器，使用梯度下降。为了简化模型，对每个字符拆分，因此所有输入的图像可以分成36个类。
根据滤波的实验结果，选择是否使用RGB三个通道。
loss function使用cs231n中的多分类svm loss function即
```javascript
L[i] = SUM for j != y[i]:(s[y[i]], s[j]) => { 
    if (s[y[i]] >= s[j] + delta)
        retexiurn 0
    else
        return s[j] - s[y[i]] + delta
}

也就是note里的
L[i] = SUM for j != y[i] max(0, s[j] - s[y[i]] +delte)
```
delta是人为设置的边际


最终的L=Li的算术平均，i是样本的index，所以L衡量了模型对于所有样本的性能


通常用hinge loss的平方，平方对于大的错误更敏感，对小错误更不敏感


还提到了正则化的意义。假如分类器以错误的函数优秀地拟合了旧数据，在引入新数据的时候，如何确保分类器能够改变错误的函数从而正确地拟合呢，即使在旧数据上表现更差？除非data loss which will tell our classifier that it should fit the training data，都需要在loss function后加一个正则项。这样loss就包括了data loss 和 regularization loss两项，这里rl还有一个lambda超参数

softmax使用了不一样的loss function，它是将s=Wx代入到logistic函数，loss function将一个值取负对数
***
### 梯度下降
>note: 使用有限差分法也可以找到导数，但是速度慢。为什么要求导呢？求导可以找到loss下降最快的方向

```python
while True:
    weights_grad = evaluate_gradient(loss_fun, data, weights)
    weights += - step_size * weights_grad
    #step_size步长与cs229的alpha学习率相同
    #实际中，data数量非常大，所以常随机取出一些来用于梯度下降
while True:
    data_batch = sample_training_data(data, 256)
    weights_grad = evaluate_gradient(loss_fun, data_batch, weights)
    weights += - step_size * weights_grad
```
> 可以看作是真实数值的蒙特卡洛估计

#### 使用梯度下降训练线性分类器
> 在深度NN大规模使用之前，通常使用两部走，先取得图像的特征量，再输入NN
一个特征表示的例子是颜色直方图，一以及方向梯度直方图

这里使用最简单的反向传播NN。回到上面的求导，这里推导解析梯度，用于求解数值梯度（使用链式求导chain rule）。
> max gate是一个gradient router, multiple gate是gradient switcher