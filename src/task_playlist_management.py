import pandas as pd
from task_connect_api import getTrack, getTrackAudio

# Get rid of excess info from Spotify's default get-playlist-items response and refromat them to tracks
def filterItemToTrack(item: dict):
    # Parent items wanted from 'item' 
    added_at = item['added_at'].split('T')[0]
    raw_track = item['track']
    # Filtering and reconstructing item to track
    album_filter_keys = ['id', 'name', 'release_date']
    raw_track['album'] = {key: raw_track['album'][key] for key in album_filter_keys}
    track_filter_keys_firstPass = ['album', 'artists', 'duration_ms', 'explicit', 'external_urls', 'id', 'name', 'popularity']
    filtered_track = {key: raw_track[key] for key in track_filter_keys_firstPass}
    filtered_track['added_at'] = added_at # may be a bottleneck !!
    filtered_track['duration'] = convertDuration(filtered_track['duration_ms'])
    return filtered_track

# Item requests have superfluous info with nested tracks, and so they will be converted to new track{} schemas
def convertPlaylistItemsToTracks(playlist: dict):
    items = playlist['items'] # [{},{},{}]
    filtered_playlist = [filterItemToTrack(item) for item in items]
    return filtered_playlist

# Cleans up track to have summarized parameters of interest
def cleanTrack(track: dict, bearer_token: str):
    track_filter_keys_secondPass = ['id', 'name', 'added_at', 'duration', 'duration_ms', 'explicit', 'popularity']
    audio_filter_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    track_audio = getTrackAudio(bearer_token, track['id'])
    filtered_audio = {key: track_audio[key] for key in audio_filter_keys}
    filtered_track = {key: track[key] for key in track_filter_keys_secondPass}
    cleaned_track = {**filtered_track, **filtered_audio}
    return cleaned_track

# Prepare a list of dicts of cleaned tracks with wanted parameters for easy df conversion
def preparePlaylist(filtered_playlist: list, bearer_token: str):
    cleaned_playlist = [cleanTrack(track, bearer_token) for track in filtered_playlist]
    return cleaned_playlist

# Convert a list of dicts to a pandas df
def playlistToDataFrame(playlist: list):
    df = pd.DataFrame.from_dict(playlist)
    return df


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


'added_at', 
'name', 
'id',
'duration_ms', 
'explicit', 
'popularity',
'danceability', 
'energy', 
'key', 
'loudness', 
'mode', 
'speechiness', 
'acousticness', 
'instrumentalness', 
'liveness', 
'valence', 
'tempo', 
'time_signature'