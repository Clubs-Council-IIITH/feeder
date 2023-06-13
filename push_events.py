#!/usr/bin/env python3

import sys
import csv

from os import getenv
from tqdm import tqdm
from copy import deepcopy
from datetime import datetime
from pymongo import MongoClient

# get environment variables
MONGO_USERNAME = getenv("MONGO_USERNAME")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")
MONGO_PORT = getenv("MONGO_PORT")
MONGO_DATABASE = getenv("MONGO_DATABASE")
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongo:{MONGO_PORT}/"

# template event with default values
eventModel = {
    "clubid": "",
    "name": "",
    "datetimeperiod": ["", ""],
    "status": {
        "state": "approved",
        "room": True,
        "budget": True,
    },
    "description": "No description available",
    "mode": "hybrid",
    "audience": [],
    "link": None,

    "poster": None,

    "location": [],
    "equipment": None,
    "additional": None,
    "population": None,

    "budget": [],
}

# config
input_dt_f = "%Y-%m-%d %H:%M:%S%z"
output_df_f = "%Y-%m-%dT%H:%M:%S%z"

def main(in_csv):
    # track metrics
    successCount = 0
    failureCount = 0

    # read the CSV file
    with open(in_csv, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        # instantiate db
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DATABASE]

        # iterate over data
        for row in tqdm(reader, total=reader.line_num):
            # create a new event instance
            event = deepcopy(eventModel)

            # set event attributes
            event["clubid"] = row["clubid"]
            event["name"] = row["name"]
            event["datetimeperiod"][0] = str(datetime.strptime(row["datetimeStart"], input_dt_f).strftime(output_df_f))
            event["datetimeperiod"][1] = str(datetime.strptime(row["datetimeEnd"], input_dt_f).strftime(output_df_f))
            event["mode"] = row["mode"]
            event["audience"] = row["audience"].replace(" ", "").split(";")
            event["description"] = row["description"] if row["description"] != "" else event["description"]
            event["link"] = row["link"] if row["link"] != "" else event["link"]
            event["location"] = row["location"].split(";") if row["location"] else event["location"]
            event["population"] = int(row["population"])
            event["poster"] = row["poster"] if row["poster"] != "" else event["poster"]

            # insert into db
            try:
                db.events.insert_one(event)
                successCount += 1
            except Exception as e:
                print(f"Failed: {e}")
                failureCount += 1

    return successCount, failureCount

if __name__ == "__main__":
    in_csv = sys.argv[1]
    successCount, failureCount = main(in_csv)
    print(f"Done. Success: {successCount}, Failed: {failureCount}")