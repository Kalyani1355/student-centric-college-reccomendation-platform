from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(
        uri,
        tls=True,
        serverSelectionTimeoutMS=10000
    )

    print(client.admin.command("ping"))
    print("MongoDB Connected Successfully!")

except Exception as e:
    print("MongoDB Connection Error:")
    print(e)