# This script is to get the Spotipy data from the Spotipy API
# and write it in a appropriate format to a CSV file

# Importing the libraries
import spotipy, json, csv
from secrets import *
from spotipy.oauth2 import SpotifyClientCredentials

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Playlist IDs
playlist_ids = [
    '75kU3tpSUe0Z487yLZ54kn?si=521c58145365425f', # liked songs
    '5XmE92oPSOfBf7v11zIVsW?si=07f9320cfbe24c5e' # unliked songs
]

# Audio features
feature_names = [
    'acousticness',
    'danceability',
    'duration_ms',
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'speechiness',
    'tempo',
    'time_signature',
    'valence'
]

# Function to get all the tracks of a playlist
def get_playlist_tracks(playlist_id):
    tracks_response = sp.playlist_items(playlist_id)['tracks']
    tracks = tracks_response['items']
    while tracks_response['next']:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response['items'])
    return tracks

# Function to get the features of a track
def get_features(track_id):
    features_response = sp.audio_features(track_id)
    features_json = json.dumps(features_response)
    features_data = json.loads(features_json)
    features_values = []
    for feature in feature_names:
        features_values.append(features_data[0][feature])
    return features_values

# Write data to CSV file
data_file = open('data.csv', 'w')
writer = csv.writer(data_file)

# Write the header
writer.writerow(['track_num', 'track_id', 'track_name', 'first_artist'] + feature_names + ['liked'])

print("Writing to the CSV file:")
print("#  Track")
print("----------------------------")

row_num = 1
for playlist_id in playlist_ids:
    tracks = get_playlist_tracks(playlist_id)
    for track in tracks:
        track_id = track['track']['id']
        track_name = track['track']['name']
        first_artist = track['track']['artists'][0]['name']
        features = get_features(track_id)
        try:
            if playlist_id == playlist_ids[0]:
                writer.writerow([row_num, track_id, track_name, first_artist] + features + [1])
            else:
                writer.writerow([row_num, track_id, track_name, first_artist] + features + [0])
            print(str(row_num) + ". " + track_name)
            row_num += 1
        except:
            print("error in csv writing")

print("\nFile is ready.")

# Closing the file
data_file.close()
