from kafka import KafkaConsumer

kserver = ["192.168.80.109:9092","192.168.80.108:9092","192.168.80.107:9092"]
consumer = KafkaConsumer('car3',
                         auto_offset_reset='earliest',
                         bootstrap_servers=kserver)

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
