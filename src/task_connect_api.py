import base64
from dotenv import load_dotenv
import json
import os
import requests
import pandas as pd
# Temp imports delete later
from task_playlist_management import convertPlaylistItemsToTracks, preparePlaylist, playlistToDF

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

def getPlaylist(bearer_token: str, playlist_id: str, field_options_url: str, limit: int = 50, offset: int = 0):
    target_url = f'{baseUrl}/playlists/{playlist_id}/tracks?fields={field_options_url}&limit={limit}&offset={offset}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def getTrack(bearer_token: str, track_id: str):
    target_url = f'{baseUrl}/tracks/{track_id}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def getTrackAudio(bearer_token: str, track_id: str):
    target_url = f'{baseUrl}/audio-features/{track_id}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def testRun(auth_code: str):
    bt = getAuthorizationCodeFlowToken(auth_code)
    playlists = getUserPlaylists(bt, offset = 6, limit=5)
    bahb = playlists['items'][0]
    bahb_id = bahb['id']
    custom_field_options_url = _createFieldOptionsUrl(current_field_options)
    
    playlist = getPlaylist(bt, bahb_id, custom_field_options_url, limit=50, offset=3282)
    filtered_playlist = convertPlaylistItemsToTracks(playlist)
    cleaned_playlist = preparePlaylist(filtered_playlist, bt)
    df = playlistToDataFrame(cleaned_playlist)

    # items = playlist['items']
    # item = items[0]
    # track = item['track']
    # track_ex = filtered_playlist[-1]
    # track_id = track_ex['id']
    # track_audio = getTrackAudio(bt, track_id)
    # df = pd.DataFrame(columns=['added_at', 'name', 'id','duration_ms', 'explicit', 'popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'])

def getAllTrackData(bearer_token: str, playlist_id: str, field_options_url: str):
    # bearer_token = getAuthorizationCodeFlowToken(auth_code)
    
    return





