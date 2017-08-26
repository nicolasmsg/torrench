'''
LinuxTracker Module
'''

import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import sys

print("""
===========
|    LinuxTracker   |
===========
""")

mylist = []
masterlist = []
index_to_name = {}
index_to_dload = {}
category_name = {}
category_code = {}
categ_url_code = 9999
index = 0

'''
Function to fetch 'url' page and prepare soup
'''


def http_request(url):
    raw = requests.get(url)
    raw = raw.content
    soup = BeautifulSoup(raw, 'lxml')
    return soup


'''
Function to control displaying to distro categories.
If chosen to display categories, display_categories() is called.
Further category is chosen.
'''


def categs():
    opt = input("Display categories? [y/n]: ")
    categ_url_code = None
    if opt == 'y' or opt == 'Y':
        categ_len = display_categories()
        try:
            selected_categ = int(input("\nSelect category (0=none) : "))
            if selected_categ == 0:
                categ_url_code = 0
                print("category: none\n")
            elif selected_categ is not type(int):
                pass
            else:
                selected = category_name[selected_categ]
                categ_url_code = int(category_code[selected])
                print("Selected [%d] : %s " % (categ_url_code, selected))
        except ValueError:
            print("\nBad Input!")
            sys.exit(2)
        except KeyError:
            print("\nBad Input! Exiting...")
            sys.exit(2)
    else:
        categ_url_code = None

    return categ_url_code


'''
Function to display available categories called by categs()
'''


def display_categories():
    count = 1
    url = "http://linuxtracker.org/index.php?page=torrents"
    soup = http_request(url)
    categories = soup.find('select', {'name': 'category'}).find_all('option')
    categ_len = len(categories)
    for i in range(categ_len):
        categ_name = categories[i].string
        categ_code = categories[i]['value']
        print("[%d] %s" % (count, categ_name))
        category_name[count] = categ_name  # Mapping name with index number
        # Mapping name with category code
        category_code[categ_name] = categ_code
        count += 1
    return categ_len


'''
Function to fetch results for given 'title'
categ_url_code: the category code obtained from categs()
Each category is mapped to a code (integer)
Following details are fetched:
- name
- date
- size
- seeds
- leeches
- completed
- downloads
'''


def fetch_results(title, categ_url_code):
    print("Fetching results...")

    if categ_url_code == None:
        url = "http://linuxtracker.org/index.php?page=torrents&search=%s&active=1" % (
            title)
    else:
        url = "http://linuxtracker.org/index.php?page=torrents&search=%s&category=%d&active=1" % (
            title, categ_url_code)
    soup = http_request(url)
    content = soup.find_all('table', {'class': 'lista', 'width': '100%'})
    search_results = content[4]
    for i in search_results:
        try:
            name = i.font.a.string
            date = i.find_all('tr')[0].get_text().split(' ')[-2]
            size = i.find_all('tr')[1].td.find(
                recursive=False, text=True).replace(' ', '')
            seeds = i.find_all('tr')[2].get_text().split(' ')[-2]
            leeches = i.find_all('tr')[3].get_text().split(' ')[-2]
            completed = i.find_all('tr')[4].get_text().split(' ')[-3]
            dload = i.find_all('td', {'align': 'right'})[
                0].find_all('a')[1]['href']
            global index
            index += 1

            # Dictationary to map torrent name and download link with corresponding index (Used in select_torrent())
            index_to_name[str(index)] = name
            index_to_dload[str(index)] = dload

            # Storing each row result in mylist
            mylist = [name, "--" + str(index) + "--",
                      size, seeds, leeches, completed, date]
            # Further, appending mylist to a masterlist. This masterlist stores the required result
            masterlist.append(mylist)
        except AttributeError:
            pass
    if index == 0:
        print("\nNo results for give input!\n")
        sys.exit(2)

    output = tabulate(masterlist, headers=[
                      'NAME', 'INDEX', 'SIZE', 'S', 'L', 'C', 'ADDED ON', ], tablefmt="grid")
    return output


'''
Function to select torrent
Selected torrent's url is sent to download() for downloading torrent
'''


def select_torrent():
    print("\n\nTorrent can be downloaded directly through index\n\n")
    opt = 9999
    while(opt != 0):
        try:
            opt = int(input("(0 = exit)\nindex > "))
            if opt == 0:
                print("\nBye!")
                break
            else:
                print("\nSelected index[%s] - %s" %
                      (opt, index_to_name[str(opt)]))
                download("%s%s" %
                         ("http://linuxtracker.org/", index_to_dload[str(opt)]))
        except KeyError:
            print("\nBad Input!\n")
        except ValueError:
            print("\nBad Input!\n")


'''
Function to download torrent
Torrent is downloaded to ~/Downloads/torrench/ (.torrent file)
download url (dload_url) is obtained from select_torrent()
'''


def download(dload_url):

    home = os.path.expanduser(os.path.join('~', 'Downloads'))
    downloads_dir = os.path.join(home, 'torrench')
    soup = http_request(dload_url)
    link = soup.find_all(
        'td', {'align': 'center', 'class': 'blocklist'})[-1].a['href']
    torrent_name = link.split('&')[1].split('=')[1]

    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)

    with open(os.path.join(downloads_dir, torrent_name), "wb") as file:
        print("Downloading...")
        response = requests.get("%s%s" % ("http://linuxtracker.org/", link))
        file.write(response.content)
        print("Download complete!")
        print("\nSaved in %s \n" % (downloads_dir))


'''
Main execution begins here
'''


def main(title):
    try:
        code = categs()
        output = fetch_results(title, code)
        print("\nS=SEEDS; L=LEECHES; C=COMPLETED")
        print(output)
        select_torrent()
    except KeyboardInterrupt:
        print("\n\nAborted!")


if __name__ == "__main__":
    print("Its a module!")
