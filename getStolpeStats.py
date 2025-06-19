import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import json
from datetime import datetime
from dotenv import dotenv_values

def to_km(dist):
    return round(dist/1000,2)

env = dotenv_values(".env")

stolpeturer_count = 0
stolpeturer_total_distance = 0.0
longest_trip_distance = 0
longest_trip_name = ""
longest_trip_date = ""

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi()

# Configure OAuth2 access token for authorization: strava_oauth
api_instance.api_client.configuration.access_token = env["STRAVA_ACCESS_TOKEN"]

after = 1735686000 # Integer | An epoch timestamp to use for filtering activities that have taken place after a certain time. (optional)
#after = 1750284000
page = 1 # Integer | Page number. Defaults to 1. (optional)
perPage = 30 # Integer | Number of items per page. Defaults to 30. (optional) (default to 30)

try: 
    # List Athlete Activities
    api_response = api_instance.get_logged_in_athlete_activities(after=after, page=page, per_page=perPage)
    data_set = json.loads(str(api_response).replace("'", '"').replace('None','"None"').replace('False','"False"'))

    for activity in data_set:
        if "stolpe" in activity['name'].casefold():
            stolpeturer_count += 1
            stolpeturer_total_distance += activity['distance']

            if activity['distance'] > longest_trip_distance:
                date = datetime.strptime(activity['start_date'], "%Y-%m-%dT%H:%M:%SZ")
                longest_trip_distance = activity['distance']
                longest_trip_name = activity['name']
                longest_trip_date = date.strftime("%d.%m.%Y")

    print(f"Antall stolpeturer: {stolpeturer_count}")
    print("Total stolpejaktlengde: {} km".format(to_km(stolpeturer_total_distance)))
    print("Lengste tur: {} - {} ({} km)".format(longest_trip_date, longest_trip_name, to_km(longest_trip_distance)))
except ApiException as e:
    print("Exception when calling ActivitiesApi->getLoggedInAthleteActivities: %s\n" % e)


