import pandas as pd
from task_connect_api import getTrack, getTrackAudio

def dispTrackInfo(track_id: str):
    track = getTrack(track_id)
    # Collect list in case there are multiple artists
    artists = []
    for artist in track['artists']:
        artists.append(artist['name'])
    # Converting millisecond durations to minutes and seconds
    minutes, seconds = convertDuration(track['duration'])
    duration = f'{minutes}:{seconds}'
    track_audio = getTrackAudio(track_id)
    track_info = {
        'Track': track['name'],
        'Artist': artists,
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
    return track_info

def convertDuration(duration_milli: int):
    minutes, seconds = divmod(duration_milli / 1000, 60)
    return minutes, seconds