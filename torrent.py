#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
from tabulate import tabulate
import pyperclip

#on linux, pyperclip will work when
#either xsel or xclip are installed
#do "sudo apt-get install xsel" you can replace xsel with xclip
#if it still doesn't work, go to the link below
# https://pyperclip.readthedocs.io/en/latest/introduction.html#not-implemented-error

#from movie import input_query_
import time

input_query = str(input('Please enter what you want to search for:\n->'))
# input_query = str(input('Please enter what you want to search for. '))
movie_title = ' '.join(word[0].upper() + word[1:] for word in input_query.split())


def query():
    # noinspection PyGlobalUndefined
    return input_query


def get_ID():
    try:
        imdb_key = "b02ef8fd"
        imdb_url = "http://www.omdbapi.com/?"
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


def get_proxy():
    url = "https://free-proxy-list.net/"
    link = requests.get(url).text
    soup = BeautifulSoup(link, "html.parser")
    table = soup.find("table", id="proxylisttable").find("tbody")
    proxy_list = []
    proxy_https = []
    for row in table.find_all("tr"):
        proxy_data = row.find_all("td")
        proxy_ip = proxy_data[0].text
        proxy_http = 'http'
        proxy_list.append(proxy_ip)
        proxy_https.append(proxy_http)

    proxy_list = [{'http': p} for p in proxy_list]
    return proxy_list


# noinspection PyBroadException
def get_magnet():
    proxy = get_proxy()
    url1 = f'https://thepiratebay10.org/search/{input_query}/1/99/200'
    size = []
    seeds = []
    seeders = []
    leechers = []
    seeds_error = 0
    for j in range(1, len(proxy) - 1):
        try:
            link = requests.get(url1, proxies=proxy[j]).text
            if link != '':
                soup = BeautifulSoup(link, 'lxml')
                for tr in soup.find_all("tr"):
                    text = tr.find_all("td", {'align': 'right', 'valign': None})
                    seeds.append(text)
                seeds.pop(0)
                seeds.pop(-1)
                for i in seeds:
                    try:
                        i = str(i)
                        clean_ = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                        seeds_ = re.sub(clean_, '', i)
                        seeder_search = re.search(r'\d+', seeds_)
                        leecher_search = re.search(r'\s\d+', seeds_)
                        seeder = seeder_search.group(0)
                        leecher = leecher_search.group(0).strip()
                        seeders.append(int(seeder))
                        leechers.append(int(leecher))

                    except:
                        seeds_error += 1

                size_ = soup.find_all("font", class_="detDesc")
                print(f'Searching for {input_query}...')
                time.sleep(1)
                results = soup.find_all('div', class_='detName')
                for x in size_:
                    size.append(str(x))
                info = []
                for i in size:
                    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                    x = re.sub(clean, '', i)
                    info.append(x)

                result_video = []
                for i in results:
                    result_video.append(i.text)
                date = []
                size1 = []
                date_error = 0
                size_error = 0

                for i in info:
                    try:
                        match_date = re.search(r'\d{2}-\d{2}\s\d{4}', i)
                        if match_date:
                            date_ = datetime.datetime.strptime(match_date.group(), '%m-%d %Y').date()
                            date.append(date_)
                        else:
                            date.append('')
                    except:
                        date_error += 1

                    try:
                        match_size = re.search(r'\d+.\d+\s[M|G]+iB', i)
                        if match_size:
                            size1.append(match_size.group(0))
                        else:
                            size1.append('')
                    except:
                        size_error += 1

                df = pd.DataFrame()
                ltitle, ldate, lsize, lseeder, lleecher = len(result_video), len(date), len(size1), len(seeders), len(
                    leechers)
                max_len = max(ltitle, ldate, lsize, lseeder, lleecher)
                if not max_len == ltitle:
                    result_video.extend(['-'] * (max_len - ltitle))
                if not max_len == ldate:
                    date.extend(['-'] * (max_len - ldate))
                if not max_len == lsize:
                    size1.extend(['-'] * (max_len - lsize))
                if not max_len == lseeder:
                    seeders.extend(['-'] * (max_len - lseeder))
                if not max_len == lleecher:
                    leechers.extend(['-'] * (max_len - lleecher))
                df['Title'] = result_video
                df['Date'] = date
                df['Size'] = size1
                df['Seeders'] = seeders
                df['Leechers'] = leechers
                df.index = df.index + 1

                print('\nShowing results: \n')
                time.sleep(1)
                print(tabulate(df.head(10), headers='keys', tablefmt='fancy_grid'))
                '''show_more = str(input("Do you want to show more results? Type YES or NO."))
                if show_more == 'YES' or 'yes':
                    print(tabulate(df, headers='keys', tablefmt='psql'))
                if show_more == 'NO' or 'no':
                    print('')'''
                print("If you want to download then input the index of the result.")
                index = int(input('Enter index of the result: '))

                name_movie = df['Title'].iloc[index - 1]
                size_movie = df['Size'].iloc[index - 1]
                magnet_result = soup.find_all('a', title='Download this torrent using magnet')
                magnet_link = []
                for link in magnet_result:
                    magnet_link.append(link['href'])
                download_link = magnet_link[index]

                print(f'\nYour selected movie: {name_movie}Size: {size_movie}')
                time.sleep(1)
                print(f"Here is the selected magnet link.\n{download_link}")
                pyperclip.copy(download_link)
                time.sleep(1)
                print("Magnet link has been copied to your clipboard.\n")
                print(f'Recommendations: {get_recommendations()}')
                break

        except Exception:
            print('Trying to get a connection. Please wait.')


get_magnet()

