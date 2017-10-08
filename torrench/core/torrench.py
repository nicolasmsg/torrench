import os
import sys
import argparse
import logging
import click
from torrench.utilities.config import Config

logger = logging.getLogger(__name__)



class Torrench(Config):

    def __init__(self):
        """Initialisations."""
        Config.__init__(self)
        self.args = None # Should probable be deleted
        self.copy = False
        self.input_title = None
        self.page_limit = 0
        self.interactive = False

    def remove_temp_files(self):
        """
        Actually only used to remove TPB HTML files (-c).

        Clearing HTML files only works for TPB (-t)
        (since only TPB generates HTML for torrent descriptions)
        Default location for temp files is
        ~/.torrench/temp (Windows/linux)
        """
        logger.debug("Selected -c :: remove tpb temp html files.")
        home = os.path.expanduser(os.path.join('~', '.torrench'))
        temp_dir = os.path.join(home, "temp")
        logger.debug("temp directory default location: %s" % (temp_dir))
        if not os.path.exists(temp_dir):
            click.echo("Directory not initialised. Exiting!")
            logger.debug("directory not found")
            sys.exit(2)
        files = os.listdir(temp_dir)
        if not files:
            click.echo("Directory empty. Nothing to remove")
            logger.debug("Directory empty!")
            sys.exit(2)
        else:
            for count, file_name in enumerate(files, 1):
                os.remove(os.path.join(temp_dir, file_name))
            click.echo("Removed {} file(s).".format(count))
            logger.debug("Removed {} file(s).".format(count))
            sys.exit(2)    

    def check_copy(self):
        """Check if --copy argument is present."""
        if self.copy:
            return True

    def verify_input(self):
        """To verify if input given is valid or not."""
        if self.input_title is None and not self.interactive:
            logger.debug("Bad input! Input string expected! Got 'None'")
            click.echo("\nInput string expected.\nUse --help for more\n")
            sys.exit(2)

        if self.page_limit <= 0 or self.page_limit > 50:
            logger.debug("Invalid page_limit entered: %d" % (tr.page_limit))
            click.echo("Enter valid page input [0<p<=50]")
            sys.exit(2)


# torrench = Torrench()

pass_torrench = click.make_pass_decorator(Torrench, ensure=True)
