import json
import urllib2
import re
        

def _get_haven_entities(args):
    response = urllib2.urlopen("https://api.havenondemand.com/1/api/sync/extractentities/v2?text={0}&entity_type=people_eng&entity_type=places_eng&entity_type=companies_eng&entity_type=organizations&entity_type=professions&entity_type=universities&entity_type=films&show_alternatives=false&apikey=9a3d7f45-9f85-4c49-809b-1691fce7fe1a".format(args))
    output = response.read()
    d = json.loads(output)
    for item in d["entities"]:
            if item["type"] == "people_eng":
                    print item["normalized_text"], item["additional_information"]

def _get_haven_tokens(plot):
    modified_text = plot.replace(' ', '+').replace(',', '%2C').replace('\n','+').strip()
    url = "http://api.havenondemand.com/1/api/sync/tokenizetext/v1?text={0}&stemming=false&apikey=9a3d7f45-9f85-4c49-809b-1691fce7fe1a".format(modified_text)
    print "url=", url                                        
    response = urllib2.urlopen(url)
    output = response.read()
    print output
    d = json.loads(output)
    for item in d["terms"]:
             print item["term"]


text = 'Washington: Barack Obama In an apparent dissatisfaction over Pak istan opposition to India becoming a member of the Nuclear Suppliers Gro up the US has said it is not about an arms race but about civilian use o f nuclear energy'
text = text.replace(' ' ,'+')
print text 
_get_haven_entities(text)
