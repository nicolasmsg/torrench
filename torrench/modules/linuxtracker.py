"""LinuxTracker Module."""

import sys
import logging
from utilities.Common import Common
import click


class LinuxTracker(Common):
    """
    LinuxTracker class.

    This class fetches results from
    linuxtracker.org and displays
    results in tabular form.
    Selected torrent is downloaded in hard-drive.
    Default download location is $HOME/downloads/torrench
    """

    def __init__(self, title):
        """Initialisations."""
        Common.__init__(self)
        self.title = title
        self.logger = logging.getLogger('log1')
        self.output_headers = ['NAME', 'INDEX', 'SIZE', 'S', 'L', 'COMPLETED', 'ADDED', ]
        self.categ_url = "http://linuxtracker.org/index.php?page=torrents"
        self.index = 0
        self.categ_url_code = 0
        self.mylist = []
        self.category_mapper = []
        self.category_mapper = []
        self.mapper = []
        self.url = "http://linuxtracker.org/index.php?page=torrents&search=%s&category=%d&active=1" % (
                        self.title, self.categ_url_code)

    def display_categories(self):
        """
        To display categories.

        If selected yes, simple torrent page is fetched
        to get category list.
        """
        self.logger.debug("Displaying categories")
        soup = self.http_request(self.categ_url)
        categories = soup.find('select', {'name': 'category'}).find_all('option')
        count = 0
        for i in range(len(categories)):
            name = str(categories[i].string)
            code = int(categories[i]['value'])
            # Map name with count (index) and code
            self.category_mapper.insert(count, (name, code))
            click.echo("[%d] %s" % (count, name))
            count += 1
        self.logger.debug("Total %d categories displayed" % (count))

    def select_category(self):
        """
        To select required category from displayed category list.

        Categories are associated with an index, and
        can be selected using that index. Each category has a Unique
        url code (hidden). The URL code is mapped with category index.
        """
        self.logger.debug("Select category")
        try:
            temp = click.prompt("\nSelect category (0=none) : ", type=int)
            self.logger.debug("selected index: %d" % (temp))
            if temp == 0:
                self.categ_url_code = 0
                click.echo("category: none\n")
            else:
                selected_category, self.categ_url_code = self.category_mapper[temp]
                click.echo("Selected [%d] : %s " % (temp, selected_category))
                self.logger.debug("Selected category %s ; index: %d" % (selected_category, temp))
                self.logger.debug("category_url_code: %d" % (self.categ_url_code))
        except (ValueError, KeyError, IndexError) as e:
            self.logger.exception(e)
            click.echo("\nBad Input!")
            sys.exit(2)

    def fetch_results(self):
        """To fetch results for given input."""
        click.echo("Fetching results...")
        self.logger.debug("Fetching...")
        masterlist = []
        self.logger.debug("categ_url_code = %d ; url=%s" % (self.categ_url_code, self.url))
        soup = self.http_request(self.url)
        content = soup.find_all('table', {'class': 'lista', 'width': '100%'})
        search_results = content[4]
        for i in search_results:
            try:
                name = i.font.a.string
                date = i.find_all('tr')[0].get_text().split(' ')[-2]
                size = i.find_all('tr')[1].td.find(recursive=False, text=True).replace(' ', '')
                seeds = i.find_all('tr')[2].get_text().split(' ')[-2]
                leeches = i.find_all('tr')[3].get_text().split(' ')[-2]
                completed = i.find_all('tr')[4].get_text().split(' ')[-3]
                dload = i.find_all('td', {'align': 'right'})[0].find_all('a')[1]['href']
                self.index += 1
                # Map torrent name and download link with corresponding index
                self.mapper.insert(self.index, (name, dload))
                self.mylist = [name, "--" + str(self.index) + "--", size, seeds, leeches, completed, date]
                masterlist.append(self.mylist)
            except AttributeError as e:
                self.logger.exception(e)
                pass
        if self.index == 0:
            click.echo("No results found for give input!")
            self.logger.debug("\nNo results found for given input! Exiting!")
            sys.exit(2)
        self.logger.debug("Results fetched successfully!")
        return masterlist

    def select_torrent(self):
        """
        To select required torrent.

        Each torrent is associated to an index value.
        Torrent is selected through that index.
        """
        click.echo("\nTorrent can be downloaded directly through index.")
        self.logger.debug("Selecting torrent...")
        temp = 9999
        while(temp != 0):
            try:
                temp = click.prompt("\n(0 = exit)\nindex > ", type=int)
                self.logger.debug("selected index %d" % (temp))
                if temp == 0:
                    click.echo("\nBye!")
                    self.logger.debug("Torrench quit!")
                    break
                elif temp < 0:
                    click.echo("\nBad Input\n")
                    continue
                else:
                    selected_index, dload = self.mapper[temp-1]
                    self.logger.debug("selected torrent: %s ; index: %d" % (selected_index, temp))
                    click.echo("\nSelected index[%s] - %s" % (temp, click.style(selected_index, fg="yellow")))
                    self.get_torrent("http://linuxtracker.org/"+dload)
            except (ValueError, IndexError, KeyError) as e:
                click.echo("\nBad Input\n")
                self.logger.exception(e)

    def get_torrent(self, url):
        """
        To get download URL.

        Download url is obtained. This URL is then
        served to download() for downloading (.torrent) file.
        """
        try:
            self.logger.debug("getting torrent download url")
            soup = self.http_request(url)
            link = soup.find_all('td', {'align': 'center', 'class': 'blocklist'})[-1].a['href']
            torrent_name = link.split('&')[1].split('=')[1]
            dload_url = "http://linuxtracker.org/" + link
            self.logger.debug("torrent dload url: %s" % (url))
            self.download(dload_url, torrent_name)
        except Exception as e:
            self.logger.exception(e)
            click.echo("Error message: %s" %(e))
            click.echo("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)

def main(title):
    """Execution begins here."""
    try:
        click.echo("\n[LinuxTracker]\n")
        ltr = LinuxTracker(title)
        if click.confirm("Display categories? : ")
            ltr.logger.debug("Display categories: %c" % (temp))
            ltr.display_categories()
            ltr.select_category()
        else:
            ltr.categ_url_code = 0
            ltr.logger.debug("Not displaying categories.")
        masterlist = ltr.fetch_results()
        ltr.show_output(masterlist, ltr.output_headers)
        ltr.select_torrent()
    except KeyboardInterrupt:
        ltr.logger.debug("Keyboard interupt! Exiting!")
        click.echo("\n\nAborted!")


if __name__ == "__main__":
    print("Its a module!")
