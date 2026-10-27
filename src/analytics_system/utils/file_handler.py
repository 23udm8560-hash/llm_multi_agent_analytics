from pathlib import Path
import re

UPLOAD_DIR = Path("data/uploads")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("data/reports")
for folder in (UPLOAD_DIR, PROCESSED_DIR, REPORT_DIR):
    folder.mkdir(parents=True, exist_ok=True)


def safe_filename(name: str) -> str:
    name = Path(name).name
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return name[:120] or "dataset.csv"
