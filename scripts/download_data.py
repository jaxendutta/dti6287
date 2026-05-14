"""
Download the airline on-time performance dataset from Kaggle.
No API key required.

USAGE:
    uv run python scripts/download_data.py
"""

import zipfile
import urllib.request
from bi.config import DOWNLOAD_URL, DOWNLOAD_ZIP, RAW_CSV, DATA_DIR


def download() -> None:
    print(f"Downloading dataset...")
    print(f"  From : {DOWNLOAD_URL}")
    print(f"  To   : {DOWNLOAD_ZIP}\n")

    req = urllib.request.Request(DOWNLOAD_URL, headers={"User-Agent": "Mozilla/5.0"})

    with urllib.request.urlopen(req) as response, open(DOWNLOAD_ZIP, "wb") as out:
        total      = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 64

        while chunk := response.read(chunk_size):
            out.write(chunk)
            downloaded += len(chunk)
            if total:
                print(f"\r  {downloaded / total * 100:.1f}%  ({downloaded // 1024 // 1024} MB)", end="", flush=True)

    print(f"\n  Saved: {DOWNLOAD_ZIP.name} ({DOWNLOAD_ZIP.stat().st_size // 1024 // 1024} MB)")


def extract() -> None:
    print(f"\nExtracting to {DATA_DIR}...")
    with zipfile.ZipFile(DOWNLOAD_ZIP, "r") as z:
        z.extractall(DATA_DIR)
    DOWNLOAD_ZIP.unlink()
    print(f"  Done. ZIP removed.")


def main() -> None:
    if RAW_CSV.exists():
        print(f"Already exists: {RAW_CSV.name} ({RAW_CSV.stat().st_size // 1024 // 1024} MB)")
        return

    download()
    extract()

    if RAW_CSV.exists():
        print(f"\nReady: {RAW_CSV.name} ({RAW_CSV.stat().st_size // 1024 // 1024} MB)")
    else:
        print(f"\nExtracted files in {DATA_DIR}:")
        for f in DATA_DIR.iterdir():
            print(f"  {f.name}")


if __name__ == "__main__":
    main()