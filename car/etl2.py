import re
# 分离品牌车型中包含字母和数字的部分
rexp = re.compile(r"^([\u4e00-\u9fa5]+)([0-9a-zA-Z\-\s]+\S+)\s")
# 分离品牌车型中包含字母和数字的部分
rexp1 = re.compile(r"^([\u4e00-\u9fa5]+)([0-9a-zA-Z]+)")
# 提取年款信息
rexpyr = re.compile(r"\s(\d+\款)\s")
# 提取数字
redg = re.compile(r"\d+.\d+|\d+")
# 发动机类型
remt = re.compile(r"(\d.\d)(\w+)\s(\d+)\w+\s(\w)(\d+)")
# 变速箱类型
regb = re.compile(r"(\d)\w+\((\S+)\)")


def getCarInfo(cells):
    if len(cells)!=15:return None

    # 解析车型信息,获取 品牌,车型,年款
    band = None
    carcat = None
    yrst = None

    bandtype = cells[0]
    bts = bandtype.split(" ")
    if len(bts)<3:  # 不足3个字段为无效数据
        return None

    if bts[2].endswith("款"):  # 规范数据,第三字段为年款,依次获取
        band = bts[0]
        carcat = bts[1]
        yrst = bts[2]
    elif bts[1].endswith("款"):
        band = bts[0]
        carcat = bts[2]
        yrst = bts[1]
    else:
        # 不规范数据
        # 提取年款
        h = re.findall(rexpyr,bandtype)
        if h:
            yrst = h[0]
            band = bts[0]

        # 尝试分离品牌车型
        g = re.match(rexp,bandtype)
        if g:
            band = g.groups()[0]
            carcat = g.groups()[1]
            # 去掉车型中的年款信息
            if carcat.endswith("款"):
                carcat = carcat[:-6]

    if band:
        # 中英文分离
        g = re.match(rexp1, band)
        if g:
            band = g.groups()[0]
            carcat = "%s %s"%(g.groups()[1], carcat)

    suc = band and carcat and yrst
    if not suc:
        return None

    try:
        saleprice = re.findall(redg,cells[2])[0]
        newprice = re.findall(redg,cells[3])[0]
        cardate = cells[4]
        km = re.findall(redg,cells[5])[0]
        pb = cells[6]
        liters = re.findall(redg,cells[7])[0]
        ownchs = cells[8][:1]
        rundate = cells[9]
        jqxdate = cells[10]
        syxdate = cells[11]
        drivetype = cells[12]
        drivetype = re.match(remt,drivetype)
        drivetype = drivetype.groups()
        turbo = drivetype[1]
        hp = drivetype[2]
        stru = drivetype[3]
        cylinders = drivetype[4]
        gearbox = cells[13]
        if gearbox.startswith("无级变速"):
            gearbox = "1%s"%gearbox
        gm = re.match(regb, gearbox).groups()
        gears = gm[0]
        geartype = gm[1]
        row = (band,carcat,yrst,saleprice,newprice,cardate,km,pb,liters,turbo,hp,stru,cylinders,ownchs,rundate,jqxdate,syxdate,gears,geartype)
        return row
    except Exception as e:
        return None


f = open("./out/data.csv",encoding='utf-8-sig')
o = open("./out/data_etl.csv","w",encoding='utf-8-sig')
head = f.readline()
print(head)
line = f.readline()

while line:
    if line != head:
        cells = line.split(",")
        r = getCarInfo(cells)
        if r:
            pass
            print(r)
            o.write(",".join(r))
            o.write("\n")
        else:
            pass
#            print(len(cells),line)
    line = f.readline()
o.close()
f.close()


