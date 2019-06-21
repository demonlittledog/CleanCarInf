from kafka import KafkaProducer
from kafka.errors import KafkaError

kserver = ["bd01:9092","bd02:9092","bd03:9092"]
kprd = KafkaProducer(bootstrap_servers=kserver)

producer = KafkaProducer(bootstrap_servers=kserver)

# Asynchronous by default
n = 1
while n<1000:
    n +=1
    future = producer.send('spark2',
                           key=b"%d"%n,
                           value="msg".encode("utf-8"))

    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as ex:
        # Decide what to do if produce request failed...
        print(ex)

    # Successful result returns assigned partition and offset
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# # produce keyed messages to enable hashed partitioning
# producer.send('my-topic', key=b'foo', value=b'bar')
#
# # encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps)
# producer.send('msgpack-topic', {'key': 'value'})
#
# # produce json messages
# producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
# producer.send('json-topic', {'key': 'value'})
#
# # produce asynchronously
# for _ in range(100):
#     producer.send('my-topic', b'msg')

# def on_send_success(record_metadata):
#     print(record_metadata.topic)
#     print(record_metadata.partition)
#     print(record_metadata.offset)
#
# def on_send_error(excp):
#     log.error('I am an errback', exc_info=excp)
#     # handle exception
#
# # produce asynchronously with callbacks
# producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)
#
# # block until all async messages are sent
# producer.flush()
#
# # configure multiple retries
# producer = KafkaProducer(retries=5)