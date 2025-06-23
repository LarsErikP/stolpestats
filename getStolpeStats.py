import json
from datetime import datetime
from dotenv import load_dotenv
from stravalib import Client
import requests

def to_km(dist):
    return round(dist/1000,2)

with open('tokens.json', "r") as f:
    token_refresh = json.load(f)

load_dotenv()
client = Client(
        access_token=token_refresh["access_token"],
        refresh_token=token_refresh["refresh_token"],
        token_expires=token_refresh["expires_at"],
 )

stolpeturer_count = 0
stolpeturer_total_distance = 0.0
longest_trip_distance = 0
longest_trip_name = ""
longest_trip_date = ""

after = "2025-01-01"
page = 1 # Integer | Page number. Defaults to 1. (optional)
perPage = 30 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)

activities = client.get_activities(after=after)
for activity in activities:
    if "stolpe" in activity.name.casefold():
        stolpeturer_count += 1
        stolpeturer_total_distance += activity.distance
        if activity.distance > longest_trip_distance:
            #date = datetime.strftime(activity.start_date, "%Y-%m-%dT%H:%M:%SZ")
            longest_trip_distance = activity.distance
            longest_trip_name = activity.name
            longest_trip_date = activity.start_date.strftime("%d.%m.%Y")

print(f"Antall stolpeturer: {stolpeturer_count}")
print("Total stolpejaktlengde: {} km".format(to_km(stolpeturer_total_distance)))
print("Lengste tur: {} - {} ({} km)".format(longest_trip_date, longest_trip_name, to_km(longest_trip_distance)))
