import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
from stravalib import Client

# Functions
def m_to_km(dist):
    return round(dist/1000,2)

def mps_to_kmt(speed):
    return round(speed*3.6,1)

def print_duration(seconds):
    h, m, s = str(timedelta(seconds=seconds)).split(':')
    return "{} timer, {} minutter og {} sekunder".format(h,m,s)

def closest_mountain(target_height):
    name, (num, height) = min(fjell.items(), key=lambda item: abs(item[1][1] - target_height))
    return (name, num, height)

def update_stat(stat_name, name, date, data_field, data):
    stolpeturer[stat_name]["name"] = name
    stolpeturer[stat_name]["date"] = date
    stolpeturer[stat_name][data_field] = data

# Global variables
stolpeturer = { "count": 0, 
               "total_distance": 0.0,
               "total_elevation_gain": 0.0,
               "longest_trip": { "distance": 0, "name": "", "date": "" },
               "fastest_trip": { "avg_speed": 0.0, "name": "", "date": "" },
               "longest_time": { "seconds" : 0, "name": "", "date": "" }
               }

after = "2025-01-01"
fjell = {}

# Load some data from files
load_dotenv()

with open('fjell.txt', newline='') as fjellfil:
    fjell_data = csv.reader(fjellfil, delimiter=';')
    for fjell_linje in fjell_data:
        num = fjell_linje[0]
        name = fjell_linje[1]
        height = int(fjell_linje[2])
        fjell[name] = (num, height)

with open('tokens.json', "r") as f:
    token_refresh = json.load(f)

# Auth
client = Client(
        access_token=token_refresh["access_token"],
        refresh_token=token_refresh["refresh_token"],
        token_expires=token_refresh["expires_at"],
 )

# Logic starts here
activities = client.get_activities(after=after)
for activity in activities:
    if "stolpe" in activity.name.casefold():
        name = activity.name
        date = activity.start_date.strftime("%d.%m.%Y")
        stolpeturer["count"] += 1
        stolpeturer["total_distance"] += activity.distance
        stolpeturer["total_elevation_gain"] += activity.total_elevation_gain

        if activity.distance > stolpeturer["longest_trip"]["distance"]:
            update_stat("longest_trip", name, date, "distance", activity.distance)

        if activity.average_speed > stolpeturer["fastest_trip"]["avg_speed"]:
            update_stat("fastest_trip", name, date, "avg_speed", activity.average_speed)

        if activity.elapsed_time > stolpeturer["longest_time"]["seconds"]:
            update_stat("longest_time", name, date, "seconds", activity.elapsed_time)

mountain = closest_mountain(stolpeturer["total_elevation_gain"])

# Printing stats
print(f"Antall stolpeturer: {stolpeturer['count']}")
print("Total stolpejaktlengde: {} km".format(m_to_km(stolpeturer["total_distance"])))
print("Total antall høydemeter: {} m (Nærmeste å ha nådd: {} - {}m - Norges {}. høyeste fjell)".format(stolpeturer["total_elevation_gain"],
                                                                                 mountain[0],
                                                                                 mountain[2],
                                                                                 mountain[1]
                                                                                )
     )
print("Lengste tur: {} - {} ({} km)".format(stolpeturer["longest_trip"]["date"],
                                            stolpeturer["longest_trip"]["name"],
                                            m_to_km(stolpeturer["longest_trip"]["distance"])
                                            )
     )
print("Lengst tid: {} - {} ({})".format(stolpeturer["longest_time"]["date"],
                                        stolpeturer["longest_time"]["name"],
                                        print_duration(stolpeturer["longest_time"]["seconds"])
                                       )
     )
print("Raskeste tur: {} - {} (Snittfart {} km/t)".format(stolpeturer["fastest_trip"]["date"],
                                                         stolpeturer["fastest_trip"]["name"],
                                                         mps_to_kmt(stolpeturer["fastest_trip"]["avg_speed"])
                                                        )
     )

