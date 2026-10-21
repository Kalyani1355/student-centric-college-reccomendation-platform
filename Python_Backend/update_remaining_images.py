from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=15000,
    connectTimeoutMS=20000,
    socketTimeoutMS=20000,
    directConnection=False
)

db = client["edufinder"]
colleges = db["colleges"]

image_folder = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend",
        "public",
        "college-images"
    )
)

college_images = {
    "Sinhgad College of Engineering": "sinhgad.jpg",
    "MKSSS's Cummins College of Engineering for Women": "cummins.jpg",
    "Bharati Vidyapeeth College of Engineering": "bharati.jpg",
    "Abasaheb Garware College": "garware.jpg",
    "Parvatibai Genba Moze College of Engineering": "pgmcoe.jpg",
    "Genba Sopanrao Moze College of Engineering": "gsmcoe.jpg"
}

print("\nUpdating college images...\n")

success = 0
failed = 0

for college_name, filename in college_images.items():

    file_path = os.path.join(
        image_folder,
        filename
    )

    print(f"College: {college_name}")
    print(f"Image:   {filename}")

    if not os.path.exists(file_path):
        print("❌ Image file not found\n")
        failed += 1
        continue

    result = colleges.update_one(
        {"name": college_name},
        {
            "$set": {
                "image": f"/college-images/{filename}"
            }
        }
    )

    if result.matched_count == 0:
        print("❌ College not found in MongoDB\n")
        failed += 1

    elif result.modified_count > 0:
        print("✅ MongoDB image updated\n")
        success += 1

    else:
        print("⚠️ Already updated\n")
        success += 1


print("=" * 55)
print("IMAGE UPDATE COMPLETED")
print("=" * 55)
print(f"Successful: {success}")
print(f"Failed:     {failed}")
print("=" * 55)