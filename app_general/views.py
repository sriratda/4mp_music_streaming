from random import shuffle
from unittest import result
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import json
import os
# path = os.path.dirname(os.path.abspath(__file__))
# path_file = path+'\\static\\app_general\\artistDetail.json'
# print(path_file)

# def getArtist(request):
#     file = open(path_file,'r',encoding='utf-8')
#     artistDetail = json.load(file)
#     name = 'Tattoo Colour'
#     artist_filter = [x for x in artistDetail if x['name'] == name]
#     return render(request, 'app_general/artistDetail.html', {'artist':artist_filter})

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            if User.objects.filter(username=username):
                messages.error(request, "Wrong Password")
            else:
                messages.error(request, "Username doesn't existed")
    
    return render(request, 'app_general/login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['con-password']
        status = True
        if User.objects.filter(username=username):
            messages.error(request, "This username is already existed.")
            status = False
            
        if User.objects.filter(email=email):
            messages.error(request, "This email is already existed.")
            status = False

        if password1 != password2:
            messages.error(request, "Password isn't match.")
            status = False

        if username.isalnum() == False or len(username) < 4:
            messages.error(request, "Username must have more than 4 characters and be alphanumeric.")
            status = False

        if len(password1) < 6:
            messages.error(request, "Password should be more than 6 characters.")
            status = False

        if status == True:   
            myuser = User.objects.create_user(username, email, password1)
            myuser.save()
            messages.success(request, "Your account has been successfully created.")
            return redirect('login')
    return render(request, 'app_general/register.html')

def createPlaylist(request):
    user = request.user
    myPlaylist = None
    if request.method == 'POST':
        playlistName = request.POST['playlistName']
        # checkName = Playlist.objects.filter(playlistName=playlistName).exists()
        # if checkName:
        #     messages.error(request, "This playlist is already existed.")
        #     return redirect('playlist')
        # else:
        # print(playlistName+' Add')
        playlist = Playlist(userID=user, playlistName=playlistName)
        playlist.save()
        return redirect('playlist')
    else:
        myPlaylist = Playlist.objects.filter(userID=user)
    
    if request.method == 'GET':
        playlistID = request.GET.get('playlistID')
        if playlistID:
            try:
                Playlist.objects.filter(id=playlistID).delete()
            except:
                print('Error')
            else:
                print(playlistID)
    return render(request, 'app_general/playlist.html', {'myPlaylist':myPlaylist})

def getSong(request):
    user = request.user
    all_songs = Song.objects.all().order_by('?')
    all_playList = None
    # print(len(all_songs))
    if user.is_authenticated:
        # print(user)
        all_playList = Playlist.objects.filter(userID=user)
    if request.method == 'POST':
        selected = request.POST.get('selected',False)
        selected_split = selected.split(',')
        selected_playlist = Playlist.objects.get(id=selected_split[0])
        selected_song = Song.objects.get(songID=selected_split[1])
        song_exists = selected_playlist.song.filter(songID=selected_song.songID).exists()
        if not song_exists:
            # messages.error(request, "This song is already in the playlist")
            # return redirect('song')
        # if selected_playlist.song.
            try:
                selected_playlist.song.add(selected_song)
            except:
                print(selected_playlist,selected_song)
            else:
                print('Add song to playist SUCCESS')

    genres = Artist.genre.field.choices
    allGenre = []
    for genre in genres:
        allGenre.append(genre[0])

    return render(request, 'app_general/song.html', {'songs': all_songs, 'all_playList': all_playList,'numberofSong':all_songs.count(),'genres':allGenre})


def getSpecificArtist(request, artistID=None):
    user = request.user
    artistName = Artist.objects.get(artistID=artistID)
    specific = Song.objects.filter(artistID=artistID).order_by('?')

    # if song_genre == "POP" or song_genre == "R&B":
    addRecom = list(Artist.objects.filter(genre="POP").exclude(artistID=artistID).order_by('?')[:3])
    # recommendedArtist+=addRecom
    # addRecom = list(Artist.objects.filter(genre="R&B").exclude(artistID=artistID))
    # recommendedArtist+=addRecom

    relateAlbum = Album.objects.filter(artistID=artistID).order_by('?')

    all_playList = None
    if user.is_authenticated:
        print(user)
        all_playList = Playlist.objects.filter(userID=user)
    if request.method == 'POST':
        selected = request.POST.get('selected',False)
        print(selected)
        selected_split = selected.split(',')
        selected_playlist = Playlist.objects.get(id=selected_split[0])
        selected_song = Song.objects.get(songID=selected_split[1])
        song_exists = selected_playlist.song.filter(songID=selected_song.songID).exists()
        if not song_exists:
            # messages.error(request, "This song is already in the playlist")
            # return redirect('song')
        # if selected_playlist.song.
            try:
                
                selected_playlist.song.add(selected_song)
            except:
                print(selected_playlist,selected_song)
            else:
                print('Add song to playist SUCCESS') 
    
    return render(request, 'app_general/SpeArtist.html', {'artists':specific, 'artistName':artistName, 'resultRecom': addRecom, 'relates':relateAlbum, 'all_playList':all_playList})


def getArtist(request):
    artists = Artist.objects.all().order_by('?')
    genres = Artist.genre.field.choices
    allGenre = []
    for genre in genres:
        allGenre.append(genre[0])
    return render(request, 'app_general/artist.html', {'artists': artists, 'numberOfArtist':artists.count(), 'allGenre':allGenre})


def getAlbum(request, album=None):
    user = request.user
    albumName = Album.objects.get(albumID=album)
    albumSongs = Song.objects.filter(albumID=album)

    exeptAlbum = albumName.artistID

    relateAlbum = Album.objects.filter(artistID=exeptAlbum).exclude(albumID=album).order_by('?')[:3]

    moreArtist = Artist.objects.all().order_by('?')[:3]
    all_playlist = None
    if user.is_authenticated:
        all_playlist = Playlist.objects.filter(userID=user)
    if request.method == 'POST':
        selected = request.POST.get('selected',False)
        selected_split = selected.split(',')
        selected_playlist = Playlist.objects.get(id=selected_split[0])
        selected_song = Song.objects.get(songID=selected_split[1])
        song_exists = selected_playlist.song.filter(songID=selected_song.songID).exists()
        if not song_exists:
            # messages.error(request, "This song is already in the playlist")
            # return redirect('song')
        # if selected_playlist.song.
            try:
                selected_playlist.song.add(selected_song)
            except:
                print(selected_playlist,selected_song)
            else:
                print('Add song to playist SUCCESS')
    return render(request, 'app_general/album.html', {'albumSongs':albumSongs, 'albumName':albumName, 'relateAlbum':relateAlbum, 'moreArtist':moreArtist, 'all_playList':all_playlist})


# def getRecommendedArtist(request):
#     randomArtist = Artist.objects.all().order_by('?')[:3]
#     rand = list(randomArtist)
#     shuffle(rand)
#     return render(request, 'app_general/recommendedArtist.html', {'recoms': randomArtist})


# def getSpecificArtist(request, artist=None):
#     Sartist = Artist.objects.filter(artistID=artist)
#     print(Sartist)
#     return render(request, 'app_general/SpeArtist.html', {'artist':Sartist})


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    randomArtist = Artist.objects.all().order_by('?')[:3]
    rand = list(randomArtist)
    shuffle(rand)
    categoriesSong = getTopsongs()
    first_five = dict(list(categoriesSong.items())[:5])
    last_five = dict(list(categoriesSong.items())[-1:len(categoriesSong)-50:-1])
    hitSong = []
    notHit = []
    for i in first_five:
        hitSong.append(Song.objects.get(songID=i))
    for i in last_five:
        notHit.append(Song.objects.get(songID=i))
    shuffle(notHit)
    recommend_song = zip(hitSong,notHit[:5])
    return render(request, 'app_general/home.html', {'random':rand, 'recommend_song':recommend_song})

def getPlaylist(request, playlistID=None):
    # user = request.user
    myPlaylist = Playlist.objects.get(id=playlistID)
    songs = myPlaylist.song.all()
    if request.method == 'POST':
        delete_songID = None
        try:
            songID = request.POST['songID']
            delete_songID = myPlaylist.song.get(songID=songID)
        except:
            print('Error')
            
        # print(delete_songID)
        if delete_songID:
            try:
                myPlaylist.song.remove(delete_songID)
            except:
                print('Delete Song has something wrong.')
    return render(request, 'app_general/playlistdetail.html', {'myPlaylist':myPlaylist, 'songs':songs})

def getSearch(request):
    if request.method == 'POST':
        found_status = True
        search = request.POST['search']
        allSongs = Song.objects.all()
        allArtists = Artist.objects.all()
        allAlbums = Album.objects.all()

        songsFound = allSongs.filter(songName__icontains=search)
        artistFound = allArtists.filter(artistName__icontains=search)
        albumFound = allAlbums.filter(albumName__icontains=search)
        if not songsFound and not artistFound and not albumFound:
            found_status = False

    return render(request, 'app_general/search.html', {'songFound': songsFound, 'artistFound': artistFound, 'albumFound': albumFound, 'search':search, 'found_status':found_status})

def getTopsongs():
    numberOfsong_in_playlist = {}
    all_song = Song.objects.all()
    all_playlist = Playlist.objects.all()
    for song in all_song:
        numberOfsong_in_playlist[song.songID] = 0
    for playlist in all_playlist:
        songInplaylist = playlist.song.all()
        for song in songInplaylist:
            numberOfsong_in_playlist[song.songID] += 1
    numberOfsong_in_playlist = dict(sorted(numberOfsong_in_playlist.items(),key=lambda x:x[1],reverse=True))
    return numberOfsong_in_playlist
    # print(numberOfsong_in_playlist)

def getFilter(request, artistFilter):
    artistGenre = Artist.objects.filter(genre=artistFilter).order_by('?')
    genres = Artist.genre.field.choices
    allGenre = []
    for genre in genres:
        allGenre.append(genre[0])
    return render(request, 'app_general/filter.html', {'artistGenre':artistGenre, 'genres':allGenre, 'numberOfArtist':artistGenre.count(), 'nameFilter': artistFilter})

def getSongFilter(request, songFilter):
    user = request.user
    filterSong = Song.objects.filter(artistID__genre=songFilter)
    genres = Artist.genre.field.choices
    all_playList = None
    if user.is_authenticated:
        # print(user)
        all_playList = Playlist.objects.filter(userID=user)
    if request.method == 'POST':
        selected = request.POST.get('selected',False)
        selected_split = selected.split(',')
        selected_playlist = Playlist.objects.get(id=selected_split[0])
        selected_song = Song.objects.get(songID=selected_split[1])
        song_exists = selected_playlist.song.filter(songID=selected_song.songID).exists()
        if not song_exists:
            # messages.error(request, "This song is already in the playlist")
            # return redirect('song')
        # if selected_playlist.song.
            try:
                selected_playlist.song.add(selected_song)
            except:
                print(selected_playlist,selected_song)
            else:
                print('Add song to playist SUCCESS')

    allGenre = []
    for genre in genres:
        allGenre.append(genre[0])
    return render(request, 'app_general/songFilter.html',{'filterSong':filterSong,'genres':allGenre, 'numberOfSong':filterSong.count(), 'genre':songFilter, 'all_playList': all_playList})