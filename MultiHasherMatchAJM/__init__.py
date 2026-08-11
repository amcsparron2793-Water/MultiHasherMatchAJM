from pathlib import Path
from typing import Optional


def find_project_root(start: Optional[Path] = None, **kwargs) -> Path:
    start: Path = start or Path(__file__).resolve()
    marker_file = kwargs.get("marker_file", "setup.py")

    for path in [start, *start.parents]:
        if (path / marker_file).exists():
            return path

    raise FileNotFoundError(f"Could not find project root containing {marker_file}")


PROJECT_ROOT = find_project_root()
MISC_PROJECT_DIR = PROJECT_ROOT / "Misc_Project_Files"
MANUAL_TEST_FILE_LOCATION = Path(MISC_PROJECT_DIR, 'manual_testing_files')

from MultiHasherMatchAJM.Utilities.multihasher_logger import MultiHasherLogger, MultiHasherSetupLogger
from MultiHasherMatchAJM import Hasher, MatchAndRecord, Utilities
