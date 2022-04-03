# Generated by Django 4.0.3 on 2022-03-28 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_general', '0004_song_songfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='genre',
            field=models.CharField(choices=[('Classical', 'Classical'), ('Pop', 'Pop'), ('Rock', 'Rock'), ('R&B', 'R&B'), ('Soul', 'Soul'), ('Electronic', 'Electronic'), ('Jazz', 'Jazz'), ('Blue', 'Blue'), ('Rap&Drill', 'Rap&Drill')], default='Pop', max_length=20),
        ),
        migrations.AlterField(
            model_name='song',
            name='albumID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_general.album'),
        ),
    ]