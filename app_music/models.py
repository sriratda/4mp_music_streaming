from distutils.command.upload import upload
from distutils.text_file import TextFile
from django.db import models
from django.forms import CharField, IntegerField

# Create your models here.

# class Song(models.Model):
#     songID = CharField(max_length=5),
#     albumID = CharField(max_length=5),
#     title = CharField(max_length=40),
#     duration = IntegerField(),
#     description = CharField(50)

class Artist(models.Model):
    artistID = models.CharField(max_length=10, primary_key=True)
    artName = models.CharField(max_length=50)
    nationality = models.CharField(max_length=20)
    genre = models.CharField(max_length=10)
    picture = models.ImageField(null=True, blank=True, upload_to="artistIMG/")
    description = models.TextField(null=True)