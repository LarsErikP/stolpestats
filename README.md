# stolpestats
An attempt to use Strava API to collect stats from activities related to Stolpejakten

# Howto obtain the Strava Access Token
- Obtain your client ID and client secret from https://www.strava.com/settings/api
- Do whatever you like to fetch the access_token, refresh_token and expires at:

You can
- Point your browser to http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read
- Note the code from the callback
- `curl -X POST https://www.strava.com/api/v3/oauth/token -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET -d code=CODE -d grant_type=authorization_code`
- Note the returning tokens and expire_date

Or... 
- Maybe try step 1-3 (https://stravalib.readthedocs.io/en/stable/get-started/authenticate-with-strava.html|here)
 

# TODO
- More stats
