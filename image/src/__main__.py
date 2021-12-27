#!/usr/bin/env python3
import os
import sys
import random
import time
import socket

from kafka import KafkaConsumer, KafkaProducer

def fail(message: str):
    print(message, file = sys.stderr)
    sys.exit(1)

def must_env_var(variable_name: str) -> str:
    value = os.getenv(variable_name)
    if value is None:
        fail(f'Required variable {variable_name} is unset!')
    return value

def consume():
    print('Starting as consumer')
    consumer = KafkaConsumer(bootstrap_servers = must_env_var('BOOTSTRAP_SERVERS'))
    consumer.subscribe(topics = must_env_var('TOPIC_NAME'))
    for message in consumer:
        decoded_message = message.value.decode('utf-8')
        print(f'Received: {decoded_message}')

def produce():
    identity = socket.gethostname()
    print(f'Starting as producer with identity {identity}')
    producer = KafkaProducer(bootstrap_servers = must_env_var('BOOTSTRAP_SERVERS'))
    topic = must_env_var('TOPIC_NAME')
    while True:
        n = random.randint(10, 100)
        message = str(n) + ' from ' + identity
        send_result = producer.send(topic, message.encode('utf-8'))
        send_result = send_result.get(timeout = 10.0)
        print(f'Produced {n}')
        time.sleep(1.0 + random.random())

def main():
    role = must_env_var('SAMPLE_ROLE')
    match role.upper():
        case 'CONSUMER':
            consume()
        case 'PRODUCER':
            produce()
        case other:
            print(f'Role {other} is not consumer / producer')

if __name__ == '__main__':
    main()
