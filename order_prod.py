from kafka import KafkaProducer
from order_struct import Order
import json
import os

LENSES_API_URL = os.getenv('LENSES_API_URL')
LENSES_API_KEY = os.getenv('LENSES_API_KEY')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')


class OrderProducer:
    def __init__(self, frequency):
        self.frequency = frequency
        self.producer = KafkaProducer(
            bootstrap_servers=f'{KAFKA_BOOTSTRAP_SERVERS}:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_order(self, order):
        self.producer.send('order_topic', order.to_json())

    def set_frequency(self, frequency):
        self.frequency = frequency