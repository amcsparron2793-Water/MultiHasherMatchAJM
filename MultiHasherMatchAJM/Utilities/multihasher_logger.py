from logging import Logger
from typing import Any, Union

from EasyLoggerAJM import EasyLogger, SetupLogger
from MultiHasherMatchAJM import PROJECT_ROOT


class MultiHasherLogger(EasyLogger):
    _PROJECT_ROOT = PROJECT_ROOT
    ROOT_LOG_LOCATION_DEFAULT = _PROJECT_ROOT / 'logs'
    # noinspection SpellCheckingInspection
    PROJECT_NAME = 'MultiHasherMatchAJM'
    DEFAULT_LOG_SPEC = 'hourly'
    DEFAULT_SHOW_WARNING_LOGS_IN_CONSOLE = True

    @classmethod
    def _set_project_specific_kwarg_defaults(cls, **kwargs) -> dict[str, Any]:
        kwargs.setdefault('project_name', cls.PROJECT_NAME)
        kwargs.setdefault('show_warning_logs_in_console',
                          cls.DEFAULT_SHOW_WARNING_LOGS_IN_CONSOLE)
        kwargs.setdefault('log_spec', cls.DEFAULT_LOG_SPEC)
        return kwargs

    def __init__(self, **kwargs):
        kwargs = self._set_project_specific_kwarg_defaults(**kwargs)
        super().__init__(**kwargs)
        self.logger.name = self.__class__.__name__

    def __call__(self, **kwargs) -> Logger:
        return self.logger


class MultiHasherSetupLogger(SetupLogger):
    DEFAULT_CUSTOM_LOGGER = MultiHasherLogger
    RWI_WARNING_TEXT = ("return_wrapper_instance was set to True. "
                        "MultiHasherSetupLogger ignores this kwarg "
                        "and will always return a logger instance.")

    @classmethod
    def _log_and_return_logger(cls, setup_logger_super_return, rwi_choice: bool) -> Logger:
        logger = None
        if isinstance(setup_logger_super_return, Logger):
            logger = setup_logger_super_return
            logger.debug("super classmethod setup_logger returned a logger directly")
        elif hasattr(setup_logger_super_return, 'logger'):
            logger = setup_logger_super_return.logger
            logger.debug("super classmethod setup_logger returned an object with a logger attribute")

        if isinstance(logger, Logger):
            cls._rwi_warning(logger, rwi_choice)
            return logger
        raise ValueError("return value of setup_logger must be a Logger instance.")

    @classmethod
    def _rwi_warning(cls, logger: Logger, rwi: bool):
        if rwi:
            logger.warning(cls.RWI_WARNING_TEXT)

    @classmethod
    def setup_logger(cls, **kwargs) -> Logger:
        rwi = kwargs.get('return_wrapper_instance', False)
        sup = super().setup_logger(**kwargs)
        return cls._log_and_return_logger(sup, rwi)


if __name__ == '__main__':
    #abl = MultiHasherLogger()()
    abl = MultiHasherSetupLogger.setup_logger()
    abl.info("this is an info message")
    abl.warning("this is a warning message")
