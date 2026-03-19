from faker import Faker
import random
faker = Faker()

class Payloads:

    def add_product(self, product_id=None, quantity=None):
        return {
            "product_id": product_id or random.randint(1, 10),
            "quantity": quantity or random.randint(1, 5)
        }


    def update_cart(self, quantity=None):
        return {
            "quantity": quantity if quantity is not None else random.randint(1, 10)
        }