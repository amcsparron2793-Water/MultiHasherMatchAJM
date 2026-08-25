import json
from logging import getLogger

from MultiHasherMatchAJM.MatchAndRecord import ComparerFactory


class TestPathHelper:
    TEST_SRC_NON_PATH_VALUE = 123
    TEST_SRC_PATH_VALUE = "source.json"

    def test_source_path_exists_true(self, tmp_path):
        source_json = {"a": 1}
        source_p = tmp_path / self.__class__.TEST_SRC_PATH_VALUE
        source_p.write_text(json.dumps(source_json))
        assert ComparerFactory._source_path_exists(source_p) is True

    def test_source_path_exists_false(self, tmp_path):
        source_p = tmp_path / self.__class__.TEST_SRC_PATH_VALUE
        assert ComparerFactory._source_path_exists(source_p) is False

    def test_source_is_not_path_defaults_true(self):
        assert ComparerFactory._source_path_exists(self.__class__.TEST_SRC_NON_PATH_VALUE) is True

    def test_source_is_not_path_logs_debug(self, caplog):
        """
        Tests that the function `_source_path_exists` logs a debug statement when the input
        source is not a Path-like object. The test verifies that the appropriate debug
        message is recorded in the log under the given logging level.

        :param caplog: A fixture that captures and asserts log messages.
        :type caplog: CapLog
        :return: None
        :rtype: None
        """
        # purely redefined for code readability
        test_src = self.__class__.TEST_SRC_NON_PATH_VALUE
        with caplog.at_level(10):
            # noinspection PyTypeChecker
            ComparerFactory._source_path_exists(test_src, logger=getLogger("test"))
        assert f'source {test_src} is not a PathLike object, returning True' in caplog.messages[0]
