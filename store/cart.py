from dataclasses import dataclass, field

from customer.models import Customer
from store.models import Item, OrderItem, Order


@dataclass
class Cart:
    item: Item
    created: bool
    order: Order
    quantity: int
    customer: Customer
    order_item: OrderItem

    def add_to_cart(self):
        # if ordered was made
        if not self.created:
            self.order_item.quantity += self.quantity
        else:
            self.order_item.quantity = self.quantity
        self.order_item.save()
        self.order.items.add(self.order_item)

    def remove_from_cart(self):
        self.order_item.delete()

    def update_cart(self):
        self.order_item.quantity = self.quantity
        self.order_item.save()
        self.order.items.add(self.order_item)
