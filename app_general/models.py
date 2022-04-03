from distutils.command.upload import upload
from random import choices
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

genre = (
    ('Classical','Classical'),
    ('Pop','Pop'),
    ('Rock','Rock'),
    ('R&B','R&B'),
    ('Soul','Soul'),
    ('Electronic','Electronic'),
    ('Jazz','Jazz'),
    ('Blue','Blue'),
    ('Rap','Rap'),
    ('trip hop&lo-fi','trip hop&lo-fi'),
)

class Artist(models.Model):
    artistID = models.CharField(max_length=10, primary_key=True)
    artistName = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    description = models.TextField(default=None, null=True,blank=True)
    picture = models.ImageField(blank=True,default=None,null=True)
    genre = models.CharField(choices=genre, max_length=20, default="Pop")
    
    def __str__(self):
        return self.artistName

class Album(models.Model):
    albumID = models.CharField(max_length = 10, primary_key = True)
    albumName = models.CharField(max_length=50)
    artistID = models.ForeignKey(Artist, on_delete=models.CASCADE)
    releaseDate = models.DateField(auto_now_add=True)
    description = models.TextField(default=None, null=True, blank=True)
    picture = models.ImageField(upload_to="album/",blank=True,default=None,null=True)
    
    def __str__(self):
        return self.albumName

class Song(models.Model):
    artistID = models.ForeignKey(Artist, on_delete=models.CASCADE)
    albumID = models.ForeignKey(Album, on_delete=models.CASCADE, default=None,blank=True)
    songID = models.CharField(max_length=10)
    songName = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10,decimal_places=2)
    songFile = models.FileField(upload_to="audio/", blank=True, default=None)
    # AlbumName = models.CharField(max_length=50)

    def __str__(self):
        return self.songName

class Playlist(models.Model):
    playlistName = models.CharField(max_length=50, default="New Playlist")
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)

    def __str__(self):
        return self.playlistName



