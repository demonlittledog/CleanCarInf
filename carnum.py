import socket
from threading import Thread
import time
import random

'''京A-D12345
京N-3XX79
冀J-A3K28

"黑吉辽京津冀晋蒙鲁苏浙沪鄂豫皖湘
云贵川陕甘宁青新藏琼渝赣粤桂闽"
'''

# 随机生成一系列车牌号
import random as rnd

def choiceByWeight(arr,w):
    '''按权重随机选取列表中元素
    arr 为列表，w为权重
    '''
    s = sum(w)  # 权重数组求和
    n = rnd.randint(0,s)  # 随机数
    #print("rnd = ",n,"/",s)
    l = len(provw)  # 个数
    for i in range(l):  # 判断区间
        sa = sum(w[:i])
        sb = sum(w[:i+1])
        if n >= sa and n <sb:  # 输出随机数对应区间的元素
            return arr[i]


# 省份简称列表
provs = "黑吉辽京津冀晋蒙鲁苏浙沪鄂豫皖湘云贵川陕甘宁青新藏琼渝赣粤桂闽"
# 各省权重列表
provw = [500,300,600,30000,2000,4000,1000,1500,500,100,100,100,
         200,400,200,100,50,50,50,50,50,50,50,10,10,10,100,100,200,100,500]
# 字母列表
letters = "ABCDEFGHJKLMNPQRST"
# 数字列表
numbers = "0123456789"

# 远程socket
remote = None

# 保存所有客户端
clients = list()

# 生成1个车牌
def getCarNum():
    p = choiceByWeight(provs,provw)  # 省份
    c = rnd.choice(letters)  # 城市字母

    a1= rnd.choice(numbers)
    a2= rnd.choice(letters)
    a3= rnd.choice(numbers)
    a4= rnd.choice(letters)
    a5= rnd.choice(numbers)

    a ="".join([a1,a2,a3,a4,a5])  # 车牌数字和字母的组合
    cn = "%s%s-%s"%(p,c,a)  # 拼合车牌
    return cn


# 线程执行体函数
def trun():
    while True:
        # 获取车牌
        timegap = random.randrange(1,5)
        time.sleep(timegap/10)
        cn = getCarNum()
        print("已拍摄车牌：", cn)
        msg = "camera02:" + cn + "\t\n"

        global remote
        # 发送给指定的客户端
        try:
            if remote:
                remote.sendall(msg.encode("utf-8"))
            else:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect(("192.168.80.108", 7777))
        except Exception as ex:
            remote = None

        # 广播给各连接的客户端
        for c in clients:
            try:
                c.sendall(msg.encode("utf-8"))
            except Exception as ex:
                clients.remove(c)
        print("已广播")


# 创建服务socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9999))
server.listen()
print("服务器已启动")

# 启动服务线程，用于广播车牌消息
task = Thread(target=trun)
task.setDaemon(True)
task.start()


print("等待客户端连接")
# 接受传入连接
while True:
    client, addr = server.accept()
    print(addr," 已连接到服务器")
    clients.append(client)