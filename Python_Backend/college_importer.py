import os
import re
import certifi
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient


# =========================================================
# CONFIG
# =========================================================

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")


SPPU_URL = (
    "https://bcud.unipune.ac.in/"
    "utilities/college_search/All_Colleges.aspx"
)


# =========================================================
# MONGODB
# =========================================================

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=15000,
    connectTimeoutMS=20000,
    socketTimeoutMS=20000,
)

db = client["edufinder"]
colleges_collection = db["colleges"]


# =========================================================
# REQUEST SESSION
# =========================================================

session = requests.Session()

session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/153.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
)


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(value):
    if value is None:
        return ""

    value = str(value)

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# =========================================================
# CLEAN WEBSITE
# =========================================================

def clean_website(value):

    value = clean_text(value)

    if not value:
        return ""

    if value in ["-", "---", "NA", "N/A", "Details"]:
        return ""

    value = value.replace(" ", "")

    if value.startswith(
        ("javascript:", "#", "mailto:")
    ):
        return ""

    if value.startswith("http://"):
        return value

    if value.startswith("https://"):
        return value

    if value.startswith("www."):
        return "https://" + value

    if "." in value:
        return "https://" + value

    return ""


# =========================================================
# NORMALIZE CITY
# =========================================================

def normalize_city(district, taluka):

    district = clean_text(district)
    taluka = clean_text(taluka)

    district_upper = district.upper()
    taluka_upper = taluka.upper()

    # Pune
    if "PUNE" in district_upper:
        return "Pune"

    # Nashik
    if "NASHIK" in district_upper:
        return "Nashik"

    # Ahilyanagar / Ahmednagar
    if (
        "AHILYANAGAR" in district_upper
        or "AHMEDNAGAR" in district_upper
    ):
        return "Ahilyanagar"

    # Mumbai
    if "MUMBAI" in district_upper:
        return "Mumbai"

    # Nagpur
    if "NAGPUR" in district_upper:
        return "Nagpur"

    # Thane
    if "THANE" in district_upper:
        return "Thane"

    # Use taluka as fallback
    if taluka:
        taluka = re.sub(
            r"\(.*?\)",
            "",
            taluka
        ).strip()

        return taluka.title()

    return district.title()


# =========================================================
# FETCH SPPU
# =========================================================

def fetch_sppu_page():

    print("\n========================================")
    print("FETCHING SPPU OFFICIAL COLLEGE DIRECTORY")
    print("========================================")

    response = session.get(
        SPPU_URL,
        timeout=40
    )

    print(
        "HTTP STATUS:",
        response.status_code
    )

    response.raise_for_status()

    print(
        "HTML LENGTH:",
        len(response.text)
    )

    return response.text


# =========================================================
# EXTRACT WEBSITE FROM ROW
# =========================================================

def extract_website(row, cells):

    # First try links from the row
    links = row.find_all(
        "a",
        href=True
    )

    for link in links:

        href = clean_text(
            link.get("href", "")
        )

        # Ignore Details links pointing to same site
        if (
            href
            and "bcud.unipune.ac.in" not in href.lower()
            and not href.lower().startswith(
                "javascript:"
            )
        ):
            website = clean_website(href)

            if website:
                return website

    # Try text in final cells
    for cell in reversed(cells):

        value = clean_text(
            cell.get_text(
                " ",
                strip=True
            )
        )

        website = clean_website(value)

        if website:
            return website

    return ""


# =========================================================
# PARSE SPPU COLLEGE ROWS
# =========================================================

def parse_colleges(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    rows = soup.find_all("tr")

    print(
        "TOTAL ROWS FOUND:",
        len(rows)
    )

    colleges = []

    for row in rows:

        cells = row.find_all(
            ["td", "th"]
        )

        if len(cells) < 9:
            continue

        values = []

        for cell in cells:

            values.append(
                clean_text(
                    cell.get_text(
                        " ",
                        strip=True
                    )
                )
            )

        row_text = " ".join(
            values
        ).lower()

        # We only import actual colleges / institutes
        if (
            "affiliated college" not in row_text
            and "recognised institute" not in row_text
        ):
            continue

        # -------------------------------------------------
        # SPPU columns
        #
        # 0 Puncode
        # 1 College
        # 2 College_Type
        # 3 Telephone
        # 4 Email
        # 5 Running_Faculties
        # 6 District
        # 7 Taluka
        # 8 Establishment_Year
        # 9 Website_link
        # -------------------------------------------------

        puncode = (
            values[0]
            if len(values) > 0
            else ""
        )

        name = (
            values[1]
            if len(values) > 1
            else ""
        )

        college_type = (
            values[2]
            if len(values) > 2
            else ""
        )

        district = (
            values[6]
            if len(values) > 6
            else ""
        )

        taluka = (
            values[7]
            if len(values) > 7
            else ""
        )

        establishment_year = (
            values[8]
            if len(values) > 8
            else ""
        )

        if not name:
            continue

        # Remove strange trailing "Details"
        name = re.sub(
            r"\s+Details$",
            "",
            name,
            flags=re.IGNORECASE
        ).strip()

        website = extract_website(
            row,
            cells
        )

        city = normalize_city(
            district,
            taluka
        )

        college = {
            "puncode": puncode,
            "name": name,
            "university": (
                "Savitribai Phule Pune University"
            ),
            "city": city,
            "district": district,
            "taluka": taluka,
            "collegeType": college_type,
            "establishmentYear": (
                establishment_year
            ),
            "website": website,
        }

        colleges.append(
            college
        )

    # Remove duplicates
    unique = {}

    for college in colleges:

        key = (
            college.get("puncode")
            or (
                college.get("name"),
                college.get("city")
            )
        )

        unique[key] = college

    colleges = list(
        unique.values()
    )

    print(
        "PARSED COLLEGES:",
        len(colleges)
    )

    return colleges


# =========================================================
# SAVE COLLEGES
# =========================================================

def save_colleges(colleges):

    inserted = 0
    updated = 0

    print("\n========================================")
    print("SAVING COLLEGES TO MONGODB")
    print("========================================")

    for college in colleges:

        puncode = college.get(
            "puncode",
            ""
        )

        name = college.get(
            "name",
            ""
        )

        city = college.get(
            "city",
            ""
        )

        if puncode:

            filter_query = {
                "puncode": puncode
            }

        else:

            filter_query = {
                "name": name,
                "city": city
            }

        result = colleges_collection.update_one(
            filter_query,
            {
                "$set": {
                    "puncode": puncode,
                    "name": name,
                    "university": college.get(
                        "university",
                        ""
                    ),
                    "city": city,
                    "district": college.get(
                        "district",
                        ""
                    ),
                    "taluka": college.get(
                        "taluka",
                        ""
                    ),
                    "collegeType": college.get(
                        "collegeType",
                        ""
                    ),
                    "establishmentYear": college.get(
                        "establishmentYear",
                        ""
                    ),
                    "website": college.get(
                        "website",
                        ""
                    ),
                },

                # Do NOT overwrite detected courses
                "$setOnInsert": {
                    "courses": [],
                    "image": ""
                }
            },
            upsert=True
        )

        if result.upserted_id:
            inserted += 1
        else:
            updated += 1

    print(
        "NEW COLLEGES:",
        inserted
    )

    print(
        "UPDATED COLLEGES:",
        updated
    )

    return {
        "inserted": inserted,
        "updated": updated
    }


# =========================================================
# MAIN IMPORT
# =========================================================

def import_sppu_colleges():

    try:

        html = fetch_sppu_page()

        colleges = parse_colleges(
            html
        )

        if not colleges:

            return {
                "status": "error",
                "message": (
                    "No colleges could be parsed "
                    "from the SPPU directory."
                )
            }

        result = save_colleges(
            colleges
        )

        return {
            "status": "success",
            "source": SPPU_URL,
            "total_parsed": len(colleges),
            **result
        }

    except Exception as error:

        print(
            "IMPORT ERROR:",
            error
        )

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    result = import_sppu_colleges()

    print("\n========================================")
    print("FINAL IMPORT RESULT")
    print("========================================")

    print(result)