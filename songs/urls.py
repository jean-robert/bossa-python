from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# urlpatterns = patterns('songs.views',
#                        url(r'^$', 'latest'),
#                        url(r'^newest', 'newest'),
#                        url(r'^(?P<chanson_id>\d+)/$', 'detail'),
#                        url(r'^playlist/(?P<playlist_id>\d+)/$', 'playlist'),
#                        url(r'^update/$', 'update')
# )



urlpatterns = patterns('songs.views',
	(r'^$', TemplateView.as_view(template_name="songs/index.html")),
	url(r'^get_playlist$', 'get_playlist', name='get_playlist'),
	url(r'^get_song/(?P<chanson_id>\d+)/$', 'get_song', name='get_song'),
	url(r'^update/$', 'update', name='update'),
)



