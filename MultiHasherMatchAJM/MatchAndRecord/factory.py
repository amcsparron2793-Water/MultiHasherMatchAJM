from os import PathLike
from pathlib import Path
from typing import Any, Optional

from MultiHasherMatchAJM import SetupLogger
from MultiHasherMatchAJM.MatchAndRecord import hash_comparers


class _PathHelpers:
    @staticmethod
    def _as_path(value: Any) -> Optional[Path]:
        if isinstance(value, (str, Path)):
            return Path(value)
        return None

    @staticmethod
    def _path_exists_as(path: Path, predicate_name: str) -> bool:
        try:
            return getattr(path, predicate_name)()
        except OSError:
            return False

    @classmethod
    def _json_source_for_path_consumer(cls, source: Any) -> Any:
        if isinstance(source, (str, Path)):
            return Path(source)
        return source


class _InputHelpers(_PathHelpers):
    FALLBACK_ARCHIVE_TYPES = ['.zip', '.tar', '.tar.gz', '.tar.bz2', '.7z', '.rar']
    JSON_SUFFIX = ".json"

    @classmethod
    def _input_type_str(cls, value: PathLike) -> str:
        path = cls._as_path(value)
        if path is None:
            return type(value).__name__

        if cls._is_archive_input(path):
            return f"{path.suffix} archive"

        if cls._path_exists_as(path, "is_file") or path.suffix:
            return f"{path.suffix} file"

        if cls._path_exists_as(path, "is_dir") or not path.suffix:
            return "directory"

        return "unknown"

    @classmethod
    def _archive_file_types(cls) -> list[str]:
        try:
            from MultiHasherMatchAJM.Hasher.archive_hashers import ArchiveFileHasher
            return ArchiveFileHasher.ARCHIVE_FILE_TYPES
        except ImportError:
            return cls.FALLBACK_ARCHIVE_TYPES

    @classmethod
    def _is_json_input(cls, value: Any) -> bool:
        if isinstance(value, (dict, list)):
            return True

        path = cls._as_path(value)
        return (
                path is not None
                and cls._path_exists_as(path, "is_file")
                and path.suffix.lower() == cls.JSON_SUFFIX
        )

    @classmethod
    def _is_archive_input(cls, value: Any) -> bool:
        path = cls._as_path(value)
        return (
                path is not None
                and cls._path_exists_as(path, "is_file")
                and path.suffix.lower() in cls._archive_file_types()
        )

    @classmethod
    def _is_directory_input(cls, value: Any) -> bool:
        path = cls._as_path(value)
        return path is not None and cls._path_exists_as(path, "is_dir")


class ComparerFactory(_InputHelpers):
    _JSON_SOURCE_JSON_TARGET_CLS = hash_comparers.JsonToJsonHashComparer
    _JSON_SOURCE_ARCHIVE_TARGET_CLS = hash_comparers.JsonToArchiveComparer
    _JSON_SOURCE_DIRECTORY_TARGET_CLS = hash_comparers.JsonToDirectoryComparer
    _ARCHIVE_SOURCE_ARCHIVE_TARGET_CLS = hash_comparers.ArchiveToArchiveComparer

    @classmethod
    def _json_src_targets(cls, source: Any, target: Any, **kwargs):
        target_is_json = cls._is_json_input(target)
        target_is_archive = cls._is_archive_input(target)
        target_is_directory = cls._is_directory_input(target)

        if target_is_json:
            return cls._JSON_SOURCE_JSON_TARGET_CLS(
                source_json=source,
                target_json=target,
                **kwargs,
            )

        if target_is_archive:
            return cls._JSON_SOURCE_ARCHIVE_TARGET_CLS(
                source_json=source,
                archive_file=Path(target),
                **kwargs,
            )

        if target_is_directory:
            return cls._JSON_SOURCE_DIRECTORY_TARGET_CLS(
                source_json=cls._json_source_for_path_consumer(source),
                target_dir=Path(target),
                **kwargs,
            )

        return None

    @classmethod
    def _archive_src_targets(cls, source: Any, target: Any, **kwargs):
        target_is_archive = cls._is_archive_input(target)
        if target_is_archive:
            return hash_comparers.ArchiveToArchiveComparer(
                source_archive_file=Path(source),
                target_archive_file=Path(target),
                **kwargs,
            )
        return None

    @classmethod
    def inst_comparer_class(cls, source: Any, target: Any, **kwargs):
        source_is_json = cls._is_json_input(source)
        source_is_archive = cls._is_archive_input(source)
        inst = None

        if source_is_json:
            inst = cls._json_src_targets(source, target, **kwargs)

        if source_is_archive:
            inst = cls._archive_src_targets(source, target, **kwargs)

        if inst:
            return inst

        raise ValueError(
            f"Could not determine a comparer for source type {cls._input_type_str(source)} "
            f"and target type {cls._input_type_str(target)}"
        )

    def __new__(cls, source: Any, target: Any, **kwargs):
        kwargs["logger"] = SetupLogger.setup_logger(**kwargs)
        return cls.inst_comparer_class(source, target, **kwargs)


if __name__ == "__main__":
    from MultiHasherMatchAJM import MANUAL_TEST_FILE_LOCATION
    # Example usage (would need actual files to run)
    # FIXME: target and source should both allow for directory inputs - currently only source allows for directories.
    comparer = ComparerFactory(target=Path(MANUAL_TEST_FILE_LOCATION / "Desktop_Backup.json"),
                               source=Path("~/Desktop").expanduser())
    print(type(comparer))
