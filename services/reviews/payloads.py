from faker import Faker
import random
faker = Faker()

class Payloads:

    def add_reviews(self, rating=None):
        return {
              "author": faker.name(),
              "comment": faker.text(),
              "rating": rating if rating is not None else random.randint(1, 5)
        }

    def put_review(self, rating=None):
        return {
              "comment": faker.text(),
              "rating": rating if rating is not None else random.randint(1, 5)
        }