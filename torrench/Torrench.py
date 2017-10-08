"""Torrench Module."""

import os
import sys
import argparse
import logging
import click
from torrench.utilities.config import Config
from torrench.utilities.module_loader import list_commands, get_command
from torrench.utilities.constants import TORRENCH_SETTINGS
from torrench.core.torrench import pass_torrench, Torrench
from torrench import __version__


logger = logging.getLogger(__name__)


class CommandsLoader(click.MultiCommand):

    def list_commands(self, ctx):
        return list_commands()

    def get_command(self, ctx, name):
        return get_command(name)

@click.command(cls=CommandsLoader, context_settings=TORRENCH_SETTINGS,
               invoke_without_command=True)
@click.version_option(__version__)
@click.option('-i', '--interactive', is_flag=True,
              help='Enable interactive mode for searches')
@click.option('-s', '--search', help='Search in default proxy')
@click.option('--set-default', help='Set default proxy')
@click.option('--import-module', type=click.Path(exists=True, file_okay=True,
                                                 resolve_path=True),
              help='Import the given module')
@pass_torrench
@click.pass_context
def cli(ctx, torrench, interactive, search, set_default, import_module):
    """Command-line torrent search tool."""
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
        if import_module:
            click.echo("I'm importing : ", import_module)
            return
        if search:
            click.echo('Searching ' + search + ' in default proxy')
        else:
            import torrench.utilities.interactive as interactive
            click.echo('Loading interactive mode')
            interactive.inter()
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)