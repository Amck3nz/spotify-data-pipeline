import spotipy
import pandas as pd
import json
from  spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="b5e56ef517d9419ab9d6a924729ab879", client_secret="6c96dc75000045cbb760fe5fcc2d8421")

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF"

# splits url twice to get only the uri
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

sp_data = sp.playlist_tracks(playlist_URI)
#print data


#Extract Album Data
    #data['items'][0]['track']['album']['id']
def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_total_url = row['track']['album']['external_urls']['spotify']
        album_dict = {'album_id':album_id, "name":album_name, "release_date":album_release_date,
                          "total_tracks":album_total_tracks, "url": album_total_url}
        #print(album_element)
        album_list.append(album_dict)
    return album_list

def artist(data):
    artist_list = []
    for row in data['items']:
        for k,v in row.items():
            if k == "track":
                for artist in v['artists']:
                    #print(artist['name'])
                    artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    artist_list.append(artist_dict)
    return artist_list


def song(data):
    song_list=[]
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_dict = {'song_id': song_id, 'song_name': song_name, 'song_duration': song_duration, 'song_url': song_url,
                     'song_popularity':song_popularity, 'song_added': song_added, 'album_id': album_id, 'artist_id': artist_id}
        song_list.append(song_dict)
    return song_list


for data in sp_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = song(data)
        
        #Create Data Frames ------------------------------------------
        album_df = pd.DataFrame.from_dict(album_list)
        album_df = album_df.drop_duplicates(subset=['album_id'])
        
       
        artist_df = pd.DataFrame.from_dict(artist_list)
        artist_df = artist_df.drop_duplicates(subset=['artist_id'])
        
        song_df = pd.DataFrame.from_dict(song_list)
        
        #Transformations ------------------------------------------
        album_df['release_date'] = pd.to_datetime(album_df['release_date'])
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])