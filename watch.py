#! /usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from justwatch import JustWatch
import time
import re

jw = JustWatch(country='IN')
source = jw.get_providers()
sourceN = len(source)
sourceL = {
    8: "Netflix",
    125: "Hooq",
    119: "Amazon Prime Video",
    122: "Disney+ Hotstar",
    121: "Voot",
    158: "Viu",
    220: "JioCinema",
    232: "Zee5",
    218: "Eros Now",
    2: "iTunes",
    3: "Google Play",
    350: "Apple TV+",
    11: "MUBI",
    237: "Sony Liv",
    192: "YouTube",
    100: "GuideDoc",
    175: "Netflix Kids",
    73: "Tubi TV",
    124: "BookMyShow",
    255: "Yupp TV",
    309: "Sunn NXT",
    283: "Crunchyroll",
    315: "Hoichoi",
    319: "Alt-Balaji",
    377: "Disney+ Hotstar"
}
offerType = {
    "buy": "Buy",
    "rent": "Rent",
    "flatrate": "Stream",
    "free": "Free"
}
imdb_key = "api key"
imdb_url = "http://www.omdbapi.com/"
imdb_headers = {
    "apikey": imdb_key
}
# print(results)
# q = input("Enter the name of the title you want to search for:\n")
q = str(input('Please enter what you want to search for:\n->'))
movie_title = ' '.join(word[0].upper() + word[1:] for word in q.split())
results = jw.search_for_item(query=q)
totalR = int(results['total_results'])
print("Found {0} results:".format(totalR))
starline0 = "*" * 75
if totalR < 10:
    print("Showing all results:")
    time.sleep(1)
    print(starline0)
    print("{:<8s}{:<50s}{:<8s}{:<5s}".format("Index", "Title", "Type", "Release Year"))
    print(starline0)
    for i in range(totalR):
        itemTitle = results['items'][i]['title']
        itemType = results['items'][i]['object_type']
        itemYear = results['items'][i]['original_release_year']
        print("{:<8d}{:<50s}{:<8s}{:<5d}".format(i + 1, itemTitle, itemType, itemYear))
else:
    print("Showing only the first 10 results:")
    time.sleep(0.5)
    print(starline0)
    print("{:<8s}{:<50s}{:<8s}{:<5s}".format("No.", "Title", "Type", "Release Year"))
    print(starline0)
    for i in range(10):
        itemTitle = results['items'][i]['title']
        itemType = results['items'][i]['object_type']
        itemYear = results['items'][i]['original_release_year']
        print("{:<8d}{:<50s}{:<8s}{:<5d}".format(i + 1, itemTitle, itemType, itemYear))
ind = int(input("Enter the index of the title you want to watch:\n->"))
ind = ind - 1
try:
    oLen = len(results['items'][ind]['offers'])
except:
    print("Sorry, the title you have entered is not being streamed or sold anywhere. You can try to search for it in our Torrents Section.")
    exit()
try:
    imdb_headers['t'] = results['items'][ind]['title']
    imdb_headers['y'] = results['items'][ind]['original_release_year']
    imdb = requests.get(imdb_url, params=imdb_headers)
    '''print("...")
    time.sleep(8)'''
    #print(imdb, imdb.url)

    #if imdb != "<Response [200]>":
    #   print("It looks like we cannot reach the servers at the moment, please check your internet connection or try again later. Thank you.")
    #   exit()
    imdb_j = imdb.json()
    # print(imdb_j)
    title = imdb_j['Title']
    year = imdb_j['Year']
    rating = imdb_j['Rated']
    synopsis = imdb_j['Plot']
    lang = imdb_j['Language']
    cast = imdb_j['Actors']
    #tomatometer = imdb_j['Ratings'][1]['Value']
    # Can't get Rotten Tomatoes to work, will try to update it in the future.
    imdb_rate = imdb_j['imdbRating']
    imdb_ratevote = imdb_j['imdbVotes']
    content_type = imdb_j['Type']
    print(f"\n\n{title}\n\nRelease Year: {year}\tMaturity Rating: {rating}\nLanguage: {lang}")
    if content_type == "series":
        seasonN = imdb_j['totalSeasons']
        print(f"Number of Seasons: {seasonN}")
    print(f"IMDb Rating: {imdb_rate} from {imdb_ratevote} votes.\n")
    print(f"{synopsis}")
except:
    print("We can't reach the IMDb servers, please check your internet connection or try again later")
    pass
print("\n\nFound {0} offers. Displaying all:\n".format(oLen))
starline = "*" * 37
print(starline)
print("{:20}{:<10}{:<5}".format("Provider", "Type", "Quality"))
print(starline)
for i in range(oLen):
    monType = results['items'][ind]['offers'][i]['monetization_type']
    NmonType = offerType[monType]
    proID = results['items'][ind]['offers'][i]['provider_id']
    presType = results['items'][ind]['offers'][i]['presentation_type']
    # url=results['items'][ind]['offers'][i]['urls']['standard_web']
    NproID = sourceL[int(proID)]
    print("{:<20}{:<10}{:<5}".format(NproID, NmonType, presType))

def get_ID():
    try:
       # imdb_key = "b02ef8fd"
       # imdb_url = "http://www.omdbapi.com/?"
        url = "http://www.omdbapi.com/"
        headers = {"t": 0, "apikey": imdb_key}
        headers["t"] = movie_title
        resp = requests.get(imdb_url, params=headers)
        json_ = resp.url, resp.json()
        id = json_[1]['imdbID']
        return id
    except:
        pass


def get_recommendations():
    try:
        url = f"https://www.imdb.com/title/{get_ID()}/"
        link = requests.get(url).text
        soup = BeautifulSoup(link, "html5lib")
        links = soup.find_all(class_='rec_item')
        recommend = []
        for i in range(0, 3):
            try:
                title = links[i]
                title = str(links[i])
                x = re.search(r'title=\"\w+\"', title)
                recommend_ = x.group(0)
                movie_recommended = recommend_.replace("title=", '')
                recommend.append(movie_recommended)
            except:
                pass
        for i in recommend:
            i = i.strip('\"')
            if len(recommend) > 2:
                return i, ',',
            else:
                return i
    except:
        pass


print(f'\nRecommendations: {get_recommendations()}')
