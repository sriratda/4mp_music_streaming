import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from django.shortcuts import render

# Create your views here.
def artist(request):
    if request.method=='POST':
        # artist_uri = 'enter Spotify artist Uri '
        # spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        # results = spotify.artist_top_tracks(artist_uri)
        # final_result = results['tracks'][:5]
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="c3106edef16946d892fba1b3a1f7f55d", client_secret="471738f9dbe541229cd62b1a7a0d4f5e"))
        # results = sp.search(q='weezer', limit=20)
        # final_result = results['tracks']
        # for idx, track in enumerate(results['tracks']['items']):
        #     print(idx, track['name'])
        if len(sys.argv) > 1:
            name = ' '.join(sys.argv[1:])
        else:
            name = 'Radiohead'
        results = spotify.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            print(artist['name'], artist['images'][0]['url'])
        return render(request, 'app_music/base.html',context={'results':items})
    else:
        return render(request, 'app_music/base.html')