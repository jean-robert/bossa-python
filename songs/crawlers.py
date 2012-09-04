from BeautifulSoup import *
import urllib2, time, re
from datetime import datetime, timedelta
from songs.models import *

def crawlNova(datetime_start, now):    
    from datetime import datetime, timedelta
    mainUrl = "http://www.novaplanet.com/cetaitquoicetitre/radionova/"
    step = 3600

    curr_datetime = datetime_start
    
    while curr_datetime < now + step:
        t1=time.time()
        
        url = mainUrl + str(curr_datetime)
        
        tracks = tracks_scraper(url)

        if tracks == None:
          return curr_datetime

        for t in tracks:
            try:
                a = Artiste.objects.get(nom=t["artist"])
            except Artiste.DoesNotExist:
                a = Artiste(nom=t["artist"])
                a.save()
                
            try:
                c = Chanson.objects.filter(artiste__id=a.id).get(titre=t["title"])
            except Chanson.DoesNotExist:
                c = Chanson(titre=t["title"], youtubekey='NA')
                c.artiste = a
                c.save()

            try:
                d = Diffusion.objects.filter(chanson__id=c.id).get(diff_time=datetime.fromtimestamp(float(t["divid"])))
            except Diffusion.DoesNotExist:
                d = Diffusion(diff_time=datetime.fromtimestamp(float(t["divid"])))
                d.chanson = c
                d.save()
                
        t2=time.time()
        print("Page processed in %s seconds.\n" % str(t2-t1))
        curr_datetime += step
    
    return curr_datetime

def tracks_scraper(url):
    tracks = [{}]
    try:
      page = urllib2.urlopen(url,timeout=15)
    except Exception as e:
      print(e)
      return
    
    content = ''.join(page.readlines("utf8"))

    parsed_content = BeautifulSoup(content, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tracks = [{"divid":t['id'], "title":t.find("span",{"id":"titre"}).find(text=True).replace("\n",""), "artist":t.find("span",{"id":"artiste"}).find(text=True).replace("\n",""),"datetime":t.find("span",{"id":"date"}).find(text=True)} for t in parsed_content.findAll("div",{"class":"resultat"})]

    return tracks

def update_songs():
    # datetime_start = 1107097200 # 30 janvier 2005, 16h00
    datetime_start =  time.mktime(Diffusion.objects.order_by('-diff_time')[0].diff_time.timetuple()) # latest diff recorded
    now = time.time()
    
    while datetime_start < now:
      datetime_start = crawlNova(datetime_start, now)

    if datetime_start>=now:
        print("Ended successfully.")
    else:
        print("Error while crawling : crawl ended at " + str(datetime_start))

    return True


def crawlVideos(track):
    mainUrl = "http://www.youtube.com/results?search_query="
    
    t1 = time.time()
    title, artist = track.titre, track.artiste.nom

    print("crawlVideo " + title + " de " + artist)

    search_words = artist.split() + title.split()
    search_query = '+'.join(search_words).lower()
    
# TO DO : Sanitize query...
    
    # regle les problemes d'encodage incompatible entre ascii et url
    url = mainUrl + search_query.encode('utf-8')
    #print("Opening page " + url + "  ...")
    page = urllib2.urlopen(url,timeout=15)
    content = ''.join(page.readlines("utf8"))
    
    if len(re.findall('Aucune vid',content))>0:
        print("Aucune video trouvee")        
    else:
        videos = re.findall('href="\/watch\?v=(.*?)[&;"]',content)
        print("Video trouvee : http://www.youtube.com/watch?v=" + videos[0])
            #sauvegarde en bdd
        track.youtubekey = videos[0]
        track.save()
                
    t2 = time.time()
    print("Page processed in " + str(t2-t1) + "\n\n")
        
    return

def update_videos():
    for t in Chanson.objects.filter(youtubekey='NA'):
        crawlVideos(t)

    return True


def update_playlist():
    # Mise a jour des 2 playlists principales
    # Dernieres 100 diffusions
    latest_diff_list = Diffusion.objects.all().order_by('-diff_time')[:100]
    p = Playlist.objects.get(pk=1)
    p.chansons.clear()
    for d in latest_diff_list:
        p.chansons.add(d.chanson)
    p.save()

    # Dernieres 100 nouveautes
    newest_songs_list = Chanson.objects.all().order_by('-id')[:100]
    p = Playlist.objects.get(pk=2)
    p.chansons.clear()
    for c in newest_songs_list:
        p.chansons.add(c)
    p.save()

    return True

