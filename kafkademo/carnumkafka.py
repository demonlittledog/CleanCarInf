from kafka import KafkaProducer
from kafka.errors import KafkaError

kserver = ["192.168.80.109:9092","192.168.80.108:9092","192.168.80.107:9092"]
producer = KafkaProducer(bootstrap_servers=kserver)
i =0
while True:
    mag = "adsada"
    i=i+1
    if i == 100:
        break
    # Asynchronous by default
    future = producer.send('spark4',mag.encode("utf-8"))
    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as ex:
        # Decide what to do if produce request failed...
        print(ex)


    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)
