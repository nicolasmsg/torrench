"""Torrench Module."""

import os
import sys
import argparse
import logging
import click
from torrench.utilities.Config import Config


logger = logging.getLogger('log1')


class Torrench(Config):

    __version__ = "Torrench (1.0.54)"

    def __init__(self):
        """Initialisations."""
        Config.__init__(self)
        self.logger = logging.getLogger('log1')
        self.args = None # Should probable be deleted
        self.copy = False
        self.input_title = None
        self.page_limit = 0
        self.interactive = False

    # @staticmethod
    # def get_version():
    #     return self.__version__

    def remove_temp_files(self):
        """
        To remove TPB HTML files (-c).

        Clearing HTML files only works for TPB (-t)
        (since only TPB generates HTML for torrent descriptions)
        Default location for temp files is
        ~/.torrench/temp (Windows/linux)
        """
        self.logger.debug("Selected -c :: remove tpb temp html files.")
        home = os.path.expanduser(os.path.join('~', '.torrench'))
        temp_dir = os.path.join(home, "temp")
        self.logger.debug("temp directory default location: %s" % (temp_dir))
        if not os.path.exists(temp_dir):
            click.echo("Directory not initialised. Exiting!")
            self.logger.debug("directory not found")
            sys.exit(2)
        files = os.listdir(temp_dir)
        if not files:
            click.echo("Directory empty. Nothing to remove")
            self.logger.debug("Directory empty!")
            sys.exit(2)
        else:
            for count, file_name in enumerate(files, 1):
                os.remove(os.path.join(temp_dir, file_name))
            click.echo("Removed {} file(s).".format(count))
            self.logger.debug("Removed {} file(s).".format(count))
            sys.exit(2)    

    def check_copy(self):
        """Check if --copy argument is present."""
        if self.copy:
            return True

    def verify_input(self):
        """To verify if input given is valid or not."""
        if self.input_title is None and not self.interactive:
            self.logger.debug("Bad input! Input string expected! Got 'None'")
            click.echo("\nInput string expected.\nUse --help for more\n")
            sys.exit(2)

        if self.page_limit <= 0 or self.page_limit > 50:
            self.logger.debug("Invalid page_limit entered: %d" % (tr.page_limit))
            click.echo("Enter valid page input [0<p<=50]")
            sys.exit(2)

torrench = Torrench()


@click.command()
@click.option('-d', '--distrowatch', is_flag=True, help='Search distrowatch')
@click.option('-t', '--thepiratebay', is_flag=True, help='Search thepiratebay (TPB)')
@click.option('-k', '--kickasstorrent', is_flag=True, help='Search KickassTorrent (KAT)')
@click.option('-s','--skytorrents', is_flag=True, help='Search SkyTorrents')
@click.option('-n', '--nyaa', is_flag=True, help='Search Nyaa')
@click.option('-x', '--xbit', is_flag=True, help='Search XBit.pw')
@click.option('-i', '--interactive', is_flag=True, help='Enable interactive mode for searches')
@click.option('--top', is_flag=True, help='Get top torrents [TPB/SkyTorrents]')
@click.option('--copy', is_flag=True, help='Copy magnetic link to clipboard')
@click.option('-p', '--page-limit', default=1, help='LIMIT Number of pages to fetch results from (1 page = 30 results). [default: 1] [TPB/KAT/SkyTorrents]')
@click.option('-c', '--clear-html', is_flag=True, help='Clear all [TPB] torrent description HTML files and exit.')
# @click.option('-v', '--verbose', is_flag=True, help='Print debugs.')
@click.version_option(Torrench.__version__)
@click.argument('search', required=False)
def search(search, distrowatch,
           thepiratebay, kickasstorrent,
           skytorrents, nyaa, xbit, top,
           copy, page_limit, clear_html,
           interactive):
    """Command-line torrent search tool."""
    _PRIVATE_MODULES = (
        thepiratebay,
        kickasstorrent,
        skytorrents,
        nyaa,
        xbit
    ) # These modules are only enabled through manual configuration.

    torrench.input_title = search
    torrench.page_limit = page_limit
    torrench.copy = copy
    torrench.interactive = interactive 

    if not clear_html and not interactive:
        torrench.verify_input()
        torrench.input_title = torrench.input_title.replace("'", "")

    if clear_html:
        if not thepiratebay:
            click.echo('error: use -c with -t only')
            sys.exit(2)
        else:
            torrench.remove_temp_files()
    if any(_PRIVATE_MODULES):
        if not torrench.file_exists():
            click.echo("\nConfig file not configured. Configure to continue. Read docs for more info.\n")
            click.echo("Config file either does not exist or is not enabled! Exiting!")
            sys.exit(2)
        else:
            if thepiratebay:
                logger.debug('using thepiratebay')
                if top:
                    logger.debug('selected TPB TOP-torrents')
                    torrench.input_title = None
                    torrench.page_limit = None
                logger.debug("Input title: [%s] ; page_limit: [%s]" % (torrench.input_title, torrench.page_limit))
                import torrench.modules.thepiratebay as tpb
                tpb.main(torrench.input_title, torrench.page_limit)
            elif kickasstorrent:
                logger.debug("Using kickasstorrents")
                logger.debug("Input title: [%s] ; page_limit: [%s]" % (torrench.input_title, torrench.page_limit))
                import torrench.modules.kickasstorrent as kat
                kat.main(torrench.input_title, torrench.page_limit)
            elif skytorrents:
                logger.debug("Using skytorrents")
                if top:
                    logger.debug("selected SkyTorrents TOP-torrents")
                    torrench.input_title = None
                    torrench.page_limit = None
                logger.debug("Input title: [%s] ; page_limit: [%s]" % (torrench.input_title, torrench.page_limit))
                import torrench.modules.skytorrents as sky
                sky.main(torrench.input_title, torrench.page_limit)           
            elif nyaa:
                logger.debug("Using Nyaa.si")
                import torrench.modules.nyaa as nyaa
                nyaa.main(torrench.input_title)
            elif xbit:
                logger.debug("Using XBit.pw")
                logger.debug("Input title: [%s]" % (torrench.input_title))
                import torrench.modules.xbit as xbit
                xbit.main(torrench.input_title)
    elif distrowatch:
        logger.debug("Using distrowatch")
        logger.debug("Input title: [%s]" % (torrench.input_title))
        import torrench.modules.distrowatch as distrowatch
        distrowatch.main(torrench.input_title)
    elif interactive:
        logger.debug("Using interactive mode")
        import torrench.utilities.interactive as interactive
        interactive.inter()
    else:
        logger.debug("Using linuxtracker")
        logger.debug("Input title: [%s]" % (torrench.input_title))
        import torrench.modules.linuxtracker as linuxtracker
        linuxtracker.main(torrench.input_title)


def main():
    search()

