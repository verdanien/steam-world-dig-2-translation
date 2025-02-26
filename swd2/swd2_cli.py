import click
import pyfiglet

from pathlib import Path

from swd2.core.extcolors import Color
from swd2.core.extlogging import ExtLogger, LogLevel, LogTemplates, LogConfig
from swd2.core.exttypes import ExtObject


class Swd2Config(ExtObject):
    def __init__(self):
        self.verbose = False
        self.working_dir = ".."
        self.login_level = LogLevel.INFO
        self.root = str(Path(__file__).parent)


stored_config = click.make_pass_decorator(Swd2Config, ensure=True)


@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('--working-dir', type=click.types.Path(), default='.', help="working directory")
@click.option('--log-level', help='Logging level', default='INFO')
@stored_config
def cli(config: Swd2Config, verbose, working_dir, log_level):
    click.secho(f'{Color.BLUE.format(pyfiglet.figlet_format("SteamWorldDig2", font="doom"))}')

    if verbose:
        ExtLogger.info(f'Use verbose mode {LogTemplates.variable(verbose)}')
        config.verbose = verbose

    if working_dir:
        working_path = Path(working_dir)
        ExtLogger.info(f'Working dir set to {LogTemplates.variable(working_dir)} absolute path: {LogTemplates.variable(working_path.absolute())}')
        config.working_dir = working_path

    if log_level:
        ExtLogger.info(f'Set lgging level to {LogTemplates.variable(log_level)}')
        parsed_level = LogLevel.ofName(log_level)
        config.login_level = parsed_level
        LogConfig.setLevel(parsed_level)


@cli.command
@stored_config
def working_dir(config: Swd2Config):
    '''
    Displays project location
    '''
    ExtLogger.info(f'Swd2 location: {LogTemplates.variable(config.root)}')
