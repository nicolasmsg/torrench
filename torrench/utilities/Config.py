""" Config module."""
import os
import logging
from configparser import SafeConfigParser
from .Common import Common


class Config(Common):
    r"""
    Config class.

    This class checks for config file's presence.
    Also, this class manages TPB/KAT proxies; That is,
    obtains TPB/KAT URL and fetches proxies thorugh those URL.
    Proxies are stored as list and returned.

    By default, Config files is checked in $XDG_CONFIG_HOME/torrench/ and
    fallback to $HOME/.config/torrench/ directory (linux)
    For windows, default location is ~\.config\torrench

    This class inherits Common class.
    """

    def __init__(self):
        """Initialisations."""
        Common.__init__(self)
        self.config = SafeConfigParser()
        self.config_dir = os.getenv('XDG_CONFIG_HOME', os.path.expanduser(os.path.join('~', '.config')))
        self.full_config_dir = os.path.join(self.config_dir, 'torrench')
        self.config_file_name = "config.ini"
        self.config_file = os.path.join(self.full_config_dir, self.config_file_name)
        self.url = None
        self.name = None
        self.urllist = []
        self.logger = logging.getLogger('log1')
        self._is_verbose = False

    def file_exists(self):
        """To check whether config.ini file exists and is enabled or not."""
        if os.path.isfile(self.config_file):
            self.config.read(self.config_file)
            enable = self.config.get('Torrench-Config', 'enable')
            if enable == '1':
                self.logger.debug("Config file exists and enabled!")
                return True

    # To get proxies for KAT/TPB
    def get_proxies(self, name):
        """
        Get Proxies.

        Proxies are read from config.ini file.
        """
        self.logger.debug("getting proxies for '%s'" % (name))
        temp = []
        self.config.read(self.config_file)
        if name == 'tpb':
            name = 'TPB_URL'
        elif name == 'kat':
            name = 'KAT_URL'
        elif name == "sky":
            name = "SKY_URL"
        elif name == "xbit":
            name = "XBIT_URL"
        elif name == "nyaa":
            name = "NYAA_URL"
        self.url = self.config.get('Torrench-Config', name)
        self.urllist = self.url.split()
        if name == 'TPB_URL':
            soup = self.http_request(self.urllist[-1])
            link = soup.find_all('td', class_='site')
            del self.urllist[-1]
            for i in link:
                temp.append(i.a["href"])
            self.urllist.extend(temp)
        self.logger.debug("got %d proxies!" % (len(self.urllist)))
        return self.urllist
