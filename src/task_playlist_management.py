import pandas as pd
from task_connect_api import getTrack, getTrackAudio

# Get rid of excess info from Spotify's default get-playlist-items response and refromat them to tracks
def filterItem(item: dict):
    # Parent items wanted from 'item' 
    added_at = item['added_at']
    raw_track = item['track']
    # Filtering and reconstructing item to track
    album_filter_keys = ['id', 'name', 'release_date']
    raw_track['album'] = {key: raw_track['album'][key] for key in album_filter_keys}
    track_filter_keys = ['album', 'artists', 'duration_ms', 'explicit', 'external_urls', 'id', 'name', 'popularity']
    filtered_track = {key: raw_track[key] for key in track_filter_keys}
    return filtered_track

# Item requests have superfluous info with nested tracks, and so they will be converted to new track{} schemas
def convertPlaylistItemsToTracks(playlist: dict):
    items = playlist['items'] # [{},{},{}]
    filtered_playlist = [filterItem(item) for item in items]
    return filtered_playlist

# Collect all playlist items into one Pandas df
def collectFullPlaylist(bearer_token: str, playlist_id: str):
    return


def dispTrackInfo(bearer_token: str, track_id: str):
    track = getTrack(bearer_token, track_id)
    # Collect list in case there are multiple artists
    artists = []
    for artist in track['artists']:
        artists.append(artist['name'])
    # Converting millisecond durations to minutes and seconds
    minutes, seconds = convertDuration(track['duration_ms'])
    duration = f'{minutes}:{seconds}'
    track_audio = getTrackAudio(bearer_token, track_id)
    track_info = {
        'Track': track['name'],
        'Artists': artists,
        'Track ID': track['id'],
        'Duration': duration,
        'Danceability': track_audio['danceability'],
        'Energy': track_audio['energy'],
        'Key': track_audio['key'],
        'Loudness': track_audio['loudness'],
        'Mode': track_audio['mode'],
        'Speechiness': track_audio['speechiness'],
        'Acousticness': track_audio['acousticness'],
        'Instrumentalness': track_audio['instrumentalness'],
        'Liveness': track_audio['liveness'],
        'Valence': track_audio['valence'],
        'Tempo': track_audio['tempo'],
        'Time Signature': track_audio['time_signature'],
        'Explicit': track['explicit'],
        'Popularity': track['popularity'],
        'Link': track['external_urls']['spotify']
    }
    for k, v in track_info.items():
        print(f'{k}: {v}')
    return track_info

def convertDuration(duration_milli: int):
    minutes, seconds = divmod(duration_milli / 1000, 60)
    minutes, seconds = int(minutes), int(seconds)
    return minutes, seconds

