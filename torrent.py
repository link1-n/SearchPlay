from bs4 import BeautifulSoup
import requests
from proxy_requests import ProxyRequests
import urllib.request

input_query = str(input('Please enter what you want to search for. '))
url1 = f'https://thepiratebay10.org/search/{input_query}/1/99/200'


def get_proxy():
    url = "https://free-proxy-list.net/"
    link = requests.get(url).text
    soup = BeautifulSoup(link, "html.parser")
    table = soup.find("table", id="proxylisttable").find("tbody")
    #global proxy_list
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


proxy = get_proxy()

for j in range(1, len(proxy) - 1):
    try:
        link = requests.get(url1, proxies=proxy[j]).text
        if link != '':
            soup = BeautifulSoup(link, 'lxml')
            print(f'Searching for {input_query}...')
            results = soup.find_all('div', class_='detName')
            i = 1
            result_video = []
            for i in results:
                result_video.append(i.text)
            #print(link)
            print('Showing results: \n')
            for i in range(0, 5):
                print(i+1,'.', result_video[i])

            show_more = str(input("Do you want to show more results? Type YES or NO."))
            if show_more == 'YES':
                for i in range(5, len(result_video)):
                    print(i + 1, '.', result_video[i])
            print("If you want to download then input the index of the result.")
            index = int(input('Enter index of the result: '))
            magnet_result = soup.find_all('a', title='Download this torrent using magnet')
            magnet_link = []
            for link in magnet_result:
                magnet_link.append(link['href'])
            download_link = magnet_link[index-1]
            print('--------------------------------------------------')
            print(f"Here is the selected magnet link.\n{download_link}")
            print('--------------------------------------------------')
            break

    except Exception as e:
        print('Trying to get a connection. Please wait.')




