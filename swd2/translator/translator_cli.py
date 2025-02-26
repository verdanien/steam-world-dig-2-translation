import click
import os
from pathlib import Path
from swd2.swd2_cli import cli, stored_config, Swd2Config

from swd2.core.extlogging import ExtLogger, LogTemplates, LogLevel
from swd2.core.commands import execute
from swd2.core.exttypes import ExtObject

@cli.group()
@stored_config
def translator(config):
    '''
    Translator group
    '''
    LogTemplates.title('Translator utility')


@translator.command()
@stored_config
def decompress(config: Swd2Config):
    '''
    Decompress *.csv.z file
    '''