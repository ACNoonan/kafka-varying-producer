from flask import Flask, request, jsonify
from order_prod import OrderProducer
from order_struct import Order
import threading
import time
import uuid
import random
from datetime import datetime, timedelta


# Create Order objects and Produce to Kafka
# (self, id, user_id, total, status, address_id, payment_id, created_at, modified_at)
def create_orders():
    orders = []
    rand_iterations = random.randint(1, 100)
    for i in range(1, rand_iterations):
        # Create random total
        random_number = random.uniform(10, 100)
        random_total = round(random_number, 2)
        #Set order status
        statuses = ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "DENIED"]
        random_selector = random.randint(0, 4)
        status = statuses[random_selector]
        # Generate random created_at datetime within the last week
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=1)
        create_date = start_date + (end_date - start_date) * random.random()
        #Generate random modified_at date with 80% of null, 20% chance of being within the last week
        modified_chance = random.random()
        if modified_chance < 0.8:
            modified_date = 'NULL'
        else:
            modified_date = create_date + timedelta(days=random.uniform(1, 7))

        order = Order(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            total=random_total,
            status=status,
            address_id=uuid.uuid4(),
            payment_id=uuid.uuid4(),
            created_at=create_date,
            modified_at=modified_date
        )
        orders.append(order)
    return orders

orders = create_orders()
for order in orders:
    print(f"Producing order: {order}")
    producer = OrderProducer(1, order)

def produce_orders():
    while True:
        time.sleep(1 / producer.frequency)
        producer.produce_order()


# Flask app 
app = Flask(__name__)
@app.route('/set_frequency', methods=['POST'])
def set_frequency():
    try:
        frequency = request.json['frequency']
        if frequency <= 0:
            raise ValueError("Frequency must be greater than 0")
        producer.set_frequency(frequency)
        return jsonify({"message": f"Frequency set to {frequency}"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/set_order', methods=['POST'])
def set_order():
    order_data = request.json['order']
    order = Order(order_data['id'], order_data['product'], order_data['quantity'], order_data['price'])
    producer.set_order(order)
    return "Order set"

if __name__ == '__main__':
    t = threading.Thread(target=produce_orders)
    t.start()
    app.run(host="0.0.0.0", port=5000)
