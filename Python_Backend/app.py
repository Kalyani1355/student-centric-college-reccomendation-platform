import os
import re
import certifi

from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv

from course_scraper import scrape_courses_detailed
from college_importer import import_sppu_colleges


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError(
        "MONGO_URI not found in .env file"
    )


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="EduFinder API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    directConnection=False
)

db = client["edufinder"]

colleges_collection = db["colleges"]


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "EduFinder Python Backend is running"
    }


# =========================================================
# STATUS
# =========================================================

@app.get("/api/status")
def api_status():

    try:

        college_count = (
            colleges_collection.count_documents({})
        )

        return {
            "status": "success",
            "backend": "running",
            "mongodb": "connected",
            "college_count": college_count
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# DATABASE DEBUG
# =========================================================

@app.get("/api/debug-db")
def debug_db():

    try:

        count = (
            colleges_collection.count_documents({})
        )

        sample = list(
            colleges_collection.find(
                {},
                {
                    "_id": 1,
                    "name": 1,
                    "city": 1,
                    "district": 1,
                    "taluka": 1,
                    "university": 1,
                    "website": 1,
                    "courses": 1,
                    "courseEvidence": 1,
                    "courseSyncStatus": 1
                }
            ).limit(10)
        )

        for college in sample:
            college["_id"] = str(
                college["_id"]
            )

        return {
            "status": "success",
            "college_count": count,
            "sample": sample
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# GET ALL COLLEGES
# =========================================================

@app.get("/api/colleges")
def get_colleges():

    try:

        colleges = list(
            colleges_collection.find({})
        )

        for college in colleges:
            college["_id"] = str(
                college["_id"]
            )

        return colleges

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# GET SINGLE COLLEGE
# =========================================================

@app.get("/api/colleges/{college_id}")
def get_college(college_id: str):

    try:

        if not ObjectId.is_valid(
            college_id
        ):
            return {
                "status": "error",
                "message": "Invalid college ID"
            }

        college = (
            colleges_collection.find_one(
                {
                    "_id": ObjectId(
                        college_id
                    )
                }
            )
        )

        if not college:

            return {
                "status": "error",
                "message": "College not found"
            }

        college["_id"] = str(
            college["_id"]
        )

        return college

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# SEARCH COLLEGES
# =========================================================

@app.get("/api/search")
def search_colleges(
    course: str = "",
    city: str = ""
):

    try:

        print("\n========================================")
        print("SEARCH STARTED")
        print("COURSE:", course)
        print("CITY:", city)
        print("========================================")

        query = {}

        # -------------------------------------------------
        # COURSE
        # -------------------------------------------------

        if course.strip():

            query["courses"] = {
                "$regex": (
                    "^"
                    + re.escape(
                        course.strip()
                    )
                    + "$"
                ),
                "$options": "i"
            }

        # -------------------------------------------------
        # CITY
        # -------------------------------------------------

        if city.strip():

            query["city"] = {
                "$regex": (
                    "^"
                    + re.escape(
                        city.strip()
                    )
                    + "$"
                ),
                "$options": "i"
            }

        print(
            "MONGODB QUERY:",
            query
        )

        colleges = list(
            colleges_collection.find(
                query,
                {
                    "_id": 1,
                    "name": 1,
                    "city": 1,
                    "district": 1,
                    "taluka": 1,
                    "university": 1,
                    "collegeType": 1,
                    "courses": 1,
                    "website": 1,
                    "image": 1
                }
            )
        )

        for college in colleges:

            college["_id"] = str(
                college["_id"]
            )

        print(
            "COLLEGES FOUND:",
            len(colleges)
        )

        print(
            "SEARCH FINISHED"
        )

        print(
            "================================\n"
        )

        return colleges

    except Exception as error:

        print(
            "SEARCH ERROR:",
            error
        )

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# IMPORT SPPU COLLEGES
# =========================================================

@app.get("/api/import-sppu")
def import_sppu():

    try:

        print("\n========================================")
        print("SPPU IMPORT STARTED")
        print("========================================")

        result = import_sppu_colleges()

        print(
            "SPPU IMPORT RESULT:",
            result
        )

        return result

    except Exception as error:

        print(
            "SPPU IMPORT ERROR:",
            error
        )

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# CLEANUP BAD PUNCODE RECORD
# =========================================================

@app.delete("/api/cleanup-puncode")
def cleanup_puncode():

    try:

        result = (
            colleges_collection.delete_many(
                {
                    "$or": [
                        {
                            "name": "Puncode"
                        },
                        {
                            "puncode": "Puncode"
                        }
                    ]
                }
            )
        )

        return {
            "status": "success",
            "deleted": result.deleted_count
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# SYNC ONE COLLEGE
# =========================================================

@app.get("/api/sync-one/{college_id}")
def sync_one_college(
    college_id: str
):

    try:

        if not ObjectId.is_valid(
            college_id
        ):

            return {
                "status": "error",
                "message": "Invalid college ID"
            }

        college = (
            colleges_collection.find_one(
                {
                    "_id": ObjectId(
                        college_id
                    )
                }
            )
        )

        if not college:

            return {
                "status": "error",
                "message": "College not found"
            }

        name = college.get(
            "name",
            "Unknown College"
        )

        website = college.get(
            "website",
            ""
        )

        print("\n========================================")
        print("SINGLE COLLEGE SYNC")
        print("COLLEGE:", name)
        print("WEBSITE:", website)
        print("========================================")

        # -------------------------------------------------
        # NO WEBSITE
        # -------------------------------------------------

        if not website:

            return {
                "status": "skipped",
                "college": name,
                "message": (
                    "Official website not available"
                )
            }

        # -------------------------------------------------
        # SCRAPE
        # -------------------------------------------------

        result = scrape_courses_detailed(
            website
        )

        print(
            "DETECTED COURSES:",
            result.get("courses", [])
        )

        # -------------------------------------------------
        # SAVE RESULT
        # -------------------------------------------------

        if result.get("success"):

            courses = result.get(
                "courses",
                []
            )

            evidence = result.get(
                "evidence",
                []
            )

            pages_checked = result.get(
                "pages_checked",
                0
            )

            errors = result.get(
                "errors",
                []
            )

            colleges_collection.update_one(
                {
                    "_id": ObjectId(
                        college_id
                    )
                },
                {
                    "$set": {
                        "courses": courses,
                        "courseEvidence": evidence,
                        "pagesChecked": pages_checked,
                        "courseSyncStatus": (
                            "success"
                            if courses
                            else "no_courses_found"
                        ),
                        "courseSyncError": (
                            ""
                            if not errors
                            else str(errors)
                        )
                    }
                }
            )

            return {
                "status": (
                    "updated"
                    if courses
                    else "no_courses_found"
                ),
                "college": name,
                "website": website,
                "courses": courses,
                "evidence": evidence,
                "pages_checked": pages_checked,
                "errors": errors
            }

        # -------------------------------------------------
        # SCRAPER FAILED
        # -------------------------------------------------

        return {
            "status": "error",
            "college": name,
            "website": website,
            "message": (
                "Website could not be analyzed"
            ),
            "errors": result.get(
                "errors",
                []
            )
        }

    except Exception as error:

        print(
            "SINGLE SYNC ERROR:",
            error
        )

        return {
            "status": "error",
            "message": str(error)
        }


# =========================================================
# BATCH COURSE SYNC
# =========================================================

@app.get("/api/sync-courses")
def sync_college_courses(
    limit: int = 10,
    skip: int = 0
):

    try:

        # -------------------------------------------------
        # SAFE LIMIT
        # -------------------------------------------------

        if limit < 1:
            limit = 10

        if limit > 100:
            limit = 100

        if skip < 0:
            skip = 0

        print("\n========================================")
        print("BATCH COURSE SYNC STARTED")
        print("LIMIT:", limit)
        print("SKIP:", skip)
        print("========================================")

        # -------------------------------------------------
        # GET BATCH
        # -------------------------------------------------

        colleges = list(
            colleges_collection.find({})
            .sort(
                "_id",
                1
            )
            .skip(skip)
            .limit(limit)
        )

        processed = len(
            colleges
        )

        print(
            "COLLEGES IN BATCH:",
            processed
        )

        results = []

        updated = 0
        no_courses_found = 0
        skipped = 0
        errors = 0

        # -------------------------------------------------
        # PROCESS
        # -------------------------------------------------

        for index, college in enumerate(
            colleges,
            start=1
        ):

            college_id = college["_id"]

            name = college.get(
                "name",
                "Unknown College"
            )

            website = college.get(
                "website",
                ""
            )

            print(
                "\n----------------------------------------"
            )

            print(
                f"[{index}/{processed}]"
            )

            print(
                "COLLEGE:",
                name
            )

            print(
                "WEBSITE:",
                website
            )

            print(
                "----------------------------------------"
            )

            # -------------------------------------------------
            # NO WEBSITE
            # -------------------------------------------------

            if not website:

                skipped += 1

                results.append(
                    {
                        "college": name,
                        "status": "skipped",
                        "courses": []
                    }
                )

                continue

            # -------------------------------------------------
            # SCRAPE
            # -------------------------------------------------

            try:

                result = scrape_courses_detailed(
                    website
                )

                if not result.get(
                    "success"
                ):

                    errors += 1

                    results.append(
                        {
                            "college": name,
                            "status": "error",
                            "courses": [],
                            "errors": result.get(
                                "errors",
                                []
                            )
                        }
                    )

                    continue

                courses = result.get(
                    "courses",
                    []
                )

                evidence = result.get(
                    "evidence",
                    []
                )

                pages_checked = result.get(
                    "pages_checked",
                    0
                )

                scrape_errors = result.get(
                    "errors",
                    []
                )

                # -------------------------------------------------
                # SAVE
                # -------------------------------------------------

                colleges_collection.update_one(
                    {
                        "_id": college_id
                    },
                    {
                        "$set": {
                            "courses": courses,
                            "courseEvidence": evidence,
                            "pagesChecked": pages_checked,
                            "courseSyncStatus": (
                                "success"
                                if courses
                                else "no_courses_found"
                            ),
                            "courseSyncError": (
                                ""
                                if not scrape_errors
                                else str(
                                    scrape_errors
                                )
                            )
                        }
                    }
                )

                # -------------------------------------------------
                # RESULT
                # -------------------------------------------------

                if courses:

                    updated += 1

                    status = "updated"

                else:

                    no_courses_found += 1

                    status = "no_courses_found"

                results.append(
                    {
                        "college": name,
                        "status": status,
                        "courses": courses,
                        "pages_checked": pages_checked,
                        "evidence": evidence,
                        "errors": scrape_errors
                    }
                )

            except Exception as scrape_error:

                errors += 1

                print(
                    "SCRAPER ERROR:",
                    scrape_error
                )

                colleges_collection.update_one(
                    {
                        "_id": college_id
                    },
                    {
                        "$set": {
                            "courseSyncStatus": "error",
                            "courseSyncError": (
                                str(scrape_error)
                            )
                        }
                    }
                )

                results.append(
                    {
                        "college": name,
                        "status": "error",
                        "courses": [],
                        "message": str(
                            scrape_error
                        )
                    }
                )

        # -------------------------------------------------
        # NEXT BATCH
        # -------------------------------------------------

        next_skip = (
            skip + processed
        )

        print("\n========================================")
        print("BATCH COURSE SYNC FINISHED")
        print("========================================")

        print(
            "PROCESSED:",
            processed
        )

        print(
            "UPDATED:",
            updated
        )

        print(
            "NO COURSES:",
            no_courses_found
        )

        print(
            "SKIPPED:",
            skipped
        )

        print(
            "ERRORS:",
            errors
        )

        print(
            "NEXT SKIP:",
            next_skip
        )

        return {
            "status": "success",
            "limit": limit,
            "skip": skip,
            "processed": processed,
            "updated": updated,
            "no_courses_found": no_courses_found,
            "skipped": skipped,
            "errors": errors,
            "next_skip": next_skip,
            "results": results
        }

    except Exception as error:

        print(
            "BATCH SYNC ERROR:",
            error
        )

        return {
            "status": "error",
            "message": str(error)
        }