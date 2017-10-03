"""Modified for DistroWatch by Jesse Smith <jsmith@resonatingmedia.com>."""

import sys
import logging
from torrench.utilities.common import Common
import click


class DistroWatch(Common):
    """
    Distrowatch class.

    This class fetches results from
    distrowatch.com and displays
    results in tabular form.
    Selected torrent is downloaded in hard-drive.
    Default download location is $HOME/downloads/torrench
    """

    def __init__(self, title):
        """Initialisations."""
        Common.__init__(self)
        self.title = title
        self.logger = logging.getLogger('log1')
        self.index = 0
        self.mylist = []
        self.urllist = []
        self.url = "https://distrowatch.com/dwres.php?resource=bittorrent"
        self.output_headers = ['NAME', 'INDEX', 'UPLOADED']
        self.mapper = []
        self.soup = None

    def fetch_results(self):
        """To fetch results for given input."""
        masterlist = []
        try:
            torrent = self.soup.find_all('td', 'torrent')
            torrent_date = self.soup.find_all('td', 'torrentdate')
            for i, j in zip(torrent, torrent_date):
                try:
                    link = i.find('a')
                    url = "https://distrowatch.com/" + link.get('href')
                    name = link.string
                    name = name.lower()
                    if self.title in name:
                        date = j.string
                        self.index += 1
                        self.mapper.insert(self.index, (name))
                        self.mylist = [name, "--" + str(self.index) + "--", date]
                        masterlist.append(self.mylist)
                        self.urllist.append(url)
                except AttributeError as e:
                    self.logger.exception(e)
                    pass
            if self.index == 0:
                click.echo("No results found for give input!")
                self.logger.debug("\nNo results found for given input! Exiting!")
                sys.exit(2)
            return masterlist
        except Exception as e:
            self.logger.exception(e)
            click.echo("Error message: %s" %(e))
            click.echo("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)

    def select_torrent(self):
        """
        To select torrent and download.

        Torrent is selected thorugh index value.
        Selected torrent (.torrent file) is downloaded to hard-drive.
        Default download location is $HOME/downloads/torrench
        """
        self.logger.debug("Selecting torrent...")
        click.echo("\nTorrent can be downloaded directly through index\n")
        temp = 9999
        while(temp != 0):
            try:
                temp = click.prompt("(0 = exit)\nindex > ", type=int)
                self.logger.debug("input index %d" % (temp))
                if temp == 0:
                    click.echo("\nBye!")
                    self.logger.debug("Torrench quit!")
                    break
                elif temp < 0:
                    self.logger.debug("Invalid input index %d" % (temp))
                    click.echo("\nBad Input\n")
                    continue
                else:
                    selected_torrent = self.mapper[temp-1]
                    self.logger.debug("selected torrent: %s ; index: %d" % (selected_torrent, temp))
                    selected_torrent = click.style(selected_torrent, fg="yellow")
                    torrent_url = self.urllist[temp-1]
                    torrent_name = torrent_url.split('/')[5]
                    click.echo("\nSelected index [%s] - %s" % (temp, selected_torrent))
                    self.download(torrent_url, torrent_name)
            except (ValueError, IndexError, KeyError) as e:
                self.logger.exception(e)
                click.echo("\nBad Input\n")


def main(title):
    """Execution begins here."""
    try:
        click.echo("\n[DistroWatch]\n")
        title = title.lower()
        dw = DistroWatch(title)
        click.echo("Fetching results...")
        dw.soup = dw.http_request(dw.url)
        masterlist = dw.fetch_results()
        dw.logger.debug("Results fetched successfully!")
        dw.show_output(masterlist, dw.output_headers)
        dw.select_torrent()
    except KeyboardInterrupt as e:
        dw.logger.debug("Keyboard interupt! Exiting!")
        click.echo("\n\nAborted!")


if __name__ == "__main__":
    print("Its a module!")
