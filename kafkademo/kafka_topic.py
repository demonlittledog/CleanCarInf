from kafka.client import KafkaClient
from kafka.protocol import admin


kserver = ["192.168.80.109:9092","192.168.80.108:9092","192.168.80.107:9092"]
client = KafkaClient(bootstrap_servers=kserver)
topic = "spark"
num_partitions = 3
timeout_ms = 10000
configs = {}
if topic not in client.cluster.topics(exclude_internal_topics=True):  # Topic不存在

    request = admin.CreateTopicsRequest_v0(
        create_topic_requests=[(
            topic,
            num_partitions,
            -1,  # replication unset.
            [],  # Partition assignment.
           [(key, value) for key, value in configs.items()],  # Configs
        )],
        timeout=timeout_ms
    )

    future = client.send(2, request)  # 2是Controller,发送给其他Node都创建失败。
    client.poll(timeout_ms=timeout_ms, future=future)  # 这里

    result = future.value
    # error_code = result.topic_error_codes[0][1]
    print("CREATE TOPIC RESPONSE: ", result)  # 0 success, 41 NOT_CONTROLLER, 36 ALREADY_EXISTS
    client.close()
else:  # Topic已经存在
    print("Topic already exists!")
