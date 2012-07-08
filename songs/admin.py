from django.contrib import admin
from songs.models import Chanson, Artiste, Playlist, Diffusion

class ChansonAdmin(admin.ModelAdmin):
    list_display = ('titre', 'artiste', 'has_youtubekey')
    list_filter = ['artiste']

class ArtisteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'count_chansons')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nom', 'count_chansons')

class DiffusionAdmin(admin.ModelAdmin):
    list_filter = ['diff_time']
    date_hierarchy = 'diff_time'

admin.site.register(Chanson, ChansonAdmin)
admin.site.register(Artiste, ArtisteAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Diffusion, DiffusionAdmin)
