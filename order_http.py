from flask import Flask, requests, request, jsonify
from order_prod import OrderProducer
from order_struct import Order
import threading
import time
import uuid
import random
from datetime import datetime, timedelta
import os
import json

LENSES_API_URL = os.getenv('LENSES_API_URL')
LENSES_API_KEY = os.getenv('LENSES_API_KEY')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')

# Optionally, you can handle cases where the variables are not set
if None in [LENSES_API_URL, LENSES_API_KEY, KAFKA_BOOTSTRAP_SERVERS, KAFKA_PASSWORD]:
    print("One or more required environment variables are not set.")
else:
    print("All required environment variables are set.")

# Register Application with Lenses
url = f"http://{LENSES_API_URL}/api/v1/apps/external"

payload = json.dumps({
  "name": "Orders-MicroService",
  "metadata": {
    "version": "1.0",
    "description": "Variable producer for orders event sourcing",
    "owner": "Adam",
    "appType": "stream-generator",
    "tags": [
      "workshop",
      "orders",
      "Adam",
      "Dev",
      "SLA:1"
    ],
    "deployment": "k8s"
  },
  "output": [
    {
      "name": "orders_topic"
    }
  ]
})

headers = {
  'X-Kafka-Lenses-Token': f'{LENSES_API_KEY}',
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)

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
        # Create random items
        items = []
        for item_index in range(random.randint(1, 5)):
            item_id = str(uuid.uuid4())
            quantity = random.randint(1, 10)
            price = round(random.uniform(1, 100), 2)
            items.append({"item_id": item_id, "quantity": quantity, "price": price})
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
            items=items,
            created_at=create_date,
            modified_at=modified_date
        )
        orders.append(order)
    return orders

running = True

producer = OrderProducer(1)

def produce_orders():
    global running
    orders = create_orders()
    while running:
        sleep_time = 1 /producer.frequency
        time.sleep(sleep_time)
        for order in orders:
            print(f"Producing order: {order.total}\nAt frequency: {sleep_time}\n")
            producer.produce_order(order)


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

if __name__ == '__main__':
    try:
        t = threading.Thread(target=produce_orders)
        t.start()
        app.run(host="0.0.0.0", port=5000)
    except:
        print("Sutting down...")
        running = False
        t.join()