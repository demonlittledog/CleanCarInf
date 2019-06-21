from kafka import KafkaConsumer
# 使用group,对于同一个group的成员只有一个消费者实例可以读取数据
kserver = ["192.168.80.109:9092","192.168.80.108:9092","192.168.80.107:9092"]
consumer = KafkaConsumer('car3',auto_offset_reset='earliest',bootstrap_servers=kserver)
for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value.decode("utf-8")))
