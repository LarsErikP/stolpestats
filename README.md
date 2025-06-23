# stolpestats
An attempt to use Strava API to collect stats from activities related to Stolpejakten. Everything depends on the fact that you put the word "stolpe" into your Strava Activities

## Howto obtain the Strava Access Token
- Obtain your client ID and client secret from https://www.strava.com/settings/api
- Do whatever you like to fetch the access_token, refresh_token and expires at:

You can
- Point your browser to http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read
- Note the code from the callback
- `curl -X POST https://www.strava.com/api/v3/oauth/token -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET -d code=CODE -d grant_type=authorization_code`
- Note the returning tokens and expire_date

Or... 
- Or maybe try step 1-3 [here](https://stravalib.readthedocs.io/en/stable/get-started/authenticate-with-strava.html)

## Store some secrets
With the above data in hand, create `tokens.json`
~~~
{
        "access_token": "<ACCESS_TOKEN>",
        "refresh_token": "<REFRESH_TOKEN>",
        "expires_at": <expire in epoch format>
}
~~~
And `.env`
~~~python
STRAVA_CLIENT_ID='<CLIENT_ID>'
STRAVA_CLIENT_SECRET='<CLIENT_SECRET>'
~~~

## Usage
Clone repo and then
~~~
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 getStolpeStats.py
~~~


## TODO
- More stats
