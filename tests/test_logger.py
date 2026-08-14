import pytest
import logging
from MultiHasherMatchAJM.Utilities.multihasher_logger import MultiHasherLogger, MultiHasherSetupLogger


class TestMultiHasherLogger:
    def test_init(self):
        abl = MultiHasherLogger()
        logger = abl()
        assert logger.name == "MultiHasherLogger"
        # Check some default kwargs
        # EasyLogger sets up handlers, we can check if it has any
        assert logger.hasHandlers()

    def test_call_returns_logger(self):
        abl = MultiHasherLogger()
        logger = abl()
        assert isinstance(logger, logging.Logger)


class TestSetupLogger:
    def test_instantiation_raises_type_error(self):
        with pytest.raises(TypeError, match="SetupLogger cannot be instantiated"):
            MultiHasherSetupLogger()

    def test_setup_logger_default(self):
        logger = MultiHasherSetupLogger.setup_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == "MultiHasherLogger"

    def test_setup_logger_custom_name(self):
        # If we don't pass a logger, it uses MultiHasherLogger which defaults to 'MultiHasherLogger'
        # But _check_fallback_logger_config uses default_logger_name if no logger passed to it.
        # Actually SetupLogger.setup_logger calls MultiHasherLogger(**kwargs)() if no logger.
        logger = MultiHasherSetupLogger.setup_logger(project_name="TestProject")
        # MultiHasherLogger sets logger.name = self.__class__.__name__ (MultiHasherLogger)
        assert logger.name == "MultiHasherLogger"

    def test_check_fallback_logger_config_with_logger(self):
        custom_logger = logging.getLogger("Custom")
        logger = MultiHasherSetupLogger._check_fallback_logger_config(logger=custom_logger)
        assert logger == custom_logger
        assert logger.name == "Custom"

    def test_check_fallback_logger_config_no_handlers(self):
        # Create a logger with no handlers
        # Using a truly unique name to avoid interference
        import uuid
        unique_name = f"NoHandlers_{uuid.uuid4().hex}"
        no_handler_logger = logging.getLogger(unique_name)
        no_handler_logger.handlers = []
        no_handler_logger.propagate = False

        import unittest.mock as mock
        # We need to mock logging.basicConfig as it's called by the fallback logic
        with mock.patch("logging.basicConfig") as mock_basic_config:
            # We also mock info to verify the fallback message is logged
            with mock.patch.object(no_handler_logger, 'info') as mock_info:
                logger = MultiHasherSetupLogger._check_fallback_logger_config(logger=no_handler_logger)

        assert logger == no_handler_logger
        mock_basic_config.assert_called_once()
        # Check if any call to info contains "using basic config"
        found = False
        for call in mock_info.call_args_list:
            if "using basic config" in call.args[0]:
                found = True
                break
        assert found, f"Expected 'using basic config' in logs, got {mock_info.call_args_list}"

    def test_setup_logger_returns_logger(self):
        logger = MultiHasherSetupLogger.setup_logger(return_wrapper_instance=True)
        assert isinstance(logger, logging.Logger)
