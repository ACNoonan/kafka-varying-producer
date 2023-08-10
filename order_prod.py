from kafka import KafkaProducer
from order_struct import Order
import json

class OrderProducer:
    def __init__(self, frequency, order):
        self.frequency = frequency
        self.order = order
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce_order(self):
        self.producer.send('order_topic', self.order.to_json())

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_order(self, order):
        self.order = order

