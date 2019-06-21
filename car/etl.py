# 整理多个数据文件,输出到 data.csv


# 获取制定目录文件列表
def getFiles(rootdir):
    import os
    k = os.walk(rootdir)
    rs = list()
    for _ in k:
        r, p, f = _
        for _i in f:
            rs.append("%s%s"%(rootdir,_i))
    return rs

# 文件名列表
fs = getFiles("./data/")
print(fs)

# 建立数据文件data.csv
with open("./out/data.csv","w",encoding='utf-8-sig') as dfl:
    # 遍历所有数据文件
    for f in fs:
        with open(f,encoding='utf-8-sig') as fl:
            # 读取数据文件内容,写入到data.csv
            print(fl.name)
            line = "\n%s"%fl.readline()
            while line:
                print(line)
                dfl.write(line)
                line = fl.readline()
