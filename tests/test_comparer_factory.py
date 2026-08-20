import json
from MultiHasherMatchAJM.MatchAndRecord import ComparerFactory
from MultiHasherMatchAJM.MatchAndRecord.hash_comparers import (
    JsonToJsonHashComparer,
    JsonToArchiveComparer,
    ArchiveToArchiveComparer,
    JsonToDirectoryComparer,
    ArchiveToDirectoryComparer,
    DirectoryToDirectoryComparer,
)


def test_comparer_factory_mapping(tmp_path):
    # 1. JSON to JSON
    source_json = {"a": 1}
    target_json = {"a": 1}
    comparer = ComparerFactory(source=source_json, target=target_json)
    assert isinstance(comparer, JsonToJsonHashComparer)

    # 2. JSON Path to JSON dict
    source_p = tmp_path / "source.json"
    source_p.write_text(json.dumps(source_json))
    comparer = ComparerFactory(source=source_p, target=target_json)
    assert isinstance(comparer, JsonToJsonHashComparer)

    # 3. JSON to Archive
    archive_p = tmp_path / "test.zip"
    archive_p.touch()
    comparer = ComparerFactory(source=source_json, target=archive_p)
    assert isinstance(comparer, JsonToArchiveComparer)

    # 4. Archive to Archive
    archive_p2 = tmp_path / "test2.zip"
    archive_p2.touch()
    comparer = ComparerFactory(source=archive_p, target=archive_p2)
    assert isinstance(comparer, ArchiveToArchiveComparer)

    # 5. JSON to Directory
    dir_p = tmp_path / "some_dir"
    dir_p.mkdir()
    comparer = ComparerFactory(source=source_json, target=dir_p)
    assert isinstance(comparer, JsonToDirectoryComparer)

    # 6. Archive to Directory
    comparer = ComparerFactory(source=archive_p, target=dir_p)
    assert isinstance(comparer, ArchiveToDirectoryComparer)

    # 7. Directory to Directory
    source_dir = tmp_path / "source_dir"
    target_dir = tmp_path / "target_dir"
    source_dir.mkdir()
    target_dir.mkdir()
    comparer = ComparerFactory(source=source_dir, target=target_dir)
    assert isinstance(comparer, DirectoryToDirectoryComparer)

    # 8. Unsupported types should raise
    with pytest.raises(ValueError, match="Could not determine a comparer"):
        ComparerFactory(source=123, target=456)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
