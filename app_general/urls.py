from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('playlist/', views.createPlaylist, name='playlist'),
    path('playlist/<str:playlistID>', views.getPlaylist, name="getPlaylist"),
    path('artist/', views.getArtist, name='artist'),
    path('artist/<str:artistID>', views.getSpecificArtist, name="specificSong"),
    path('album/<str:album>', views.getAlbum, name='album'),
    path('song/', views.getSong, name='song'),
    path('song/<str:songFilter>', views.getSongFilter, name='songFilter'),
    path('search/', views.getSearch, name='search'),
    path('filter/<str:artistFilter>', views.getFilter, name='filter')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
