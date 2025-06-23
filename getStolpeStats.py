import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from stravalib import Client
import requests

def m_to_km(dist):
    return round(dist/1000,2)

def mps_to_kmt(speed):
    return round(speed*3.6,1)

def closest_mountain(target_height):
    return min(fjell.items(), key=lambda item: abs(item[1] - target_height))

load_dotenv()

stolpeturer = { "count": 0, 
               "total_distance": 0.0,
               "total_elevation_gain": 0.0,
               "longest_trip": { "distance": 0, "name": "", "date": "" },
               "fastest_trip": { "avg_speed": 0.0, "name": "", "date": "" }
               }

after = "2025-01-01"
fjell = {}

with open('fjell.txt', newline='') as fjellfil:
    fjell_data = csv.reader(fjellfil, delimiter=';')
    for fjell_linje in fjell_data:
        name = fjell_linje[0]
        height = int(fjell_linje[1])
        fjell[name] = height

with open('tokens.json', "r") as f:
    token_refresh = json.load(f)

client = Client(
        access_token=token_refresh["access_token"],
        refresh_token=token_refresh["refresh_token"],
        token_expires=token_refresh["expires_at"],
 )



activities = client.get_activities(after=after)
for activity in activities:
    if "stolpe" in activity.name.casefold():
        stolpeturer["count"] += 1
        stolpeturer["total_distance"] += activity.distance
        stolpeturer["total_elevation_gain"] += activity.total_elevation_gain
        if activity.distance > stolpeturer["longest_trip"]["distance"]:
            stolpeturer["longest_trip"]["distance"] = activity.distance
            stolpeturer["longest_trip"]["name"] = activity.name
            stolpeturer["longest_trip"]["date"]= activity.start_date.strftime("%d.%m.%Y")

        if activity.average_speed > stolpeturer["fastest_trip"]["avg_speed"]:
            stolpeturer["fastest_trip"]["avg_speed"] = activity.average_speed
            stolpeturer["fastest_trip"]["name"] = activity.name
            stolpeturer["fastest_trip"]["date"]= activity.start_date.strftime("%d.%m.%Y")

mountain = closest_mountain(stolpeturer["total_elevation_gain"])
print(f"Antall stolpeturer: {stolpeturer['count']}")
print("Total stolpejaktlengde: {} km".format(m_to_km(stolpeturer["total_distance"])))
print("Total antall høydemeter: {} m (Nærmeste fjelltopp nådd: {} - {}m)".format(stolpeturer["total_elevation_gain"],
                                                                                mountain[0],
                                                                                mountain[1],
                                                                                )
     )
print("Lengste tur: {} - {} ({} km)".format(stolpeturer["longest_trip"]["date"],
                                            stolpeturer["longest_trip"]["name"],
                                            m_to_km(stolpeturer["longest_trip"]["distance"])
                                            )
     )
print("Raskeste tur: {} - {} (Snittfart {} km/t)".format(stolpeturer["fastest_trip"]["date"],
                                                         stolpeturer["fastest_trip"]["name"],
                                                         mps_to_kmt(stolpeturer["fastest_trip"]["avg_speed"])
                                                        )
     )
