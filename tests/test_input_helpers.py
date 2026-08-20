import builtins

# noinspection PyProtectedMember
from MultiHasherMatchAJM.MatchAndRecord.factory import _InputHelpers


class TestInputHelpers:
    def test_input_type_str_non_pathlike(self):
        assert _InputHelpers._input_type_str(5) == "int"

    def test_input_type_str_for_file(self, tmp_path):
        p = tmp_path / "a.json"
        p.write_text("{}")
        assert _InputHelpers._input_type_str(p) == ".json file"

    def test_input_type_str_for_directory(self, tmp_path):
        d = tmp_path / "dir"
        d.mkdir()
        assert _InputHelpers._input_type_str(d) == "directory"

    def test_is_json_input(self, tmp_path):
        # dict/list are json inputs
        assert _InputHelpers._is_json_input({"a": 1}) is True
        assert _InputHelpers._is_json_input([{"a": 1}]) is True

        # path with .json suffix and exists
        p = tmp_path / "b.json"
        p.write_text("{}")
        assert _InputHelpers._is_json_input(p) is True

        # non-json file
        p2 = tmp_path / "b.txt"
        p2.write_text("hi")
        assert _InputHelpers._is_json_input(p2) is False

    def test_is_archive_input(self, tmp_path):
        zip_p = tmp_path / "c.zip"
        zip_p.touch()
        assert _InputHelpers._is_archive_input(zip_p) is True

        other = tmp_path / "c.bin"
        other.touch()
        assert _InputHelpers._is_archive_input(other) is False

    def test_archive_file_types_fallback(self, monkeypatch):
        real_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "MultiHasherMatchAJM.Hasher.archive_hashers":
                raise ImportError("mocked import error")
            return real_import(name, globals, locals, fromlist, level)

        monkeypatch.setattr(builtins, "__import__", fake_import)
        types = _InputHelpers._archive_file_types()
        assert types == _InputHelpers.FALLBACK_ARCHIVE_TYPES
