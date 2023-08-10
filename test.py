import random, uuid
from datetime import datetime, timedelta 
from order_struct import Order

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


if __name__ == "__main__":
    orders = create_orders()
    for order in orders[:10]:
        print(order)
    print(f"Total number of orders: {len(orders)}")