import pika

import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters("172.16.5.63"))

channel = connection.channel()

result = channel.queue_declare(queue="Samples.RabbitMQ.NativeIntegration.Sender")

channel.basic_publish(exchange='',
                      routing_key="Samples.RabbitMQ.NativeIntegration",
                      properties=pika.BasicProperties(message_id=str(uuid.uuid1())),
                      body='<aa>1</aa>')
connection.close()

print("[x] send success!")
