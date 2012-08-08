from BeautifulSoup import *
import urllib2, _mysql, time
from datetime import datetime,timedelta

def sqlwrap(text):
  return "'"+text.replace('\\','\'').replace('\'','\\\'').replace('"','\\"')+"'"

def get_track_time(time, year, month, day,hour):
    [h,m] = time.split('H')
    [h,m] = [int(h),int(m)]
    
    d = datetime(year,month,day,h,m,0)
    
    #On gere le cas des pages a cheval sur 2 jours
    if hour in [0,1,2] and h in [22,23]:
        d = d - timedelta(days=1)
    
    return d.strftime("%Y-%m-%d %H:%M:%S")
    

def crawlNova(datetime_start, now):
    mainUrl = "http://www.novaplanet.com/cetaitquoicetitre/radionova/"
    step = 3600

    db = _mysql.connect(host="localhost",user="root",passwd="root",db="nova_tracks",unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
    curr_datetime = datetime_start
    

    while curr_datetime < now + step:
        t1=time.time()
        date = datetime.fromtimestamp(curr_datetime)
        year = date.year
        month = date.month
        hour = date.hour
        day = date.day

        print("Processing page "+ str(year)+"-"+str(month)+"-"+str(day)+ " : "+ str(date.hour)+":00 ("+str(curr_datetime)+")...")
        
        url = mainUrl + str(curr_datetime)
        
        tracks = tracks_scraper(url)

        if tracks == None:
          return curr_datetime

        #insertion en base de donnees

        query = "INSERT IGNORE INTO tracks (title, artist, first_time_played) VALUES "
        query += ",".join(["(%s,%s,%s)" % (sqlwrap(t["title"]),sqlwrap(t["artist"]),sqlwrap(get_track_time(t["datetime"],year,month,day,hour))) for t in tracks])
        db.query(query.encode("utf8"))

        result=db.store_result()
        for t in tracks:
            date = get_track_time(t["datetime"],year,month,day,hour)
            query="UPDATE tracks SET last_time_played=%s, nb_times_played=nb_times_played+1 WHERE title=%s AND artist=%s AND last_time_played<>%s " % (sqlwrap(date),sqlwrap(t["title"]),sqlwrap(t["artist"]),sqlwrap(date))
            db.query(query.encode("utf8"))

        t2=time.time()
        print("Page processed in %s seconds.\n" % str(t2-t1))
        curr_datetime += step
        
    db.close()
    
    return curr_date


def tracks_scraper(url):
    tracks = [{}]
    try:
      page = urllib2.urlopen(url,timeout=15)
    except Exception as e:
      print(e)
      return
    
    content = ''.join(page.readlines("utf8"))

    parsed_content = BeautifulSoup(content, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    tracks = [{"title":t.find("span",{"id":"titre"}).find(text=True).replace("\n",""), "artist":t.find("span",{"id":"artiste"}).find(text=True).replace("\n",""),"datetime":t.find("span",{"id":"date"}).find(text=True)} for t in parsed_content.findAll("div",{"class":"resultat"})]

    return tracks




if __name__ == "__main__":
    datetime_start = 1107097200 # 30 janvier 2005, 16h00
    now = time.time()
    
    while datetime_start < now:
      datetime_start = crawlNova(datetime_start, now)

    if date>=now:
        print("Ended successfully.")
    else:
        print("Error while crawling : crawl ended at " + str(date))
    
    
