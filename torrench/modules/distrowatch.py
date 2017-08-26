'''
Modified for DistroWatch by Jesse Smith <jsmith@resonatingmedia.com>
'''

import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import colorama
import sys

print("""
===========
|    DistroWatch    |
===========
""")

colorama.init()
YELLOW = colorama.Fore.YELLOW + colorama.Style.BRIGHT
RESET = colorama.Style.RESET_ALL
urllist = []
index_to_name = {}

'''
Function to send HTTP GET request and obtain page source.
'''


def http_request(url):
    raw = requests.get(url)
    raw = raw.content
    soup = BeautifulSoup(raw, 'lxml')
    return soup


'''
Function to fetch results for given 'title'
soup is obtained from http_request()
'''


def fetch_results(soup, title):

    mylist = []
    masterlist = []
    torrent = soup.find_all('td', 'torrent')
    torrent_date = soup.find_all('td', 'torrentdate')
    index = 0
    for i, j in zip(torrent, torrent_date):
        try:
            link = i.find('a')
            url = "https://distrowatch.com/" + link.get('href')
            name = link.string
            name = name.lower()
            if title in name:
                date = j.string
                index += 1
                index_to_name[str(index)] = name
                mylist = [name, "--" + str(index) + "--", date]
                masterlist.append(mylist)
                urllist.append(url)
        except AttributeError:
            pass

    if index == 0:
        return 0

    output = tabulate(masterlist, headers=[
                      'NAME', 'INDEX', 'UPLOADED'], tablefmt="grid")
    return output


'''
Function to select torrent index and download torrent
download() is called, passing torrent's download url to it
'''


def post_result():

    print("\n\nTorrent can be downloaded directly through index\n")
    temp = 9999
    while(temp != 0):
        try:
            temp = int(input("(0 = exit)\nindex > "))
            if temp == 0:
                print("\nBye!")
                break
            else:
                selected_torrent = YELLOW + index_to_name[str(temp)] + RESET
                print("\nSelected index [%s] - %s" % (temp, selected_torrent))
                download(urllist[temp - 1])
        except ValueError:
            print("\nBad Input\n")
        except KeyError:
            print("\nBad Input\n")


'''
Function to download .torrent file. Torrent is downloaded in ~/Downloads/torrench/
'''


def download(dload_url):

    home = os.path.expanduser(os.path.join('~', 'Downloads'))
    downloads_dir = os.path.join(home, 'torrench')
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    torrent_name = dload_url.split('/')[5]

    with open(os.path.join(downloads_dir, torrent_name), "wb") as file:
        print("Downloading ", dload_url)
        response = requests.get(dload_url)
        file.write(response.content)
        print("Download complete!")
        print("\nSaved in %s \n" % (downloads_dir))


'''
Execution begins here.
'''


def main(title):

    try:
        url = "https://distrowatch.com/dwres.php?resource=bittorrent"
        soup = http_request(url)
        results = fetch_results(soup, title)
        if results == 0:
            print("\nNo results for give input!\n")
            sys.exit(2)
        else:
            print(results)
            post_result()
    except KeyboardInterrupt:
        print("\n\nAborted!")


if __name__ == "__main__":
    main("ubuntu")
