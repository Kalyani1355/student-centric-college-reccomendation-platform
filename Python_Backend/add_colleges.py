from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

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
colleges_collection = db["colleges"]

colleges = [
    {
        "name": "Symbiosis Institute of Technology",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹2,50,000/year",
        "placement": "90%",
        "highestPackage": "₹50 LPA",
        "averagePackage": "₹8 LPA",
        "rating": 4.7,
        "image": "",
        "website": "https://www.sitpune.edu.in",
        "description": "A technology institute in Pune offering undergraduate engineering programs."
    },
    {
        "name": "Vishwakarma Institute of Technology",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,80,000/year",
        "placement": "92%",
        "highestPackage": "₹44 LPA",
        "averagePackage": "₹8 LPA",
        "rating": 4.6,
        "image": "",
        "website": "https://www.vit.edu",
        "description": "An engineering institute in Pune offering undergraduate technology programs."
    },
    {
        "name": "COEP Technological University",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,40,000/year",
        "placement": "95%",
        "highestPackage": "₹50 LPA",
        "averagePackage": "₹10 LPA",
        "rating": 4.8,
        "image": "",
        "website": "https://www.coeptech.ac.in",
        "description": "A public technological university in Pune."
    },
    {
        "name": "AISSMS College of Engineering",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,20,000/year",
        "placement": "85%",
        "highestPackage": "₹18 LPA",
        "averagePackage": "₹5.5 LPA",
        "rating": 4.3,
        "image": "",
        "website": "https://aissmsioit.org",
        "description": "An engineering college in Pune offering undergraduate engineering programs."
    },
    {
        "name": "Sinhgad College of Engineering",
        "course": "B.Tech,MCA",
        "city": "Pune",
        "fees": "₹1,30,000/year",
        "placement": "86%",
        "highestPackage": "₹30 LPA",
        "averagePackage": "₹6 LPA",
        "rating": 4.4,
        "image": "",
        "website": "https://cms.sinhgad.edu",
        "description": "An engineering and postgraduate institute in Pune."
    },
    {
        "name": "Modern College of Arts, Science and Commerce",
        "course": "B.Sc,BCA,B.Com,BA",
        "city": "Pune",
        "fees": "₹45,000/year",
        "placement": "75%",
        "highestPackage": "₹12 LPA",
        "averagePackage": "₹4 LPA",
        "rating": 4.3,
        "image": "",
        "website": "https://moderncollegepune.edu.in",
        "description": "An undergraduate college offering arts, science and commerce programs."
    },
    {
        "name": "Fergusson College",
        "course": "B.Sc,BA,B.Com",
        "city": "Pune",
        "fees": "₹35,000/year",
        "placement": "78%",
        "highestPackage": "₹12 LPA",
        "averagePackage": "₹4.5 LPA",
        "rating": 4.6,
        "image": "",
        "website": "https://fergusson.edu",
        "description": "An autonomous college in Pune offering undergraduate programs."
    },
    {
        "name": "Nowrosjee Wadia College",
        "course": "B.Sc,BA",
        "city": "Pune",
        "fees": "₹30,000/year",
        "placement": "72%",
        "highestPackage": "₹10 LPA",
        "averagePackage": "₹4 LPA",
        "rating": 4.4,
        "image": "",
        "website": "https://nowrosjeewadia.mespune.org",
        "description": "An autonomous college in Pune offering undergraduate arts and science programs."
    },
    {
        "name": "MKSSS's Cummins College of Engineering for Women",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,60,000/year",
        "placement": "94%",
        "highestPackage": "₹45 LPA",
        "averagePackage": "₹9 LPA",
        "rating": 4.7,
        "image": "",
        "website": "https://cumminscollege.org",
        "description": "An engineering college in Pune offering undergraduate programs for women."
    },
    {
        "name": "Bharati Vidyapeeth College of Engineering",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,50,000/year",
        "placement": "88%",
        "highestPackage": "₹30 LPA",
        "averagePackage": "₹6 LPA",
        "rating": 4.3,
        "image": "",
        "website": "https://bvdu.ac.in",
        "description": "An engineering institute in Pune."
    },
    {
        "name": "Poona College of Arts, Science and Commerce",
        "course": "B.Sc,B.Com,BCA",
        "city": "Pune",
        "fees": "₹40,000/year",
        "placement": "70%",
        "highestPackage": "₹10 LPA",
        "averagePackage": "₹3.8 LPA",
        "rating": 4.2,
        "image": "",
        "website": "https://poonacollege.edu.in",
        "description": "An undergraduate college in Pune offering arts, science and commerce programs."
    },
    {
        "name": "Abasaheb Garware College",
        "course": "B.Sc,BA,B.Com",
        "city": "Pune",
        "fees": "₹35,000/year",
        "placement": "73%",
        "highestPackage": "₹10 LPA",
        "averagePackage": "₹4 LPA",
        "rating": 4.3,
        "image": "",
        "website": "https://garwarecollege.mespune.org",
        "description": "An autonomous college in Pune offering undergraduate programs."
    },
    {
        "name": "Sir Parashurambhau College",
        "course": "B.Sc,BA,B.Com",
        "city": "Pune",
        "fees": "₹30,000/year",
        "placement": "72%",
        "highestPackage": "₹10 LPA",
        "averagePackage": "₹4 LPA",
        "rating": 4.4,
        "image": "",
        "website": "https://spcollegepune.ac.in",
        "description": "An autonomous undergraduate college in Pune."
    },
    {
        "name": "Parvatibai Genba Moze College of Engineering",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,10,000/year",
        "placement": "80%",
        "highestPackage": "₹15 LPA",
        "averagePackage": "₹5 LPA",
        "rating": 4.1,
        "image": "",
        "website": "https://pgmcoe.ac.in",
        "description": "An engineering college in Pune."
    },
    {
        "name": "Genba Sopanrao Moze College of Engineering",
        "course": "B.Tech",
        "city": "Pune",
        "fees": "₹1,10,000/year",
        "placement": "80%",
        "highestPackage": "₹15 LPA",
        "averagePackage": "₹5 LPA",
        "rating": 4.1,
        "image": "",
        "website": "https://gsmcoe.org",
        "description": "An engineering college in Pune."
    },
    {
        "name": "Ramdeobaba University",
        "course": "B.Tech,BCA,BBA",
        "city": "Nagpur",
        "fees": "₹1,50,000/year",
        "placement": "90%",
        "highestPackage": "₹45 LPA",
        "averagePackage": "₹7 LPA",
        "rating": 4.6,
        "image": "",
        "website": "https://www.rknec.edu",
        "description": "A university in Nagpur offering technology and management programs."
    },
    {
        "name": "Yeshwantrao Chavan College of Engineering",
        "course": "B.Tech",
        "city": "Nagpur",
        "fees": "₹1,30,000/year",
        "placement": "88%",
        "highestPackage": "₹35 LPA",
        "averagePackage": "₹6 LPA",
        "rating": 4.5,
        "image": "",
        "website": "https://ycce.edu",
        "description": "An engineering institute in Nagpur."
    },
    {
        "name": "St. Vincent Pallotti College of Engineering and Technology",
        "course": "B.Tech",
        "city": "Nagpur",
        "fees": "₹1,20,000/year",
        "placement": "84%",
        "highestPackage": "₹20 LPA",
        "averagePackage": "₹5.5 LPA",
        "rating": 4.3,
        "image": "",
        "website": "https://www.stvincentngp.edu.in",
        "description": "An engineering college in Nagpur."
    },
    {
        "name": "Sandip University",
        "course": "B.Tech,BCA,B.Sc,BBA",
        "city": "Nashik",
        "fees": "₹1,20,000/year",
        "placement": "82%",
        "highestPackage": "₹20 LPA",
        "averagePackage": "₹5 LPA",
        "rating": 4.2,
        "image": "",
        "website": "https://www.sandipuniversity.edu.in",
        "description": "A university in Nashik offering technology, science and management programs."
    },
    {
        "name": "MET Bhujbal Knowledge City",
        "course": "B.Tech,BCA,MBA",
        "city": "Nashik",
        "fees": "₹1,15,000/year",
        "placement": "80%",
        "highestPackage": "₹18 LPA",
        "averagePackage": "₹5 LPA",
        "rating": 4.2,
        "image": "",
        "website": "https://www.metbhujbalknowledgecity.ac.in",
        "description": "An educational campus in Nashik offering technology and management programs."
    }
]

result = colleges_collection.insert_many(colleges)

print("====================================")
print("20 COLLEGES ADDED SUCCESSFULLY!")
print("====================================")
print("Number of colleges inserted:", len(result.inserted_ids))

client.close()