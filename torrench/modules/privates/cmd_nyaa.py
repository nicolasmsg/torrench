"""nyaa.si module"""

import sys
import logging
import platform
from torrench.utilities.config import Config
from torrench.core.torrench import pass_torrench
import click


CMD_NAME = 'nyaa'

@click.command('nyaa', short_help='search on NyaaTracker.')
@click.argument('search')
@pass_torrench
@click.pass_context
def cli(ctx, torrench, search):
    """Search on nyaa tracker."""
    click.echo('search on NyaaTracker')
    torrench.input_title = search 
    main(torrench.input_title)


class NyaaTracker(Config):
    """
    Nyaa.si class.

    This class fetches results from nyaa.si
    and displays in tabular form.
    Selected torrent is downloaded to hard-drive.

    Default download location is $HOME/Downloads/torrench

    Known problems:
    - If the torrent name in the website is too long (200 chars+) the table will be displayed incorrectly in the terminal.
    Possible fixes:
    - Cut the name if the name is too big.
    """

    def __init__(self, title: str):
        """Class constructor"""
        Config.__init__(self)
        self.title = title
        self.logger = logging.getLogger('log1')
        self.output_headers = ['NAME', 'INDEX', 'SIZE', 'S', 'L']
        self.index = 0
        self.mapper = []
        self.proxy = self.check_proxy('nyaa')
        self.search_parameter = "/?f=0&c=0_0&q={query}&s=seeders&o=desc".format(query=self.title)
        self.soup = self.http_request(self.proxy+self.search_parameter)
        self.OS_WIN = False
        if platform.system() == "Windows":
            self.OS_WIN = True

    def check_proxy(self, proxy: str):
        """
        Check for proxies in the `config.ini` file.
        :params: proxy
        :returns: proxy on success, -1 on error
        """
        _torrench_proxies = self.get_proxies(proxy)
        counter = 0
        if _torrench_proxies:
            for proxy in _torrench_proxies:
                click.echo("Testing: {proxy}".format(proxy=click.style(proxy, fg='yellow')))
                proxy_soup = self.http_request(proxy+'/?f=0&c=0_0&q=hello&s=seeders&o=desc')
                self.logger.debug("Testing {proxy} as a possible candidate.".format(proxy=proxy))
                if not proxy_soup.find_all('td', {'colspan': '2'}):
                    click.echo("{proxy} was a bad proxy. Trying next proxy.".format(proxy=proxy))
                    counter += 1
                    if counter == len(_torrench_proxies):
                        self.logger.debug("Proxy list finished. No valid proxies were found.")
                        click.echo("Failed to find any valid proxies. Terminating.")
                        return -1
                else:
                    click.echo("Proxy `{proxy}` is available. Connecting.".format(proxy=proxy))
                    self.logger.debug("Proxy `{proxy}` is a valid proxy.")
                    return proxy
        click.echo("No proxies were given.")
        return -1

    def parse_name(self):
        """
        Parse torrent name
        """
        t_names = []
        for name in self.soup.find_all('td', {'colspan': '2'}):
            n = name.get_text().replace('\n', '')
            if self.OS_WIN:
                n = n.encode('ascii', 'replace').decode()
            t_names.append(n)
        if t_names:
            return t_names
        click.echo("Unable to parse torrent name.")
        sys.exit(2)

    def parse_urls(self):
        t_urls = []
        for url in self.soup.find_all('a'):
            try:
                if url.get('href').startswith('/download/'):
                    t_urls.append(click.style('https://nyaa.si'+url['href'], fg='yellow'))
            except AttributeError:
                pass
        if t_urls:
            return t_urls
        click.echo("Unable to parse torrent URLs.")
        sys.exit(2)

    def parse_magnets(self):
        t_magnets = []
        for url in self.soup.find_all('a'):
            try:
                if url['href'].startswith('magnet:'):
                    t_magnets.append(url['href'])
            except KeyError:
                pass
        if t_magnets:
            return t_magnets
        click.echo("Unable to parse magnet links.")
        sys.exit(2)

    def parse_sizes(self):
        t_size = []
        for size in self.soup.find_all('td', {'class': 'text-center'}):
            if size.get_text().endswith(("GiB", "MiB")):
                if self.OS_WIN:
                    t_size.append( size.get_text())
                else:
                    t_size.append(click.style(size.get_text(), fg='yellow'))
            else:
                pass
        if t_size:
            return t_size
        click.echo("Unable to parse size of files.")
        sys.exit(2)

    def parse_seeds(self):
        t_seeds = []
        for seed in self.soup.find_all('td', {'style': 'color: green;'}):
            t_seeds.append(click.style(seed.get_text(), fg="green"))
        if t_seeds:
            return t_seeds
        click.echo("Unable to parse seeds")
        sys.exit(2)

    def parse_leeches(self):
        t_leeches = []
        for leech in self.soup.find_all('td', {'style': 'color: red;'}):
            t_leeches.append(click.style(leech.get_text(), fg="red"))
        if t_leeches:
            return t_leeches
        click.echo("Unable to parse leechers")
        sys.exit(2)

    def fetch_results(self):
        """
        Fetch results for a given query.

        @datafanatic:
        Work in progress
        """
        click.echo("Fetching results")
        self.logger.debug("Fetching...")
        self.logger.debug("URL: %s", self.url)
        try:
            name = self.parse_name()
            urls = self.parse_urls()
            sizes = self.parse_sizes()
            seeds = self.parse_seeds()
            leeches = self.parse_leeches()
            magnets = self.parse_magnets()
            self.index = len(urls)
        except (KeyError, AttributeError) as e:
            click.echo("Something went wrong. Logging and terminating.")
            self.logger.exception(e)
            click.echo("OK. Terminating.")
        if self.index == 0:
            click.echo("No results were found for the given query. Terminating")
            self.logger.debug("No results were found for `%s`.", self.title)
            return -1
        self.logger.debug("Results fetched. Showing table.")
        self.mapper.insert(self.index+1, (name, urls, magnets))
        return list(zip(name, ["--"+str(idx)+"--" for idx in range(1, self.index+1)], sizes, seeds, leeches))

    def select_torrent(self):
        """Select torrent from table using index."""
        while True:
            try:
                prompt = click.prompt("\n\n(0 to exit)\nIndex > ", type=int)
                self.logger.debug("Selected index {idx}".format(idx=prompt))
                if prompt == 0:
                    click.echo("Bye!")
                    break
                else:
                    selected_torrent, download_url, magnet_url = self.mapper[0][0][prompt-1], self.mapper[0][1][prompt-1], self.mapper[0][2][prompt-1]
                    selected_torrent = click.style(selected_torrent, fg="yellow")
                    click.echo("Selected index [{idx}] - {torrent}\n".format(idx=prompt, torrent=selected_torrent))
                    # Print Magnetic link / load magnet to client
                    prompt2 = click.prompt("1. Print magnetic link [p]\n2. Load magnetic link to client [l]\n\nOption [p/l]: ", type=str)
                    prompt2 = prompt2.lower()
                    self.logger.debug("selected option: [%c]" % (prompt2))
                    if prompt2 == 'p':
                        self.logger.debug("printing magnetic link and upstream link")
                        click.echo("\nMagnet link: {magnet}".format(magnet=click.style(magnet_url, fg="red")))
                        self.copy_magnet(magnet_url)
                        click.echo("\n\nUpstream link: {url}\n".format(url=download_url))
                    elif prompt2 == 'l':
                        try:
                            self.logger.debug("Loading torrent to client")
                            self.load_torrent(magnet_url)
                        except Exception as e:
                            self.logger.exception(e)
                            continue
            except (ValueError, IndexError, TypeError) as e:
                click.echo("\nBad Input!")
                self.logger.exception(e)
                continue

    def get_torrent(self, url, name):
        """Download the .torrent file to the computer."""
        self.download(url, name+'.torrent')

def main(title):
    """
    Execution will begin here.
    """
    try:
        click.echo("\n[Nyaa.si]\n")
        nyaa = NyaaTracker(title)
        results = nyaa.fetch_results()
        nyaa.show_output([result for result in results], nyaa.output_headers)
        nyaa.select_torrent()
    except KeyboardInterrupt:
        nyaa.logger.debug("Interrupt detected. Terminating.")
        click.echo("Terminated")


if __name__ == "__main__":
    print("Modules are not supposed to be run standalone.")
