from pymongo import MongoClient
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import certifi
import os
from urllib.parse import urljoin

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

OUTPUT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend",
        "public",
        "college-images"
    )
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/139.0 Safari/537.36"
    )
}


# Pages where campus/gallery images are commonly available
PAGE_KEYWORDS = [
    "gallery",
    "campus",
    "campus-life",
    "facilities",
    "infrastructure",
    "about"
]


def get_page(url):

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            verify=certifi.where()
        )

        if response.status_code != 200:
            return None

        return response.text

    except Exception:
        return None


def find_pages(website):

    pages = [website]

    for keyword in PAGE_KEYWORDS:

        if website.endswith("/"):
            page = website + keyword + "/"
        else:
            page = website + "/" + keyword + "/"

        pages.append(page)

    return pages


def find_good_image(page_url, html):

    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img")

    candidates = []

    for img in images:

        src = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-lazy-src")
            or img.get("data-original")
        )

        if not src:
            continue

        src_lower = src.lower()

        # Skip unwanted images
        bad_words = [
            "favicon",
            "facebook",
            "instagram",
            "twitter",
            "linkedin",
            "icon",
            "arrow",
            "sprite",
            "loading",
            "loader",
            "avatar",
            "logo"
        ]

        if any(word in src_lower for word in bad_words):
            continue

        image_url = urljoin(page_url, src)

        # Prefer images whose filename suggests campus/infrastructure
        score = 0

        good_words = [
            "campus",
            "building",
            "college",
            "infrastructure",
            "facility",
            "main",
            "banner",
            "gallery"
        ]

        for word in good_words:

            if word in src_lower:
                score += 10

        # Alt text can also help
        alt = img.get("alt", "").lower()

        for word in good_words:

            if word in alt:
                score += 5

        candidates.append(
            (score, image_url)
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return candidates[0][1]


def download_image(image_url, college_id):

    try:

        response = requests.get(
            image_url,
            headers=HEADERS,
            timeout=30,
            stream=True,
            verify=certifi.where()
        )

        if response.status_code != 200:
            return None

        content_type = response.headers.get(
            "content-type",
            ""
        ).split(";")[0].lower()

        if not content_type.startswith("image/"):
            return None

        extensions = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif"
        }

        extension = extensions.get(
            content_type,
            ".jpg"
        )

        filename = f"{college_id}{extension}"

        filepath = os.path.join(
            OUTPUT_DIR,
            filename
        )

        with open(filepath, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=8192
            ):

                if chunk:
                    file.write(chunk)

        return f"/college-images/{filename}"

    except Exception:
        return None


# Only colleges which don't have an image
query = {
    "$or": [
        {"image": ""},
        {"image": None},
        {"image": {"$exists": False}}
    ]
}

college_list = list(
    colleges.find(query)
)

print()
print("=" * 65)
print(f"Found {len(college_list)} colleges without images")
print("=" * 65)

success = 0
failed = 0


for college in college_list:

    name = college.get(
        "name",
        "Unknown"
    )

    website = college.get(
        "website",
        ""
    )

    college_id = str(
        college["_id"]
    )

    print()
    print("-" * 65)
    print(name)
    print("-" * 65)

    if not website:
        print("No website")
        failed += 1
        continue

    if not website.startswith("http"):
        website = "https://" + website

    image_found = False

    pages = find_pages(website)

    for page in pages:

        print(
            f"Checking: {page}"
        )

        html = get_page(page)

        if not html:
            continue

        image_url = find_good_image(
            page,
            html
        )

        if not image_url:
            continue

        print(
            f"Image found: {image_url}"
        )

        local_path = download_image(
            image_url,
            college_id
        )

        if local_path:

            colleges.update_one(
                {"_id": college["_id"]},
                {
                    "$set": {
                        "image": local_path
                    }
                }
            )

            print(
                f"SUCCESS: {local_path}"
            )

            success += 1
            image_found = True
            break

    if not image_found:

        print(
            "FAILED: No suitable campus image found"
        )

        failed += 1


print()
print("=" * 65)
print("FINAL RESULT")
print("=" * 65)

print(
    f"Successful: {success}"
)

print(
    f"Failed:     {failed}"
)

print(
    f"Total:      {len(college_list)}"
)

print("=" * 65)