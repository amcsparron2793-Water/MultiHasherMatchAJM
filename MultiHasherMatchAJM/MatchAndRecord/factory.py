from pathlib import Path
from typing import Any

from MultiHasherMatchAJM import SetupLogger
from MultiHasherMatchAJM.MatchAndRecord import hash_comparers


class ComparerFactory:
    FALLBACK_ARCHIVE_TYPES = ['.zip', '.tar', '.tar.gz', '.tar.bz2', '.7z', '.rar']

    @classmethod
    def _is_json_input(cls, val: Any) -> bool:
        if isinstance(val, (dict, list)):
            return True
        if isinstance(val, (str, Path)):
            p = Path(val)
            try:
                return p.is_file() and p.suffix.lower() == '.json'
            except OSError:
                return False
        return False

    @classmethod
    def _is_archive_input(cls, val: Any) -> bool:
        if isinstance(val, (str, Path)):
            p = Path(val)
            try:
                # Use a local import or hardcode the list if necessary to avoid circular import
                from MultiHasherMatchAJM.Hasher.archive_hashers import ArchiveFileHasher
                return p.is_file() and p.suffix.lower() in ArchiveFileHasher.ARCHIVE_FILE_TYPES
            except (OSError, ImportError):
                # Fallback to common archive types if import fails or other error
                return p.is_file() and p.suffix.lower() in cls.FALLBACK_ARCHIVE_TYPES
        return False

    @classmethod
    def _is_directory_input(cls, val: Any) -> bool:
        if isinstance(val, (str, Path)):
            p = Path(val)
            try:
                return p.is_dir()
            except OSError:
                return False
        return False

    @classmethod
    def inst_comparer_class(cls, source: Any, target: Any, **kwargs):
        # Determine types
        is_source_json = cls._is_json_input(source)
        is_source_archive = cls._is_archive_input(source)
        
        is_target_json = cls._is_json_input(target)
        is_target_archive = cls._is_archive_input(target)
        is_target_dir = cls._is_directory_input(target)

        if is_source_json:
            if is_target_json:
                return hash_comparers.JsonToJsonHashComparer(source_json=source, target_json=target, **kwargs)
            elif is_target_archive:
                return hash_comparers.JsonToArchiveComparer(source_json=source, archive_file=Path(target), **kwargs)
            elif is_target_dir:
                return hash_comparers.JsonToDirectoryComparer(source_json=Path(source) if isinstance(source, (str, Path)) else source, 
                                                              target_dir=Path(target), **kwargs)
        
        if is_source_archive:
            if is_target_archive:
                return hash_comparers.ArchiveToArchiveComparer(source_archive_file=Path(source), 
                                                               target_archive_file=Path(target), **kwargs)

        raise ValueError(f"Could not determine a comparer for source type {type(source)} and target type {type(target)}")

    def __new__(cls, source: Any, target: Any, **kwargs):
        kwargs["logger"] = SetupLogger.setup_logger(**kwargs)
        return cls.inst_comparer_class(source, target, **kwargs)


if __name__ == "__main__":
    from MultiHasherMatchAJM import MANUAL_TEST_FILE_LOCATION
    # Example usage (would need actual files to run)
    comparer = ComparerFactory(source=Path(MANUAL_TEST_FILE_LOCATION / "Desktop_Backup.json"),
                               target=Path("~/Desktop").expanduser())
    print(type(comparer))
