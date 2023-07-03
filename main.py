import streamlit as st
import json
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from requests import get, post
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from wordcloud import WordCloud


load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
scope ="playlist-read-private user-library-read user-top-read"

# authentication
credentials = SpotifyOAuth(client_id=client_id, 
                           client_secret=client_secret,
                           redirect_uri="https://www.google.com/",
                           scope=scope)

sp = spotipy.Spotify(auth_manager=credentials)
# auth field -> handles authentication if you have access token externally
# auth_manager field handles all authentication process for you. it handles access tokens and its expiration/refresh automatically

current_user = sp.current_user()
display_name = current_user['display_name']

print(f"{display_name}, your account has been authorized")

# getting playlists from current user
playlist = sp.current_user_playlists()
playlist_track = []
def getMyPlaylists():    
    for i in range(playlist['items']['total']):
        playlist_id = playlist['items'][i]['id']
        playlist_track.append(sp.playlist_tracks(playlist_id))
    print(playlist_track)

# getMyPlaylists()

# user's liked songs
def showLikedSongs():
    offset = 0
    i=0
    limit = 50  
    print("Liked songs: \n")
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        tracks = results['items']
        
        for item in tracks:
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            print(f"'{track_name}' by {artist_name}")
            i+=1
        
        if len(tracks) < limit: # Check if there are more tracks to retrieve
            break
        offset += limit
    print("No of liked songs: ", i)

# showLikedSongs()

# user's top 10 tracks
def getTopTracks():    
    top_tracks = sp.current_user_top_tracks(limit=10)
    # print(json.dumps(top_tracks, sort_keys=True, indent=4))
    for track in top_tracks['items']:
        artists = [artist['name'] for artist in track['artists']]
        song_name = track['name']
        print(f"'{song_name}' by {', '.join(artists)}")

# getTopTracks()





# searchQuery = input("Enter artist name:")
# # searchQuery = "naalayak"
# searchResults = sp.search(q=searchQuery, limit=1, offset=0, type="artist")

# # print(searchResults)
# # print(json.dumps(searchResults, sort_keys=True, indent=4))


# artist = searchResults['artists']['items'][0]

# artist_uri = artist['uri']
# artist_id = artist['id']

# user = sp.current_user()
# print(user)