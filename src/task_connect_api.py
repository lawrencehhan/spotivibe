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

def sendPostRequest(bearer_token: str, url: str, body: dict):
    headers = {"Authorization": f'Bearer {bearer_token}'}
    request_body = json.dumps(body)
    response = requests.post(url, headers=headers, data=request_body)
    response_content = response.json()
    return response_content

def getUserID(bearer_token: str, baseUrl: str = baseUrl):
    target_url = f'{baseUrl}/me'
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

def getSpotifyGenres(bearer_token: str, baseUrl: str = baseUrl):
    target_url = f'{baseUrl}/recommendations/available-genre-seeds'
    response = sendGetRequest(bearer_token, target_url)
    try:
        genre_set = {genre for genre in response['genres']}
    except:
        genre_set = {'No Genres Returned'}
    return genre_set

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

def getArtist(bearer_token: str, artist_id: str):
    target_url = f'{baseUrl}/artists/{artist_id}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def createPlaylist(bearer_token: str, user_id: str, name: str, public: bool = False, collaborative: bool = False, description: str = 'New Spotivibe playlist'):
    target_url = f'{baseUrl}/users/{user_id}/playlists'
    body = {
        "name": name,
        "public": public,
        "collaborative": collaborative,
        "description": description
    }
    response = sendPostRequest(bearer_token, target_url, body)
    return response

def addTracksToPlaylist(bearer_token: str, playlist_id: str, tracks: list):
    target_url = f'{baseUrl}/playlists/{playlist_id}/tracks'
    body = {"uris": tracks}
    response = sendPostRequest(bearer_token, target_url, body)
    return response

def testRun(auth_code: str):
    bt = getAuthorizationCodeFlowToken(auth_code)
    user_id = getUserID(bt)['id']
    playlists = getUserPlaylists(bt, offset = 6, limit=5)
    bahb = playlists['items'][1]
    bahb_id = bahb['id']
    custom_field_options_url = _createFieldOptionsUrl(current_field_options)
    
    playlist = getPlaylist(bt, bahb_id, custom_field_options_url, limit=5, offset=3363)
    filtered_playlist = convertPlaylistItemsToTracks(playlist)
    cleaned_playlist = preparePlaylist(filtered_playlist, bt)
    df = playlistToDataFrame(cleaned_playlist)

    # new_playlist = createPlaylist(bt, user_id, name="spotivibe_test")
    new_playlist_id = '09naepORkqG4OvU2VgH9jz'
    artist_id = playlist['items'][-1]['track']['artists'][0]['id']
    zion_t = '5HenzRvMtSrgtvU16XAoby'
    artist_genres = getArtist(bt, zion_t)['genres']


def getAllTrackData(bearer_token: str, playlist_id: str, field_options_url: str):
    # bearer_token = getAuthorizationCodeFlowToken(auth_code)
    
    return





