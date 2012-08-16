from django.db import models
import datetime

class Artiste(models.Model):
    nom = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nom
    def count_chansons(self):
        return self.chanson_set.count()
    count_chansons.short_description = 'Nb de chansons'

class Chanson(models.Model):
    artiste = models.ForeignKey(Artiste)
    titre = models.CharField(max_length=200)
    youtubekey = models.CharField('YouTube key',max_length=200)
    def __unicode__(self):
        return self.titre
    def has_youtubekey(self):
        return self.youtubekey!='NA'
    has_youtubekey.boolean = True
    has_youtubekey.short_description = 'Has YouYube key?'
    def last_diff(self):
        return self.diffusion_set.all().order_by('-diff_time')[0].diff_time.strftime('%d/%m/%Y %H:%M')

class Diffusion(models.Model):
    chanson = models.ForeignKey(Chanson)
    diff_time = models.DateTimeField('heure diffusion')
    def __unicode__(self):
        return self.chanson.artiste.nom + ' - ' + self.chanson.titre + ' - ' + self.diff_time.strftime('%d/%m/%Y %H:%M')
    def viewdisplay(self):
        return self.chanson.artiste.nom + ' - ' + self.chanson.titre + ' - ' + self.diff_time.strftime('%d/%m/%Y %H:%M')

class Playlist(models.Model):
    nom = models.CharField(max_length=200)
    chansons = models.ManyToManyField(Chanson)
    def __unicode__(self):
        return self.nom
    def count_chansons(self):
        return self.chansons.count()
    count_chansons.short_description = 'Nb de chansons'

