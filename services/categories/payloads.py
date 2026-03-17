from faker import Faker
import random
faker = Faker()

class Payloads:

    def create_category(self, name: str = None):
        return {
            "description": faker.text(),
            "name": name if name is not None else faker.word()
        }