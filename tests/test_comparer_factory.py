import json
import pytest
from MultiHasherMatchAJM.MatchAndRecord import ComparerFactory
from MultiHasherMatchAJM.MatchAndRecord.hash_comparers import (
    JsonToJsonHashComparer,
    JsonToArchiveComparer,
    ArchiveToArchiveComparer,
    JsonToDirectoryComparer,
    ArchiveToDirectoryComparer,
    DirectoryToDirectoryComparer,
)


class TestComparerFactory:
    def test_comparer_factory_json_to_json(self):
        source_json = {"a": 1}
        target_json = {"a": 1}
        comparer = ComparerFactory(source=source_json, target=target_json)
        assert isinstance(comparer, JsonToJsonHashComparer)

    def test_comparer_factory_json_path_to_json(self, tmp_path):
        source_json = {"a": 1}
        target_json = {"a": 1}
        source_p = tmp_path / "source.json"
        source_p.write_text(json.dumps(source_json))
        comparer = ComparerFactory(source=source_p, target=target_json)
        assert isinstance(comparer, JsonToJsonHashComparer)

    def test_comparer_factory_json_to_archive(self, tmp_path):
        source_json = {"a": 1}
        archive_p = tmp_path / "test.zip"
        archive_p.touch()
        comparer = ComparerFactory(source=source_json, target=archive_p)
        assert isinstance(comparer, JsonToArchiveComparer)

    def test_comparer_factory_archive_to_archive(self, tmp_path):
        archive_p = tmp_path / "test.zip"
        archive_p.touch()
        archive_p2 = tmp_path / "test2.zip"
        archive_p2.touch()
        comparer = ComparerFactory(source=archive_p, target=archive_p2)
        assert isinstance(comparer, ArchiveToArchiveComparer)

    def test_comparer_factory_json_to_directory(self, tmp_path):
        source_json = {"a": 1}
        dir_p = tmp_path / "some_dir"
        dir_p.mkdir()
        comparer = ComparerFactory(source=source_json, target=dir_p)
        assert isinstance(comparer, JsonToDirectoryComparer)

    def test_comparer_factory_archive_to_directory(self, tmp_path):
        archive_p = tmp_path / "test.zip"
        archive_p.touch()
        dir_p = tmp_path / "some_dir"
        dir_p.mkdir()
        comparer = ComparerFactory(source=archive_p, target=dir_p)
        assert isinstance(comparer, ArchiveToDirectoryComparer)

    def test_comparer_factory_directory_to_directory(self, tmp_path):
        source_dir = tmp_path / "source_dir"
        target_dir = tmp_path / "target_dir"
        source_dir.mkdir()
        target_dir.mkdir()
        comparer = ComparerFactory(source=source_dir, target=target_dir)
        assert isinstance(comparer, DirectoryToDirectoryComparer)

    def test_comparer_factory_unsupported_types(self):
        with pytest.raises(ValueError, match="Could not determine a comparer"):
            ComparerFactory(source=123, target=456)


if __name__ == "__main__":
    pytest.main([__file__])
