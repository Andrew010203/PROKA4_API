from faker import Faker
import random
faker = Faker()

class Payloads:

    def create_product(self):
        return {
          "category": faker.company(),
          "description": faker.domain_word(),
          "image_url": faker.email(),
          "name": faker.domain_word(),
          "price": random.randint(1, 10000),
          "rating": random.uniform(1.0, 10.0),
          "reviews_count": random.randint(1, 100),
          "stock": random.randint(1, 100)
        }


    def update_product(self):
        return {
            "price": random.uniform(1.0, 100000.0),
            "stock": random.randint(1, 100)
        }