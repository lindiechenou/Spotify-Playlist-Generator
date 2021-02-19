from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
BILLBOARD = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = "Your_spotify_developer_id"
CLIENT_SECRET = "Your_spotify_developer_secret"
REDIRECT_URI = "http://example.com"

user_date = input("which date do you which? Please enter it in the format of YYYY-MM-DD. ")
link = f"{BILLBOARD}/{user_date}"

response = requests.get(link)
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")
songs = {}
title = []
artist = []
song_title = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_artist = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
for song in song_title:
    title.append(song.get_text())
for singer in song_artist:
    artist.append(singer.get_text())

for i in range(100):
    songs[i+1]=[title[i], artist[i]]

###GETTING ACCESS INTO SPOTIFY

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uri = []
year = user_date.split("-")[0]
for song in songs:
    try:
        result = sp.search(q=f"track:{songs[song][0]} year:{year}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        try:
            result = sp.search(q=f"track:{songs[song][0]} artist:{songs[song][1]}", type="track")
            uri = result["tracks"]["items"][0]["uri"]
            song_uri.append(uri)
        except IndexError:
            print(f"Sorry the song: {songs[song][0]} by {songs[song][1]} could not be added to the playlist")
# print(user_id)


######CREATE THE PLAYLIST FOR THE SONG

playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri)



