# 进一步整理数据
import re
import pymysql

rexm = re.compile(r"(\d+)\-(\d+)")
pb = {
    "国三":3,"国四":4,"国五":5,"国六":6
}
turbo = {
    "L":0,"T":1,"THP":1,"TSI":1,"NA":0,"N/A":0
}
motor = {
    "L":1,"H":2,"V":3,"W":4
}
gears = {
    "AT":6,"DCT":5,"CVT":4,"AMT":2,"MT":3,"DSG":5
}


# 2016-03转换成整数
def getMonth(s):
    m = re.match(rexm,s)
    if m:
        g = m.groups()
        y = int(g[0])-1970
        mt = int(g[1])
        return y*12+mt
    return 0


# 定义数据处理函数
def deal(a):
    r = list()
    r.append(a[0])  # 品牌
    r.append(a[1])  # 车型
    r.append(a[2][:-1]) # 年款数值部分
    r.append(float(a[3]))  # 现售价
    r.append(float(a[4]))  # 新车价
    r.append(int(getMonth(a[5])))  # 把年月统一成月份维度的表达
    r.append(float(a[6]))  # 万公里数
    r.append(int(pb.get(a[7],0)))  # 排放标准
    r.append(float(a[8]))  # 排量
    r.append(int(turbo.get(a[9],1)))  # 是否涡轮增压 1是,0否
    r.append(int(a[10]))  # 马力
    r.append(int(motor.get(a[11],0)))  # 发动机结构形式
    r.append(int(a[12]))  # 汽缸数
    r.append(int(a[13]))  # 过户次数
    # 处理日期: 验车,交强险,商业险
    r.append(int(getMonth(a[14])))
    r.append(int(getMonth(a[15])))
    r.append(int(getMonth(a[16])))
    r.append(int(a[17]))  # 档位数
    r.append(int(gears.get(a[18],3)))  # 变速箱类型
    return r

#sql_str = "insert into cars(band,cat,yeart,pricenow,pricenew,regtime,wkms,pb,lit,turbo,hp,stru,cys,regs,ycdate,jqdate,sydate,gears,gt) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
sql_str = "insert into cars(band,cat,yeart,pricenow,pricenew,regtime,wkms,pd,lit,turbo,hp,stru,cys,regs,ycdate,jqdate,sydate,gears,gt) values('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"


conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="08170327",
    database="car"
)
print("连接成功",conn)

cur = conn.cursor()

f = open("./out/data_etl.csv",encoding='utf-8-sig')
#o = open("out/data_num.csv","w")

line = f.readline()
n = 0
while line:
    row = line.split(",")
    r = deal(row)
    n += 1
#    o.write(str(r))
#    o.write("\n")
#    print(len(r),r)
#    print(sql_str%tuple(r))
    if not n%100:
        print(n)
    try:
        cur.execute(sql_str%tuple(r))
    except Exception as e:
        print(n,line)
        print(sql_str%tuple(r))
    line = f.readline()

conn.commit()
cur.close()
conn.close()
#o.close()
f.close()
