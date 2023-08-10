from kafka import KafkaProducer
from order_struct import Order
import json

class OrderProducer:
    def __init__(self, frequency):
        self.frequency = frequency
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_order(self, order):
        self.producer.send('order_topic', order.to_json())

    def set_frequency(self, frequency):
        self.frequency = frequency