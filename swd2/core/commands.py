import subprocess
import os

from swd2.core.exttypes import ExtEnum, ExtObject
from swd2.core.extlogging import LogLevel, ExtLogger, LogTemplates
from swd2.core.extcolors import Color

LOG_INDENT = '>    '
COL_BLUE = '\033[94m'
COL_GREEN = '\033[92m'
COL_RED = '\x1b[38;5;196m'
COL_YELLOW = '\x1b[33m'
COL_RESET = '\033[0m'


class CmdStatus(ExtEnum):
    SUCCESS = (0, LogLevel.INFO, f'{COL_GREEN}')
    ERROR = (1, LogLevel.ERROR, f'{COL_RED}')
    SKIP = (2, LogLevel.WARNING, f'{COL_YELLOW}')

    def __new__(cls, value, log_level: LogLevel, color: str):
        obj = object.__new__(cls)
        obj._value = value
        obj._log_level = log_level
        obj._color = color
        return obj

    @property
    def color(self):
        return self._color

    @property
    def log_level(self):
        return self._log_level

    @staticmethod
    def of(value: int):
        if value == 0:
            return CmdStatus.SUCCESS
        else:
            return CmdStatus.ERROR


class CmdResult(ExtObject):
    cmd: str = None
    path: str = None
    output: str = None
    status: CmdStatus = None
    result_code: int = None

    def __init__(self, cmd: str, path: str, output: str, result_code: int, status: CmdStatus):
        self.cmd = cmd
        self.path = path
        self.output = output
        self.status = status
        self.result_code = result_code;

    @property
    def is_ok(self):
        return self.status != CmdStatus.ERROR

    def log(self):
        log_detailed(self)

    def value(self) -> str:
        return str(self.output).strip()

    def validate(self):
        if not self.is_ok:
            self.log()
            raise CmdException(self)
        return self

    def __str__(self) -> str:
        return f'CmdResult(cmd={self.cmd}. status={self.status}, resultCode={self.result_code}, output={self.output})'


class CmdResults(ExtObject):
    def __init__(self,
                 cmd: str,
                 results: list[CmdResult] = []
                 ):
        self.cmd = cmd
        self.results = results

    @property
    def isOk(self) -> bool:
        return all(result for result in self.results if result.is_ok is True)

    @property
    def status(self) -> CmdStatus:
        return CmdStatus.SUCCESS if self.is_ok else CmdStatus.ERROR


def execute(cmd, path: str = os.path.curdir) -> CmdResult:
    LogTemplates.subtitle(f'Run command {LogTemplates.variable(cmd)} in dir: {LogTemplates.variable(path)}', logLevel=LogLevel.DEBUG)
    resolved_cmd = tuple(cmd.split(' '))

    result = None
    try:
        result = subprocess.run(resolved_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        output = '\n'.join([
            result.stdout.decode('utf-8'),
            result.stderr.decode('utf-8')
        ])
        result = CmdResult(cmd=cmd, path=path, result_code=result.returncode, status=CmdStatus.of(result.returncode), output=output)
    except subprocess.CalledProcessError as err:
        result = CmdResult(cmd=cmd, path=path, result_code=err.returncode, status=CmdStatus.ERROR, output=err.stderr.decode('utf-8'))
    except Exception as err:
        result = CmdResult(cmd=cmd, path=path, result_code=1, status=CmdStatus.ERROR, output=str(err))
    return result


def log_summary(cmd: str, cmd_results):
    status = _get_status(cmd_results)
    LogTemplates.subtitle(f'Summary of executing {LogTemplates.variable(cmd)} : {format_status(status)}')
    for result in cmd_results:
        log_simple(result)


def _get_status(cmd_results):
    if any(not result.is_ok for result in cmd_results):
        return CmdStatus.ERROR
    else:
        return CmdStatus.SUCCESS


def log_simple(cmd_result: CmdResult):
    logger = ExtLogger.getLogger()
    cmd_status = format_status(cmd_result.status)
    logger.info(f'{cmd_status} : [{COL_BLUE}{cmd_result.cmd}{COL_RESET}] : {str(cmd_result.path)}')


def format_status(status: CmdStatus):
    return f'{status.color}[{status.name}]{COL_RESET}'


def log_detailed(cmd_result: CmdResult):
    title = f'when command {LogTemplates.variable(cmd_result.cmd)}'
    output = LOG_INDENT + cmd_result.output.replace('\n', f'\n{LOG_INDENT}')

    ExtLogger.log(f'{cmd_result.status.log_level.name} : {title}', log_level=cmd_result.status.log_level)
    ExtLogger.log(output, log_level=cmd_result.status.log_level)


class CmdException(Exception):
    def __init__(self, cmdResult: CmdResult):
        self.cmdResult = cmdResult
        self.message = f'Command {LogTemplates.variable(cmdResult.cmd)} failed with Error: {LogTemplates.variable(cmdResult.result_code)}:\n{cmdResult.output}'
