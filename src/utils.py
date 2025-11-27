# src/utils.py
import shutil
from pathlib import Path
from typing import List
import time

def ensure_folders(folders: List[str]):
    for f in folders:
        Path(f).mkdir(parents=True, exist_ok=True)

def archive_file(path: str, processed_folder: str) -> str:
    src = Path(path)
    dest_dir = Path(processed_folder)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    # if destination exists, add timestamp suffix
    if dest.exists():
        dest = dest_dir / f"{src.stem}_{int(time.time())}{src.suffix}"
    shutil.move(str(src), str(dest))
    return str(dest)
