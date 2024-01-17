import pandas as pd
from task_connect_api import getTrack, getTrackAudio, getArtist

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
    # artists_cleaned = [{artist['name']:artist['id']} for artist in filtered_track['artists']]
    artists_names = [artist['name'] for artist in filtered_track['artists']]
    artists_id = [artist['id'] for artist in filtered_track['artists']]
    filtered_track['artists'] = artists_names
    filtered_track['artists_id'] = artists_id

    return filtered_track

# Item requests have superfluous info with nested tracks, and so they will be converted to new track{} schemas
def convertPlaylistItemsToTracks(playlist: dict):
    items = playlist['items'] # [{},{},{}]
    filtered_playlist = [filterItemToTrack(item) for item in items]
    return filtered_playlist

# Collect artist(s) genres without duplicates to one list
def organizeGenres(genre_set: set, track_genres: list, raw_genres: list):
    
    for genre in raw_genres:
        if genre not in genre_set:
            genre_set.add(genre)
            track_genres.append(genre)

# Cleans up track to have summarized parameters of interest
def cleanTrack(track: dict, bearer_token: str):
    track_filter_keys_secondPass = ['id', 'name', 'artists', 'artists_id', 'added_at', 'duration', 'duration_ms', 'explicit', 'popularity']
    # Genre compilation
    genre_set = set()
    # track_genres = []
    raw_genres = [getArtist(bearer_token, artist)['genres'] for artist in track['artists_id']]
    for genre_list in raw_genres:
        for genre in genre_list:
            if genre not in genre_set:
                genre_set.add(genre)
                # track_genres.append(genre)
    
    # O(2n) or O(n) space but lookup time for sets is basically O(1), worst case O(n) - O(n) for lists

    # Audio data compilation
    audio_filter_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    track_audio = getTrackAudio(bearer_token, track['id'])
    filtered_audio = {key: track_audio[key] for key in audio_filter_keys}
    filtered_track = {key: track[key] for key in track_filter_keys_secondPass}
    cleaned_track = {**filtered_track, **filtered_audio, 'genres': genre_set}
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

# For viewing the options available when filtering your playlist
def dispTrackFeatureOptions():
    features = {
        'Acousticness': {
            'desc': 'A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.',
            'range': [0,1]
        },
        'Danceability': {
            'desc': 'Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.',
            'range': [0,1]
        },
        'Energy': {
            'desc': 'Represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.',
            'range': [0,1]
        },
        'Instrumentalness': {
            'desc': 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.',
            'range': [0,1]
        },
        'Key': {
            'desc': 'The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.',
            'range': [-1,11]
        },
        'Liveness': {
            'desc': 'Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.',
            'range': [0,"No Upper End"]
        },
        'Loudness': {
            'desc': 'The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.',
            'range': [-60, 0]
        },
        'Mode': {
            'desc': 'Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.',
            'range': ['Either 0 for minor or 1 for major','n/a']
        },
        'Speechiness': {
            'desc': 'Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.',
            'range': [0,1]
        },
        'Tempo': {
            'desc': 'The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.',
            'range': ['No lower limit', 'No upper limit']
        },
        'Time Signature': {
            'desc': 'An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".',
            'range': [3,7]
        },
        'Valence': {
            'desc': 'A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).',
            'range': [0,1]
        },
        'Explicit': {
            'desc': 'Whether a track is explicit or not - only in booleans',
            'range': [True, False]
        },
        'Popularity': {
            'desc': 'How popular a track is currently',
            'range': [0,100]
        },
    }
    for key in features:
        desc = features[key]['desc']
        range_start = features[key]['range'][0]
        range_end = features[key]['range'][1]
        cleaned_print = f'{key}\n{desc}\nRange: {range_start} - {range_end}\n'
        print(cleaned_print)
    return

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