from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Artist, Song, Album, Playlist

# Register your models here.

class artistAdmin(admin.ModelAdmin):
    list_display = ['artistName', 'nationality','genre']
    search_fields = ['artistName', 'artistID']
    list_filter = ['nationality','genre']

class songAdmin(admin.ModelAdmin):
    list_display = ['songName', 'length', 'albumID', 'artistID']
    search_fields = ['songID','songName', 'albumID', 'artistID']
    list_filter = ['artistID','albumID']

class albumAdmin(admin.ModelAdmin):
    list_display = ['albumName', 'artistID']
    search_fields = ['albumID','albumName', 'albumID']
    list_filter = ['artistID']

class countSongInPlaylist(admin.ModelAdmin):
    list_display = ["playlistName","All_songs"]

    def All_songs(self, obj):
        return ", ".join([song.songName for song in obj.song.all()])

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email','date_joined', 'last_login')


admin.site.site_header = "4PM MUSIC ADMIN"

admin.site.unregister(User)

admin.site.register(User, MyUserAdmin)

admin.site.register(Artist, artistAdmin)

admin.site.register(Album, albumAdmin)

admin.site.register(Song, songAdmin)

admin.site.register(Playlist, countSongInPlaylist)
