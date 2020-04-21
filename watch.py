#! /usr/bin/env python3
from justwatch import JustWatch
import json
import requests
jw=JustWatch(country='IN')
source=jw.get_providers()
sourceN=len(source)
sourceL={
        8:"Netflix",
        125:"Hooq",
        119:"Amazon Prime Video",
        122:"Disney+ Hotstar",
        121:"Voot",
        158:"Viu",
        220:"JioCinema",
        232:"Zee5",
        218:"Eros Now",
        2:"iTunes",
        3:"Google Play",
        350:"Apple TV+",
        11:"MUBI",
        237:"Sony Liv",
        192:"YouTube",
        100:"GuideDoc",
        175:"Netflix Kids",
        73:"Tubi TV",
        124:"BookMyShow",
        255:"Yupp TV",
        309:"Sunn NXT",
        283:"Crunchyroll",
        315:"Hoichoi",
        319:"Alt-Balaji",
        377:"Disney+ Hotstar"
        }
offerType={
        "buy":"Buy",
        "rent":"Rent",
        "flatrate":"Stream",
        "free":"Free"
        }
imdb_key="b02ef8fd"
imdb_url="http://www.omdbapi.com/"
imdb_headers={
        "apikey":imdb_key
        }
#print(results)
q=input("Enter the name of the title you want to search for:\n")
results = jw.search_for_item(query=q)
totalR =int(results['total_results'])
print("Found {0} results:".format(totalR))
starline0="*"*75
if totalR < 10:
    print("Showing all results:")
    print(starline0)
    print("{:<8s}{:<50s}{:<8s}{:<5s}".format("Index", "Title", "Type", "Release Year"))
    print(starline0)    
    for i in range(totalR):
        itemTitle=results['items'][i]['title']
        itemType=results['items'][i]['object_type']
        itemYear=results['items'][i]['original_release_year']
        print("{:<8d}{:<50s}{:<8s}{:<5d}".format(i+1,itemTitle, itemType, itemYear))
else:
    print("Showing only the first 10 results:")
    print(starline0)
    print("{:<8s}{:<50s}{:<8s}{:<5s}".format("No.", "Title", "Type", "Release Year"))
    print(starline0)    
    for i in range(10):
        itemTitle=results['items'][i]['title']
        itemType=results['items'][i]['object_type']
        itemYear=results['items'][i]['original_release_year']
        print("{:<8d}{:<50s}{:<8s}{:<5d}".format(i+1,itemTitle, itemType, itemYear))
ind=int(input("Enter the index of the title you want to watch:\n"))
ind=ind-1
oLen=len(results['items'][ind]['offers'])
imdb_headers['t']=results['items'][ind]['title']
imdb_headers['y']=results['items'][ind]['original_release_year']
imdb=requests.get(imdb_url, params=imdb_headers)
#print(imdb, imdb.url)
imdb_j=imdb.json()
#print(imdb_j)
title=imdb_j['Title']
year=imdb_j['Year']
rating=imdb_j['Rated']
synopsis=imdb_j['Plot']
lang=imdb_j['Language']
cast=imdb_j['Actors']
tomatometer=imdb_j['Ratings'][1]['Value']
imdb_rate=imdb_j['imdbRating']
imdb_ratevote=imdb_j['imdbVotes']
content_type=imdb_j['Type']
print(f"\n\n{title}\n\nRelease Year: {year}\tMaturity Rating: {rating}\n\nLanguage:{lang}\n\n")
if content_type=="series":
    seasonN=imdb_j['totalSeasons']
    print(f"Number of Seasons: {seasonN}\n\n")
print(f"IMDb Rating: {imdb_rate} from {imdb_ratevote} votes.\n\n")
print(f"{synopsis}\n\n")
print("Found {0} offers. Displaying all.".format(oLen))
starline="*"*37
print(starline)
print("{:20}{:<10}{:<5}".format("Provider","Type","Quality"))
print(starline)
for i in range(oLen):
     monType=results['items'][ind]['offers'][i]['monetization_type']
     NmonType=offerType[monType]
     proID=results['items'][ind]['offers'][i]['provider_id']
     presType=results['items'][ind]['offers'][i]['presentation_type']
     #url=results['items'][ind]['offers'][i]['urls']['standard_web']
     NproID=sourceL[int(proID)]
     print("{:<20}{:<10}{:<5}".format(NproID, NmonType, presType))

