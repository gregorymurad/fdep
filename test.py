import pymongo
import datetime
import random
import time
import streamlit as st

# MongoDB client setup
client = pymongo.MongoClient(st.secrets["SWARM_CONNECTION_STRING"])
db = client["biscaynebay"]
collection = db["weird_database"]


def generate_data():
    # Base coordinates
    base_latitude = 25.909617521666668
    base_longitude = -80.13719838

    # Generate small variations for geolocation and environmental data
    data = {
        "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.datetime.now().strftime("%H:%M:%S"),
        "latitude": base_latitude + random.uniform(-0.0005, 0.0005),
        "longitude": base_longitude + random.uniform(-0.0005, 0.0005),
        "Chl (ug/L)": str(random.uniform(0.0, 10.0)),
        "BGA-PE (ug/L)": str(random.uniform(0.0, 10.0)),
        "Turb (FNU)": str(random.uniform(-0.1, 0.1)),
        "TSS (mg/L)": str(random.uniform(0.0, 50.0)),
        "ODO (%sat)": str(random.uniform(90.0, 100.0)),
        "ODO (mg/l)": str(random.uniform(5.0, 8.0)),
        "Temp (C)": str(random.uniform(20.0, 30.0)),
        "Cond (uS/cm)": str(random.uniform(50000, 55000)),
        "Sal (PPT)": str(random.uniform(30.0, 40.0)),
        "Pressure (psi a)": str(random.uniform(10.0, 20.0)),
        "Depth (m)": str(random.uniform(0.0, 30.0))
    }
    return data

try:
    while True:
        # Generate document with varying coordinates and sensor data
        document = generate_data()

        # Insert document into MongoDB
        collection.insert_one(document)
        print(f"Document inserted: {document}")

        # Sleep for a specified time (e.g., 10 seconds) between inserts
        time.sleep(5)
except KeyboardInterrupt:
    print("Script interrupted by user.")