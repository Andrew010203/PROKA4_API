from faker import Faker
import random
faker = Faker()

class Payloads:

    def create_pet(self):
        return {
          "id": random.randint(1, 100),
          "category": {
            "id": random.randint(1, 100),
            "name": faker.file_name()
          },
          "name": faker.name(),
          "photoUrls": [
            faker.url()
          ],
          "tags": [
            {
              "id": random.randint(1, 100),
              "name": faker.user_name()
            }
          ],
          "status": "available"
        }