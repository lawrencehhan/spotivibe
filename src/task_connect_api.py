import base64
from dotenv import load_dotenv
import json
import os
import requests


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
baseUrl = 'https://api.spotify.com/v1'
current_field_options = 'total,limit,offset,items(added_by,added_at,is_local,track(album,artists,disc_number,duration_ms,explicit,external_urls,id,name,popularity,track_number))'

def getAuthorizationCodeFlowToken(auth_code: str):
    token_url = "https://accounts.spotify.com/api/token"
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("ascii")
    credentials_base64 = base64.b64encode(credentials).decode("ascii")
    
    auth_headers = {
        "Authorization": f'Basic {credentials_base64}',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:8888/callback"
    }
    
    response = requests.post(token_url, data=auth_data, headers=auth_headers)
    try:
        bearer_token = (json.loads(response.content.decode("ascii")))["access_token"]
    except:
        # log.error("Invalid Client ID or Client Secret in .env file")
        quit()
    return bearer_token

def sendGetRequest(bearer_token: str, url: str):
    headers = {"Authorization": f'Bearer {bearer_token}'}
    response = requests.get(url, headers=headers)
    response_content = response.json()
    return response_content

def getUserID(bearer_token: str, baseUrl: str = baseUrl):
    target_url = f'{baseUrl}/me'
    print(target_url)
    response = sendGetRequest(bearer_token, target_url)
    return response

def getUserPlaylists(bearer_token: str, offset: int = 0, limit: int = 50, baseUrl: str = baseUrl):
    target_url = f'{baseUrl}/me/playlists?offset={offset}&limit={limit}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def _createFieldOptionsUrl(field_options: str):
    # Follows the fields translation found on Spotify's api
    # https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks
    field_options_url = field_options.replace(',','%2C').replace('(','%28').replace(')','%29')
    return field_options_url

def getPlaylistItems(bearer_token: str, playlist_id: str, field_options_url: str, limit: int = 50, offset: int = 0):
    target_url = f'{baseUrl}/playlists/{playlist_id}/tracks?fields={field_options_url}&limit={limit}&offset={offset}'
    response = sendGetRequest(bearer_token, target_url)
    return response






## OLD client credentials flow method
def getClientCredentialsFlow():
    # Client Credentials Flow: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    token_url = "https://accounts.spotify.com/api/token"
    message = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("ascii")
    base64_message = base64.b64encode(message).decode("ascii")

    auth_headers = {"Authorization": "Basic " + base64_message}
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(token_url, data=auth_data, headers=auth_headers)
    try:
        bearer_token = (json.loads(response.content.decode("ascii")))["access_token"]
    except:
        log.error("Invalid Client ID or Client Secret in .env file")
        quit()
    return bearer_token



