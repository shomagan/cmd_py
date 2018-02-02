#!/usr/bin/env python
import pika
import time

credentials = pika.PlainCredentials('vart', 'vurt')
parameters = pika.ConnectionParameters('192.168.2.95',5672, '/', credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
for i in range(100):
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
    time.sleep(0.02)

print(" [x] Sent 'Hello World!'")
connection.close()
