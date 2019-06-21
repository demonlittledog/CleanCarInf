import numpy as np
import pandas as pd


# 对象存储
import pickle


# 定义激活函数 sigmod 和损失函数 dsigmod
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def dsigmoid(x):
    return x * (1 - x)


# 搭建神经网络
# 把感知器的创建,权值的更新,模型的检验封装在一个类
class NeuralNetwork:  # Neuron神经
    def __init__(self, layers):
        self.n = 0
        self.lr = 0.03  # lr 学习率 learn rate
        self.accuracy = 0
        # 权值的初始化，范围-1到1
        # 2层网络, 2个权值向量, 与各自输入元素个数对应
        self.V = np.random.random(
            (layers[0] + 1, layers[1] + 1)
        ) * 2 - 1
        self.W = np.random.random(
            (layers[1] + 1, layers[2])) * 2 - 1

    def setData(self, dataIn, labIn, dataTest, labTest):
        # 添加偏置, 令输入数据集增添一个列,值为1
        temp = np.ones([dataIn.shape[0], dataIn.shape[1] + 1])
        temp[:, 0:-1] = dataIn
        self.X = temp
        self.Y = labIn
        self.X_test = dataTest
        self.Y_test = labTest

    def train(self,t):
        # 训练
        # 随机选取一个数据
        self.n += 1
        i = np.random.randint(self.X.shape[0])
        x = [self.X[i]]  # python list,不能直接参与矩阵运算
        # 转为numpy数组
        x = np.array(x)

        # 计算两个层的输出
        L1 = sigmoid(np.dot(x, self.V))
        L2 = sigmoid(np.dot(L1, self.W))

        # 计算梯度
        # 首先计算输出层
        L2_delta = (self.Y[i] - L2) * dsigmoid(L2)
        # 计算隐藏层的时候, 依据输出层的输出作为反馈(反向传递)
        L1_delta = np.dot(L2_delta, self.W.T) * dsigmoid(L1)

        # 更新权值向量
        self.W += self.lr * np.dot(L1.T, L2_delta)
        self.V += self.lr * np.dot(x.T, L1_delta)
        return self.accuracy > t

    def test(self):
        # 获取预测结果
        predictions = []
        for j in range(self.X_test.shape[0]):
            # 测试数据集中数据, 计算输出层输出
            o = self.predict(self.X_test[j])
            predictions.append(np.argmax(o))
        # 计算正确率
        self.accuracy = np.mean((abs(predictions-self.Y_test))/self.Y_test<0.3)
        return self.accuracy

    def predict(self, x):
        # 用测试数据集对当前权值向量进行验证
        # 添加偏置
        temp = np.ones(x.shape[0] + 1)
        temp[0:-1] = x
        x = temp
        # 转换成numpy数组
        x = np.array(x)
        L1 = sigmoid(np.dot(x, self.V))  # 隐藏层
        L2 = sigmoid(np.dot(L1, self.W))  # 输出层
        return L2  # 返回输出层结果

    def train10k(self):
        #训练一万次,检验正确率
        for i in range(10000):
            self.train(1)
        self.test()
        print("已训练%d次,当前准确率:%.4f"%(self.n,self.accuracy))
        # 保存训练结果
        f = open("nnm.mod","bw+")
        pickle.dump(self,f)
        f.close()
        print("训练结果已保存到文件 nnm.mod")





df1 = pd.read_csv("./out/dataset.csv")

npa = df1.to_numpy()
# regular
npa -= npa.min()
npa /= npa.max()

print(npa.shape)
X = npa[:,2:]
Y = npa[:,1]
print(X.shape)
print(X[0,:])

# split train dataset and test dataset
Xi = X[:-1000]
Yi = Y[:-1000]
Xt = X[-1000:]
Yt = Y[-1000:]

nn = NeuralNetwork((16,256,1))
nn.setData(Xi,Yi,Xt,Yt)
for i in range(30):
    nn.train10k()
