
import logging
import sys
from torrench.utilities.config import Config
import torrench.utilities.module_loader as mod_loader 
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
        self.load_modules()

    def load_modules(self):
        cmds = mod_loader.list_commands()
        for cmd in cmds:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            try:
                mod = __import__('torrench.modules.' + mod_loader.cmd_map[cmd],
                                None, None, ['cli', 'main'])
            except FileNotFoundError:
                if Config().file_exists():
                    mod = __import__('torrench.modules.privates.' + mod_loader.cmd_map[cmd],
                        None, None, ['cli', 'main'])
                else:
                    continue
            self._modules['!' + cmd] = mod
        return self._modules

    def parser(self, query):
        """
        :query: String to query the module.
        """
        _available_modules = self.load_modules().keys()
        splitted_query = query.split(' ') 
        module = splitted_query[0]
        if module in ('!h', 'help'):
            self.logger.debug("Display !h (help menu)")
            self._interactive_help()
        elif module in _available_modules:
            self._caller(module, splitted_query[1])
        elif module in ('!q', 'quit'):
            self.logger.debug("!q selected. Exiting interactive mode")
            print("Bye!")
            sys.exit(2)
        else:
            self.logger.debug("Invalid command input")
            print('Invalid command! Try `!h` or `help` for help.')

    def _caller(self, module, query):
        """
        Send queries to their respective modules.

        :module: Module to use in query.
        :query: String to search for.
        """
        # _modules = self._set_modules()
        if query and module in self._modules and not query.isspace():
            self.logger.debug("Selected module %s, query: %s" % ((module), query))
            self._modules[module].main(query)
        else:
            click.prompt("You called an invalid module or provided an empty query. Module: {}, query: {}".format(module, query))
            self.logger.debug("Called an invalid module or provided an empty query.")

    # @staticmethod
    def _interactive_help(self):
        """
        Display help
        """
        default_help_text = """
            Available commands:
        !h or help  - Help text (this)
        !q or quit  - Quit interactive mode
        """

        modules_help_text = """ 
            Available modules :
        """
        modules = self.load_modules()
        for key, value in modules.items():
            modules_help_text +=  "\r\n\t" + key + ' <string> - ' + value.cli.__doc__
            
        help_text = default_help_text + '\r\n' + modules_help_text

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
