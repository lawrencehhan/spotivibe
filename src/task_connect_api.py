import base64
from dotenv import load_dotenv
import json
import os
import requests
from structlog import get_logger
from random import randint


load_dotenv()
log = get_logger(__name__)
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
baseUrl = 'https://api.spotify.com/v1'

def getSpotifyToken():
    # Client Credentials Flow: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    authUrl = "https://accounts.spotify.com/api/token"
    message = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("ascii")
    base64_message = base64.b64encode(message).decode("ascii")

    auth_headers = {"Authorization": "Basic " + base64_message}
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(authUrl, data=auth_data, headers=auth_headers)
    try:
        bearer_token = (json.loads(response.content.decode("ascii")))["access_token"]
    except:
        log.error("Invalid Client ID or Client Secret in .env file")
        quit()
    return bearer_token

def sendGetRequest(bearer_token: str, url: str):
    headers = {"Authorization": f'Bearer {bearer_token}'}
    response = requests.get(url, headers=headers)
    response_content = response.json()
    return response_content

def getUserID(bearer_token: str, baseUrl: str):
    target_url = f'{baseUrl}/me'
    print(target_url)
    response = sendGetRequest(bearer_token, target_url)
    return response

def getUserPlaylists(bearer_token: str, user_id: str, offset: int, limit: int, baseUrl: str = baseUrl):
    target_url = f'{baseUrl}/users/{user_id}/playlists?offset={offset}&limit={limit}'
    response = sendGetRequest(bearer_token, target_url)
    return response

def getTest(bt, baseUrl):
    print(baseUrl)
    payload = {}
    headers = {
        'Authorization': f'Bearer {bt}'
    }
    print(headers)

    response = requests.request("GET", baseUrl, headers=headers, data=payload)
    print(response.text)


