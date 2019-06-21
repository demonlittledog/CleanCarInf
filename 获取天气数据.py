import datetime
import time

from bs4 import BeautifulSoup
import urllib.request as req
from kafka import KafkaProducer
from kafka.errors import KafkaError

kserver = ["192.168.80.109:9092","192.168.80.108:9092","192.168.80.107:9092"]
#作为kafka生产者
producer = KafkaProducer(bootstrap_servers=kserver)
def getTempList(date:str):
    url = "http://www.tianqishi.com/beijing/%s.html"%date
    rsp = req.urlopen(url)
    html = rsp.read().decode("UTF-8")
    #当前页面的内核
    bs = BeautifulSoup(html,"lxml")
    tmrs = list()
    try:
        t = bs.select("table.yuBaoTable")
        trs = t[0].select("tr")
    except Exception as e:
        trs = []
    for _ in trs:
        tds = _.select("td")
        time.sleep(1)
        yield (tds[0].text,tds[1].text[:-1])


#print(getTempList("20190515"))

dt = datetime.date(2018,5,10)
print(dt)
day1 = datetime.timedelta(days=1)
for i in range(90):
    date_str ="%4d%02d%02d"%(dt.year,dt.month,dt.day)
    temps = getTempList(date_str)
    for _ in temps:
        print(_)
        future = producer.send('weather',_[1].encode("utf-8"),_[0].encode("utf-8"))
    dt += day1





