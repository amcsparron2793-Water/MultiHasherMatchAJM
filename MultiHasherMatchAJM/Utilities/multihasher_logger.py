from logging import Logger
from typing import Optional, Any, Union, Callable

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
    def _set_project_specific_kwarg_defaults(cls, **kwargs):
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
    def _check_fallback_logger_config(cls, default_logger_name: Optional[str] = None, **kwargs) -> Logger:
        default_logger_name = default_logger_name or 'logger'
        return super()._check_fallback_logger_config(default_logger_name=default_logger_name, **kwargs)

    @classmethod
    def _rwi_warning(cls, logger, rwi):
        if rwi:
            logger.warning(cls.RWI_WARNING_TEXT)

    @classmethod
    def setup_logger(cls, **kwargs) -> Logger:
        rwi = True if 'return_wrapper_instance' in kwargs else False
        sup = super().setup_logger(**kwargs)

        if isinstance(sup, Logger):
            sup.debug("super classmethod setup_logger returned a logger directly")
            cls._rwi_warning(sup, rwi)
            return sup
        elif hasattr(sup, 'logger'):
            sup.logger.debug("super classmethod setup_logger returned an object with a logger attribute")
            cls._rwi_warning(sup.logger, rwi)
            return sup.logger
        raise ValueError("return value of setup_logger must be a Logger instance.")


if __name__ == '__main__':
    #abl = MultiHasherLogger()()
    abl = MultiHasherSetupLogger.setup_logger()
    abl.info("this is an info message")
    abl.warning("this is a warning message")
