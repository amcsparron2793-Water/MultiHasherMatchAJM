from logging import Logger
from typing import Optional

from EasyLoggerAJM import EasyLogger, SetupLogger
from MultiHasherMatchAJM import PROJECT_ROOT


class MultiHasherLogger(EasyLogger):
    _PROJECT_ROOT = PROJECT_ROOT
    ROOT_LOG_LOCATION_DEFAULT = _PROJECT_ROOT / 'logs'
    PROJECT_NAME = 'MultiHasherMatchAJM'

    def __init__(self, **kwargs):
        kwargs.setdefault('project_name', self.__class__.PROJECT_NAME)
        kwargs.setdefault('show_warning_logs_in_console', True)
        kwargs.setdefault('log_spec', 'hourly')
        super().__init__(**kwargs)
        self.logger.name = self.__class__.__name__

    def __call__(self, **kwargs) -> Logger:
        return self.logger


class MultiHasherSetupLogger(SetupLogger):
    DEFAULT_CUSTOM_LOGGER = MultiHasherLogger

    @classmethod
    def _check_fallback_logger_config(cls, default_logger_name: Optional[str] = None, **kwargs) -> Logger:
        default_logger_name = default_logger_name or 'logger'
        return super()._check_fallback_logger_config(default_logger_name=default_logger_name, **kwargs)


if __name__ == '__main__':
    #abl = MultiHasherLogger()()
    abl = MultiHasherSetupLogger.setup_logger()
    abl.info("this is an info message")
    abl.warning("this is a warning message")
