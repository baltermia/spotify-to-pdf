from config import get_config, save_config
import requests
from datetime import datetime, timedelta
from dateutil import parser

def __get_headers():
    def create_header(token):
        return {
            'Authorization': 'Bearer {}'.format(token)
        } 

    config = get_config()
    c_spotify = config["SPOTIFY"]
    expiration_date = c_spotify["token_expiration"]

    if expiration_date != "" and expiration_date != None and expiration_date.strip() != "":
        if datetime.now() < parser.isoparse(c_spotify["token_expiration"]):
            return create_header(c_spotify["token"])

    client_id = c_spotify["cid"]
    client_secret = c_spotify["secret"]

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post("https://accounts.spotify.com/api/token", data)

    token = response.json().get("access_token")
    expiration = response.json().get("expires_in")

    c_spotify["token"] = token
    c_spotify["token_expiration"] = (datetime.now() + timedelta(seconds = expiration)).isoformat()

    config["SPOTIFY"] = c_spotify
    save_config(config)

    return create_header(c_spotify["token"])

def get_playlist(id):
    headers = __get_headers()

    response = requests.get("https://api.spotify.com/v1/playlists/" + id, headers = headers)

    return response.json()
