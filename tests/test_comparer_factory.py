import json
from pathlib import Path
from MultiHasherMatchAJM.MatchAndRecord import ComparerFactory
from MultiHasherMatchAJM.MatchAndRecord.hash_comparers import (
    JsonToJsonHashComparer,
    JsonToArchiveComparer,
    ArchiveToArchiveComparer,
    JsonToDirectoryComparer
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

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
