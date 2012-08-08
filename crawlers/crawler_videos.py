# -*- coding: utf-8 -*-
from BeautifulSoup import *
import urllib2, _mysql, time
import re

def sqlwrap(text):
  return "'"+text.replace('\'','\\\'').replace('"','\\"').replace('=','\\=').replace(';','\\;')+"'"

def crawlVideos(start_id):
    mainUrl = "http://www.youtube.com/results?search_query="
    db = db = _mysql.connect(host="localhost",user="root",passwd="root",db="nova_tracks",unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
    db.query("SELECT id,title,artist FROM tracks ORDER BY id")
    tracks = db.store_result()
    
    track_id=0
        
    while True:
        try:
            track = tracks.fetch_row()[0]
        except:
            return
        t1 = time.time()
        track_id, title, artist = track[0],track[1],track[2]

        if int(track_id)<start_id:
            continue

        print(title + " de " + artist)

        search_words = artist.split() + title.split()
        search_query = '+'.join(search_words).lower()

        # TO DO : Sanitize query...

        url = mainUrl + search_query
        print("Opening page " + url + "  ...")
        page = urllib2.urlopen(url,timeout=15)
        content = ''.join(page.readlines("utf8"))

        if len(re.findall('Aucune vid',content))>0:
            print("Aucune video trouvee")
            continue
        else:
            videos = re.findall('href="\/watch\?v=(.*?)[&;"]',content)
            track_video = videos[0]
            print("Video trouvee : http://www.youtube.com/watch?v=" + track_video)
            #sauvegarde en bdd
            query="UPDATE tracks SET video=%s WHERE id=%s" % (sqlwrap(track_video), track_id)
            db.query(query.encode("utf8"))

        t2 = time.time()
        print("Page processed in " + str(t2-t1) + "\n\n")

        
    return

if __name__ == "__main__":

    start_id = 1
    crawlVideos(start_id)



