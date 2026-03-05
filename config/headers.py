import os
from dotenv import load_dotenv


load_dotenv()
class Headers:
    base = {
        'Authorization': os.getenv("BEARER_TOKEN")
        }