import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify credentials
client_id = "96ce87edae0949aaaeec8e5b82678a3d"
client_secret = "0cf5e905b5024144a7e58c1062590571"
redirect_uri = "http://localhost:8080" # this has to match uri in spotify developer dashboard
scope = "user-modify-playback-state" # this scope allows us to play music and control playback


# Use the SpotifyOAuth object to authenticate with the Spotify API
spotify_oauth = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope)

# # Get the access token from the authentication manager
# access_token = spotify_oauth.get_access_token()

# Create a spotipy object with the authentication manager
sp = spotipy.Spotify(client_credentials_manager=spotify_oauth)

results = sp.search(q="kiss prince", type="track")

track = results["tracks"]["items"][0]

uri = track["uri"]
url = track["external_urls"]["spotify"]


# play the song
sp.start_playback(uris=[uri])




