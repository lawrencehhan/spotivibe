import base64
from dotenv import load_dotenv
import json
import os
import requests
import pandas as pd


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

def getTrackAudio(bearer_token: str, track_id: str):
    target_url = f'{baseUrl}/audio-features/{track_id}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def testRun(auth_code: str):
    bt = getAuthorizationCodeFlowToken(auth_code)
    playlists = getUserPlaylists(bt, offset = 1, limit=1)
    bahb_id = playlists['items'][0]['id']
    field_options_url = _createFieldOptionsUrl(current_field_options)
    items = getPlaylistItems(bt, bahb_id, field_options_url, limit=1)
    item = items['items'][0]
    track = item['track']
    track_id = track['id']
    track_audio = getTrackAudio(bt, track_id)
    df = pd.DataFrame(columns=['added_at', 'name', 'id','duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'])

def getAllTrackData(bearer_token: str, playlist_id: str, field_options_url: str):
    # bearer_token = getAuthorizationCodeFlowToken(auth_code)
    
    return




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



