import pandas as pd
from task_connect_api import getTrack, getTrackAudio


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

