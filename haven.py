import json
import urllib2
import re
import sqlite3
conn = sqlite3.connect('movel_da.db')
cus = conn.cursor()

cus.execute('''CREATE TABLE movel_phrases(id text,phrase text,url text,entity text)''')
cus.execute('''CREATE TABLE movel_headlines(headline text,id text)''')

import hashlib
m = hashlib.md5()



def _get_haven_entities(args):
    url  = "https://api.havenondemand.com/1/api/sync/extractentities/v2?text={0}&entity_type=people_eng&entity_type=places_eng&entity_type=companies_eng&entity_type=organizations&entity_type=professions&entity_type=universities&entity_type=films&show_alternatives=false&apikey=9a3d7f45-9f85-4c49-809b-1691fce7fe1a".format(args)
    response = urllib2.urlopen(url)
    output = response.read()
    d = json.loads(output)
    for item in d["entities"]:
        for m in item["matches"]:
            l = m['original_length']
            ofs = m['offset']
            print args[ofs:ofs+l], " ",ofs, " " , ofs+l
            if('image' in item['additional_information']):
                img_links[ofs+l] =item['additional_information']['image']
            offsets.append(ofs)
            offsets.append(ofs+l)            
    printing_phrases(args)

def printing_phrases(args):
    tmp1=tmp2=tmp3=''
    offsets.sort()
    s=0
    length = len(offsets)
    for i in range(1,length):
        if(i%2==1):
            tmp1 = args[s:offsets[i]]
            print tmp1,"...IMG:",
            if(offsets[i] in img_links):
                tmp2  = img_links[offsets[i]]
                print  tmp2,"..end..\n\n"
            tmp3 = args[offsets[i-1]:offsets[i]]
            tmp1 =tmp1.replace("+"," ")
            tmp2 =tmp2.replace("+"," ")
            tmp3 =tmp3.replace("+"," ")
            cus.execute("INSERT INTO movel_phrases VALUES(?,?,?,?)",(gid,tmp1,tmp2,tmp3))
            s = offsets[i]
    conn.commit()


with open('/home/user/rbharti/news_training/hackathon/test.py') as data_file:    
    data = json.load(data_file)

for headline,text in data.iteritems():
    gid=''
    offsets =[]
    img_links={}
    m.update(headline)
    gid=m.hexdigest()
    cus.execute("INSERT INTO movel_headlines VALUES(?,?)",(headline,gid))
    _get_haven_entities(text.replace(" ", "+"))
    print "here\n"
conn.close()
