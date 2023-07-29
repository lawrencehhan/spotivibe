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


def getGenreSeeds(bearer_token: str):
    # Get list of genres: https://developer.spotify.com/console/get-available-genre-seeds/
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    genre_list = sendGetRequest(bearer_token, url)
    adjusted_genre_list = ["r&b" if genre=="r-n-b" else genre for genre in genre_list["genres"]]
    # Faulty genres found on 8/10/22
    faulty_genres = [
        "bossanova",
        "holidays",
        "metal-misc",
        "movies",
        "new-release",
        "philippines-opm",
        "post-dubstep",
        "rainy-day",
        "road-trip",
        "soundtracks",
        "summer",
        "work-out"
    ]
    adjusted_genre_list = [genre for genre in adjusted_genre_list if genre not in faulty_genres]
    return adjusted_genre_list

def checkArtistAvailable(bearer_token: str, seed_genre: str):
    # Check individual genre for Artist availablility (boolean return)
    artist_info = getSearchResults(bearer_token,  f"genre:{seed_genre}", 'artist', 3)
    total_artists = artist_info["artists"]["total"]
    if total_artists < 2:
        return False
    else: 
        return True


def getSearchResults(bearer_token: str, query: str, search_type: str, limit: int):
    # Get recommended songs: https://developer.spotify.com/console/get-recommendations/
    url = _createSearchUrl(query, search_type, limit)
    search_results = sendGetRequest(bearer_token, url)
    return search_results


def getRecommendations(
    bearer_token: str,
    limit: int,
    market: str,
    seed_artists: str,
    seed_genres: str,
    seed_tracks: str,
    target_energy: float,
    target_loudness: float,
    target_tempo: float
):
    # Get recommended songs: https://developer.spotify.com/console/get-recommendations/
    url = _createRecommendationsUrl(
        limit, market, seed_artists, seed_genres, seed_tracks, target_energy, target_loudness, target_tempo
    )
    recommendations = sendGetRequest(bearer_token, url)
    return recommendations


def sendGetRequest(bearer_token: str, url: str):
    headers = {"Authorization": "Bearer " + bearer_token}
    response = requests.get(url, headers=headers)
    response_content = response.json()
    return response_content


def _createSearchUrl(query: str, search_type: str, limit: int):
    base_url = "https://api.spotify.com/v1/search?"
    query = "q=" + query.replace("&", "%26").replace(" ", "%20")
    search_type = "&type=" + search_type
    limit = "&limit=" + str(limit)
    search_url = base_url + query + search_type + limit
    return search_url


def _createRecommendationsUrl(
    limit: int, 
    market: str, 
    seed_artist: str, 
    seed_genre: str, 
    seed_track: str,
    target_energy: float,
    target_loudness: float,
    target_tempo: float
):
    base_url = "https://api.spotify.com/v1/recommendations?"
    limit = "limit=" + str(limit)
    market = "&market=US"
    seed_artist = (
        "&seed_artists=" + seed_artist
    )  # Example: 3TVXtAsR1Inumwj472S9r4 Drake
    seed_genre = "&seed_genres=" + seed_genre  # Example: pop
    seed_track = (
        "&seed_tracks=" + seed_track
    )  # Example: 7wcWkzT1X75DguAwOWxlGt Way 2 Sexy
    target_energy = "&target_energy=" + str(target_energy)
    target_loudness = "&target_loudness=" + str(target_loudness)
    target_tempo = "&target_tempo=" + str(target_tempo)

    recommendations_url = (
        base_url + limit + market + seed_artist + seed_genre + seed_track + target_energy + target_loudness + target_tempo
    )
    return recommendations_url


def getSeedFromGenre(bearer_token: str, seed_genre: str, search_type: str, total_seeds: int):
    seeds = getSearchResults(bearer_token, f"genre:{seed_genre}", search_type, total_seeds)
    seed_selection = randint(0, total_seeds-1)
    seed = seeds[f'{search_type}s']['items'][seed_selection]
    seed_id = seed['id']
    seed_name = seed['name']
    return (seed_id, seed_name)

def getArtistSeedFromGenre(bearer_token: str, seed_genre: str, total_seeds: int):
    seeds = getSearchResults(bearer_token, f"genre:{seed_genre}", "artist", total_seeds)
    seed_selection_first, seed_selection_second  = findPopularArtists(seeds)
    artist_first, artist_second = seeds['artists']['items'][seed_selection_first], seeds['artists']['items'][seed_selection_second]
    artist_id_first, artist_id_second = artist_first['id'], artist_second['id']
    artist_name_first, artist_name_second = artist_first['name'], artist_second['name']
    return (artist_id_first, artist_name_first, artist_id_second, artist_name_second)

def findPopularArtists(artistSeeds):
    popularities = [item["popularity"] for item in artistSeeds['artists']['items']]
    item_num_most = popularities.index(max(popularities))
    del popularities[item_num_most]
    item_num_second = popularities.index(max(popularities))
    return item_num_most, item_num_second

def getTrackSeedFromArtist(bearer_token: str, seed_artist: str, total_seeds: int):
    seeds = getSearchResults(bearer_token, f"artist:{seed_artist}", 'track', total_seeds)
    seed_selection = randint(0, total_seeds-1)
    track_seed = seeds['tracks']['items'][seed_selection]
    track_id = track_seed['id']
    track_name = track_seed['name']
    return (track_id, track_name)


# Manually retrieve list of faulty genre lists to update adjusted genre list
def getFaultyGenreSeeds(bearer_token: str):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    genre_list = sendGetRequest(bearer_token, url)
    adjusted_genre_list = ["r&b" if genre=="r-n-b" else genre for genre in genre_list["genres"]]
    faulty_genre_list = list(filter(lambda genre: not checkArtistAvailable(bearer_token, genre), adjusted_genre_list))
    return faulty_genre_list