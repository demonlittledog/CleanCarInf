import re
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
#预编译正则表达式，提取数据：省，市，维度，经度
p = re.compile(r"(\w+)\s(\w+)\s北纬(\d+\.?\d+)\s东经(\d+\.?\d+)")
#保存读取的数据
x = []
#读取文件
f = open("cities.txt",encoding="utf-8")
# 逐行读取
l = f.readline()
while l:
    # 正则查找
    m = re.search(p, l)
    if m:
        # 找到则添加到数据列表
        x.append(m.groups())
    else:
        print(l)
    # print(m.groups())
    l = f.readline()
f.close()

# 转换城numpy矩阵
nx = np.array(x)
#print(nx)

# 只获取经纬度数值用于聚类分析
X = np.array(nx[:, -2:],dtype=float)
# print(X)

#以上是城市地理坐标，以下是模拟点数据
X = np.array([
    [1,1],[2,1],[1,2],[0,0],
    [15,16],[16,15],[18,17],[19,17],
    [105,22],[99,21],[97,23],[89,15],
    [35,98],[32,100],[41,133],[29,79],
])
x = X[:,0].reshape((16,))
y = X[:,1].reshape((16,))

for k in range(3,4):
    # K-Means聚类
    # 设定聚类数目 k
    #k = 3
    # 创建聚类对象
    kmo = KMeans(k)
    # 调用对象fit传递被聚类数据，得到聚类结果
    clusters = kmo.fit(X)

    # 查看聚类结果标签
    # print(clusters.labels_)

    # n = len(x)
    # for i in range(n):
    #     print(nx[i],clusters.labels_[i])

    #计算轮廓系数
    score = silhouette_score(
    X,#被聚类的数据
    clusters.labels_,#聚类标签
    metric='euclidean'#欧几里得数据
    )

    print("k:",k,"轮廓系数",score)

colors = ["b.","g.","r."]

for i in range(16):
    plt.plot(x[i],y[i],colors[clusters.labels_[i]])
plt.show()