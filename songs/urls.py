from django.conf.urls import patterns, include, url

urlpatterns = patterns('songs.views',
                       url(r'^$', 'latest'),
                       url(r'^(?P<chanson_id>\d+)/$', 'detail'),
                       url(r'^playlist/(?P<playlist_id>\d+)/$', 'playlist'),
)
