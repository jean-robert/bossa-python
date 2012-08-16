from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from songs.models import *
from songs.crawlers import *

def latest(request):
    latest_diff_list = Diffusion.objects.all().order_by('-diff_time')[:10]
    return render_to_response('songs/difflist.html',
                              {'diff_list': latest_diff_list,
                               'derniere_quoi': 'diffusions'})

def newest(request):
    newest_songs_list = Chanson.objects.all().order_by('-id')[:10]
    newest_diff_list = [s.diffusion_set.all().order_by('-diff_time')[0] for s in newest_songs_list]
    return render_to_response('songs/difflist.html',
                              {'diff_list': newest_diff_list,
                               'derniere_quoi': 'nouveautes'})

def detail(request, chanson_id):
    c = get_object_or_404(Chanson, pk=chanson_id)
    return render_to_response('songs/detail.html', {'c': c})


def playlist(request, playlist_id):
    p = get_object_or_404(Playlist, pk=playlist_id)
    return render_to_response('songs/playlist.html', {'p': p})

def update(request):
    update_songs()
    update_videos()
    return HttpResponse("Database updated")
