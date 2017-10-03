
import logging
from sys import exit as _exit
import torrench.modules.distrowatch as distrowatch
import torrench.modules.kickasstorrent as kat
import torrench.modules.linuxtracker as linuxtracker
import torrench.modules.nyaa as nyaa_module
import torrench.modules.skytorrents as sky
import torrench.modules.thepiratebay as tpb_module
import torrench.modules.xbit as xbit_module
from torrench.utilities.config import Config
import click


class InteractiveMode:
    """
    This class deals with most of the functionality assigned to the interactive mode.
    It resolves the arguments, parses and calls their respective modules
    :params: None
    """
    def __init__(self):
        self._modules = {}
        self.logger = logging.getLogger('log1')

    def parser(self, query):
        """
        :query: String to query the module.
        """
        _available_modules = self._set_modules().keys()
        if query[:4] in ('!h', 'help'):
            self.logger.debug("Display !h (help menu)")
            self._interactive_help()
        elif query[:2] in _available_modules:
            self._caller(query[:2], query[3:])
        elif query[:4] in ('!q', 'quit'):
            self.logger.debug("!q selected. Exiting interactive mode")
            print("Bye!")
            _exit(2)
        else:
            self.logger.debug("Invalid command input")
            print('Invalid command! Try `!h` or `help` for help.')

    def _set_modules(self):
        """
        Map functions to commands and return dictionary.
        """
        if Config().file_exists():
            self._modules = {
                            '!t': tpb_module,
                            '!n': nyaa_module,
                            '!k': kat,
                            '!x': xbit_module,
                            '!d': distrowatch,
                            '!l': linuxtracker,
                            '!s': sky
                            }
            return self._modules
        else:
            self.logger.debug("Config file not setup!")

        self._modules = {
                            '!d': distrowatch,
                            '!l': linuxtracker
                            }

        return self._modules

    def _caller(self, module, query):
        """
        Send queries to their respective modules.

        :module: Module to use in query.
        :query: String to search for.
        """
        _modules = self._set_modules()
        if query and module in _modules and not query.isspace():
            self.logger.debug("Selected module %s, query: %s" % ((module), query))
            if module in ['!t', '!k', '!s']:
                _modules[module].main(query, page_limit=1)
            else:
                _modules[module].main(query)
        else:
            print("You called an invalid module or provided an empty query.")
            self.logger.debug("Called an invalid module or provided an empty query.")

    @staticmethod
    def _interactive_help():
        """
        Display help
        """
        help_text = """
            Available commands:
        !h or help  - Help text (this)
        !q or quit  - Quit interactive mode
        !t <string> - Search on LinuxTorrents
        !d <string> - Search on DistroWatch

        =========== Requires Config file ==========
        !n <string> - Search on nyaa.si for anime.
        !t <string> - Search on ThePirateBay.
        !k <string> - Search on KickAssTorrents.
        !s <string> - Search on SkyTorrents
        !x <string> - Search on XBit.pw
        ===========================================
        These commands are only available after a `config.ini` file has been set.
        See the documentation for more information.
        """
        print(help_text)


def inter():
    """
    Execution will start here.
    """
    try:
        i = InteractiveMode()
        while True:
            data = click.prompt(click.style('\ntorrench > ', fg="yellow"), type=str)
            i.logger.debug(data)
            i.parser(data)
    except (KeyboardInterrupt, EOFError):
        click.echo('Terminated.')
        i.logger.debug("Terminated.")


if __name__ == '__main__':
    print("Run torrench -i")
