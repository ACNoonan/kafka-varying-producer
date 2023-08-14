class Order:
    def __init__(self, id, user_id, total, status, address_id, payment_id, items, created_at, modified_at):
        self.id = id
        self.user_id = user_id
        self.total = total
        self.status = status
        self.address_id = address_id
        self.payment_id = payment_id
        self.items = items
        self.created_at = created_at
        self.modified_at = modified_at

        
    def __str__(self):
        return (
            f"Order(id={self.id}, user_id={self.user_id}, total={self.total}, "
            f"status={self.status}, address_id={self.address_id}, payment_id={self.payment_id}, items={self.items}, "
            f"created_at={self.created_at}, modified_at={self.modified_at})"
        )

    def to_json(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'total': self.total,
            'status': self.status,
            'address_id': str(self.address_id),
            'payment_id': str(self.payment_id),
            'items': self.items,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at if isinstance(self.modified_at, str) else self.modified_at.isoformat()
        }
