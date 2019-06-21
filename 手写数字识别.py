# 图像处理
import cv2
# 矩阵运算
import numpy as np

# sklearn 的安装: pip install scikit-learn
# 机器学习数据集
from sklearn.datasets import load_digits
# 拆分工具
from sklearn.model_selection import train_test_split
# 预处理
from sklearn.preprocessing import LabelBinarizer
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
        self.accuracy = np.mean(np.equal(predictions, self.Y_test))
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


class Paint:
    def __init__(self, w, h, nm):
        # 初始化画布大小
        self.width = w
        self.height = h
        self.nm = nm
        self.img = np.zeros(
            (w, h, 3),
            np.uint8
        )
        self.data = np.zeros(
            (8, 8), np.float64
        )
        # 初始状态为抬笔
        self.draw = False
        # 上一个绘制点
        self.lastPoint = None

    def drawLine(self, e, x, y, flag, param):
        if e == 1:
            # 落笔,记录落笔点
            self.draw = True
            self.lastPoint = (x, y)
        if e == 4:
            # 抬笔
            self.draw = False
        if self.draw and (e == 0):
            # 画线,起点为落笔点,终点为当前点
            cv2.line(
                param["img"],
                self.lastPoint,
                (x, y),
                (255, 255, 190),
                40,
                cv2.LINE_4
            )
            # 划线终点更新为落笔点
            self.lastPoint = (x, y)

    def run(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback(
            'image',
            self.drawLine,
            param={"img": self.img}
        )

        while 1:
            cv2.imshow('image', self.img)
            ch = cv2.waitKey(20)
            if ch == 27:#退出
                break
            if ch == ord('c'):#识别
                step = 40
                ii = 0
                for i in range(0, self.height, step):
                    ij = 0
                    for j in range(0, self.width, step):
                        s = self.img[i:i + step, j:j + step]
                        v = np.mean(s.reshape(4800))
                        self.data[ii][ij] = v
                        ij += 1
                    ii += 1
                #print(self.data)

                # 数据归一化
                rdata = self.data
                rdata = rdata.reshape(64)
                rdata -= rdata.min()
                rdata /= rdata.max()
                # 获取识别结果
                otest = self.nm.predict(rdata)
                n = np.argmax(otest)
                print("识别结果:",n)
            if ch == ord('q'):#清空
                self.img = np.zeros((self.width, self.height, 3), np.uint8)
                cv2.imshow('image', self.img)
                cv2.setMouseCallback('image', self.drawLine, param={"img": self.img})
            if ch == ord('t'):#训练
                self.nm.train10k()
            if ch == ord('r'):#重建
                self.nm = NeuralNetwork([64,256,10])#创建网络
                self.nm.setData(Xa,Ya,Xb,Yb)
                print("模型已重建")
                self.nm.train10k()
        self.stop()

    def stop(self):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # 载入数据(手写体数字,8*8点阵图像信息)
    digits = load_digits()
    X = digits.data  # 数据
    Y = digits.target  # 标签

    # 对数据集进行分割, 得到训练数据和测试数据
    Xa, Xb, Ya, Yb = train_test_split(X, Y)
    # 数据归一化(0~1)
    Xa -= Xa.min()
    Xa /= Xa.max()
    # 训练标签二值化
    Ya = LabelBinarizer().fit_transform(Ya)

    exm = False
    # 载入训练模型,如果没有,则进行训练并保存模型
    try:
        f = open("nnm.mod","br")
        nm = pickle.load(f)
        f.close()
        exm = True
        print("训练模型已加载,当前准确率:",nm.accuracy)
    except FileNotFoundError as e:
        print("训练模型不存在\n自动训练至正确率70%以上")
        nm = NeuralNetwork([64,256,10])#创建网络
        nm.setData(Xa,Ya,Xb,Yb)


    # 开始训练
    while nm.accuracy< 0.7:
        print("正确率不达标,重新训练")
        nm.train10k()
        print('训练完毕')
    else:
        print("开始识别,请在窗口手写数字,按C识别"
              "\nQ清空,T训练,R重建,ESC退出")
        a = Paint(320, 320, nm)
        a.run()
