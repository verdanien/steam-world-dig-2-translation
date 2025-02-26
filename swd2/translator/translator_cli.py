import click
from swd2.swd2_cli import cli, stored_config, Swd2Config
from swd2.core.extlogging import ExtLogger, LogTemplates, LogLevel
from swd2.translator import compressor


@cli.group()
@stored_config
def translator(config):
    '''
    Translator group
    '''
    LogTemplates.title('Translator utility')


@translator.command()
@click.option('--src',
              type=click.types.Path(),
              required=True,
              help="Source file location"
              )
@click.option('--dst',
              type=click.types.Path(),
              help="Target file location"
              )
@click.option('--force',
              is_flag=True,
              help="Force overwrite file"
              )
@stored_config
def decompress(config: Swd2Config, src: str, dst: str, force: bool):
    '''
    Decompress *.csv.z to *.csv
    '''
    compressor.decompress(config.working_dir / src, config.working_dir / dst, force)


@translator.command()
@click.option('--src',
              type=click.types.Path(),
              required=True,
              help="Source file location"
              )
@click.option('--dst',
              type=click.types.Path(),
              help="Target file location"
              )
@click.option('--force',
              is_flag=True,
              help="Force overwrite file"
              )
@stored_config
def compress(config: Swd2Config, src: str, dst: str, force: bool):
    '''
    Compress *.csv to *.csv.z
    '''
    compressor.compress(config.working_dir / src, config.working_dir / dst, force)


@translator.command()
@click.option('--ext',
              type=str,
              help="Extension",
              default=".csv.z"
              )
@click.option('--dst',
              type=click.types.Path(),
              help="Target dir",
              default="out"
              )
@click.option('--force',
              is_flag=True,
              help="Force overwrite file"
              )
@stored_config
def decompress_all(config: Swd2Config, ext:str, dst: str, force: bool):
    '''
    Decompress all files *.csv.z to *.csv
    '''
    outDir = config.working_dir / dst
    outDir.mkdir(parents=True, exist_ok=True)
    for file in config.working_dir.glob(f"*{ext}"):
        ExtLogger.info(f'File: {LogTemplates.variable(file.name)}')
        compressor.decompress(file, outDir / file.stem, force)


@translator.command()
@click.option('--ext',
              type=str,
              help="Extension",
              default=".csv"
              )
@click.option('--dst',
              type=click.types.Path(),
              help="Target dir",
              default="out"
              )
@click.option('--force',
              is_flag=True,
              help="Force overwrite file"
              )
@stored_config
def compress_all(config: Swd2Config, ext:str, dst: str, force: bool):
    '''
    Compress all files *.csv to *.csv.z
    '''
    outDir = config.working_dir / dst
    outDir.mkdir(parents=True, exist_ok=True)
    for file in config.working_dir.glob(f"*{ext}"):
        ExtLogger.info(f'File: {LogTemplates.variable(file.name)}')
        compressor.compress(file, (outDir / file.stem).with_suffix(".z"), force)
