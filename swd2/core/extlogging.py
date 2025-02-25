import copy
import inspect
import logging

from pathlib import Path

from swd2.core.exttypes import ExtEnum
from swd2.core.extcolors import Color


class LogLevel(ExtEnum):
    DEBUG = (logging.DEBUG, f'{Color.GRAY_DARK}')
    INFO = (logging.INFO, f'{Color.GRAY}')
    WARN = (logging.WARN, f'{Color.YELLOW}')
    WARNING = (logging.WARNING, f'{Color.YELLOW}')
    ERROR = (logging.ERROR, f'{Color.RED}')
    CRITICAL = (logging.CRITICAL, f'{Color.RED_WITH_BG}')

    def __new__(cls, value, color):
        obj = object.__new__(cls)
        obj._value = value
        obj._color = color
        return obj

    @property
    def value(self):
        return self._value

    @property
    def color(self):
        return self._color

    @classmethod
    def ofValue(cls, value):
        for key, el in cls.elements().items():
            if el.value == value:
                return el
        return None
        # raise NoSuchElementException(f'Element [{value}] not exists for [{cls}]. Possible values are [{str(cls.elements().values())}]')


class ExtLogger:
    def __init__(self, file, line: int):
        self.id = f'{str(file)}:{line}'
        self.name = Path(file).stem
        self.line = line
        self.file = file
        self.shortPath = f'.({self.name}.py:{line})'
        self.logger = logging.getLogger(
            self.shortPath)  # intellij interprets '.(filename:line_no)' as a link to file, then it produces a navigable link in the logs to the given file and line number.
        LogConfig.register(self)

    def setLevel(self, level: LogLevel):
        self.logger.setLevel(level.value)

    def getLevel(self):
        return LogLevel.ofValue(self.logger.level)

    def __str__(self):
        return f'{self.name} : {self.getLevel()}'

    @staticmethod
    def getLogger(level=1):
        stack = inspect.stack()
        frame = stack[level]
        file = inspect.getfile(frame[0])
        line_no = frame.lineno
        return ExtLogger(file, line_no)

    @staticmethod
    def resetColor(message: str, level: LogLevel) -> str:
        return message.replace(f'{Color.RESET}', level.color)

    @staticmethod
    def log(message: str = ' ', log_level: LogLevel = LogLevel.INFO, stack: int = 2):
        ExtLogger.getLogger(stack).logger.log(log_level.value, ExtLogger.resetColor(str(message), log_level))

    @staticmethod
    def debug(message: str = ' ', stack: int = 2):
        ExtLogger.getLogger(stack).logger.debug(ExtLogger.resetColor(str(message), LogLevel.DEBUG))

    @staticmethod
    def info(message: str = ' ', stack: int = 2):
        ExtLogger.getLogger(stack).logger.info(ExtLogger.resetColor(str(message), LogLevel.INFO))

    @staticmethod
    def warn(message: str = ' ', stack: int = 2):
        ExtLogger.getLogger(stack).logger.warning(ExtLogger.resetColor(str(message), LogLevel.WARNING))

    @staticmethod
    def error(message: str, stack: int = 2, error: Exception = None):
        ExtLogger.getLogger(stack).logger.error(
            msg=ExtLogger.resetColor(message, LogLevel.ERROR)
        )

    @staticmethod
    def critical(message: str):
        ExtLogger.getLogger(2).logger.critical(ExtLogger.resetColor(str(message), LogLevel.CRITICAL))


class ExtLogFormatter(logging.Formatter):

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: f'{LogLevel.DEBUG.color}{fmt}{Color.RESET}',
            logging.INFO: f'{LogLevel.INFO.color}{fmt}{Color.RESET}',
            logging.WARNING: f'{LogLevel.WARNING.color}{fmt}{Color.RESET}',
            logging.ERROR: f'{LogLevel.ERROR.color}{fmt}{Color.RESET}',
            logging.CRITICAL: f'{LogLevel.CRITICAL.color}{fmt}{Color.RESET}'
        }

    def format(self, record):
        logLevel = LogLevel.ofValue(record.levelno)
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)

        records = []
        for line in record.msg.splitlines():
            cur_record = copy.deepcopy(record)
            line = line.replace(str(Color.RESET), str(''))
            cur_record.msg = line
            records.append(formatter.format(cur_record))

        return "\n".join(records)


class LogConfig:
    __DEFAULT_FORMAT = '%(asctime)s [%(levelname)-8s] %(name)-20s : %(message)s'
    format: str = __DEFAULT_FORMAT
    loggers = {}
    console = None

    @staticmethod
    def console_output():
        out = logging.StreamHandler()
        out.setLevel(logging.DEBUG)
        out.setFormatter(ExtLogFormatter(LogConfig.format))
        return out

    @staticmethod
    def register(ext: ExtLogger):
        LogConfig.cfg()

        ext.logger.handlers = []
        ext.logger.addHandler(LogConfig.console)
        ext.logger.setLevel(LogConfig.console.level)
        LogConfig.loggers[ext.id] = ext

    @classmethod
    def cfg(cls):
        if cls.console is None:
            cls.console = LogConfig.console_output()

    @classmethod
    def setLevel(cls, level: LogLevel):
        cls.cfg()
        cls.console.level = level.value

    @staticmethod
    def printLoggers():
        print('Loggers:')
        for (key, value) in LogConfig.loggers.items():
            print(f'{key} :{value}')


class LogTemplates:
    LINE_1 = '============================================================'
    LINE_2 = '------------------------------------------------------------'
    VARIABLE_COLOR = Color.ORANGE

    @classmethod
    def section(cls, title: str, line: str, color: Color, logLevel: LogLevel = LogLevel.INFO):
        msg = color.format(f'{line}\n{title}\n{line}')
        ExtLogger.log(msg, log_level=logLevel, stack=4)

    @classmethod
    def title(cls, title: str):
        cls.section(title=title, line=cls.LINE_1, color=Color.GREEN)

    @classmethod
    def subtitle(cls, title: str, logLevel: LogLevel = LogLevel.INFO):
        cls.section(title=title, line=cls.LINE_2, color=Color.GREEN_DARK, logLevel=logLevel)

    @classmethod
    def variable(cls, value) -> str:
        return f'[{cls.VARIABLE_COLOR.format(str(value))}]'


if __name__ == '__main__':
    print('-----------------')
    print('extlogging module')
    print('-----------------')

    LogTemplates.title(f'some message with value {LogTemplates.variable("internal var")} before end.')

    ExtLogger.debug('some message')
    ExtLogger.info('some message')
    ExtLogger.warn('some message')
    ExtLogger.error('some message')
    ExtLogger.critical('some message')

    LogConfig.printLoggers()

    LogConfig.setLevel(LogLevel.ERROR)

    ExtLogger.debug('some message')
    ExtLogger.info('some message')
    ExtLogger.warn('some message')
    ExtLogger.error('some message')
    ExtLogger.critical('some message')
