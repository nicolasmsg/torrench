"""Torrench Module."""

import os
import sys
import argparse
import logging
import click
from torrench.utilities.config import Config
from torrench.core.torrench import pass_torrench, Torrench
from torrench import __version__


logger = logging.getLogger(__name__)

TORRENCH_SETTINGS = dict(auto_envvar_prefix='TORRENCH')

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'modules'))


class CommandsLoader(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        ctx.cmd_map = {}

        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                mod = __import__('torrench.modules.' + filename[:-3], 
                        None, None, ['CMD_NAME'])
                rv.append(mod.CMD_NAME)
                ctx.cmd_map[mod.CMD_NAME] = filename[:-3]
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        self.list_commands(ctx)
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('torrench.modules.' + ctx.cmd_map[name],
                             None, None, ['cli'])
        except ImportError as ex:
            return
        return mod.cli


@click.command(cls=CommandsLoader, context_settings=TORRENCH_SETTINGS, invoke_without_command=True)
@click.version_option(__version__)
@click.option('-i', '--interactive', is_flag=True, help='Enable interactive mode for searches')
@click.option('-s', '--search', help='Search in default proxy')
@click.option('--set-default', help='Set default proxy')
@click.option('--import-module', type=click.Path(exists=True, file_okay=True, 
                                          resolve_path=True), help='Import the given module')
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