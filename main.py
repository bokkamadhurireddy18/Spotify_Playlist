import requests
from bs4 import BeautifulSoup
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id= os.environ.get("spotify_client_id")
spotify_client_secret=os.environ.get("spotify_client_secret")
spotify_username=os.environ.get("spotify_username")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response= requests.get("https://www.billboard.com/charts/hot-100/"+date)
soup= BeautifulSoup(response.text, "html.parser")
song_tag = soup.select("li ul li h3")
song_list=[song.getText().strip() for song in song_tag]
#print(song_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username=spotify_username,
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify and printing playlist link
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

