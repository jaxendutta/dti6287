"""
Windows Spark Setup Script
Downloads winutils.exe and hadoop.dll from cdarlint/winutils (Hadoop 3.3.5)
and configures HADOOP_HOME in your .env file.

Only needs to be run once.

USAGE:
    uv run python scripts/setup_winutils.py
"""

import os
import sys
import urllib.request
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
HADOOP_VERSION  = "hadoop-3.3.5"
HADOOP_HOME     = Path("C:/hadoop")
HADOOP_BIN      = HADOOP_HOME / "bin"
ENV_FILE        = Path(__file__).parent.parent / ".env"

BASE_URL = f"https://github.com/cdarlint/winutils/raw/master/{HADOOP_VERSION}/bin"
FILES    = ["winutils.exe", "hadoop.dll"]

# ─────────────────────────────────────────────────────────────────────────────

def check_platform() -> None:
    if sys.platform != "win32":
        print("This script is only needed on Windows. Exiting.")
        sys.exit(0)


def download_file(url: str, dest: Path) -> None:
    print(f"  Downloading {dest.name}...", end=" ", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
        f.write(r.read())
    print(f"OK ({dest.stat().st_size // 1024} KB)")


def setup_hadoop() -> None:
    print(f"Creating {HADOOP_BIN}...")
    HADOOP_BIN.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        dest = HADOOP_BIN / filename
        if dest.exists():
            print(f"  {filename} already exists, skipping.")
            continue
        url = f"{BASE_URL}/{filename}"
        download_file(url, dest)

    print(f"\nHadoop binaries installed to: {HADOOP_HOME}")


def update_env() -> None:
    """Add or update HADOOP_HOME in .env file."""
    env_text = ENV_FILE.read_text() if ENV_FILE.exists() else ""

    hadoop_line = f"HADOOP_HOME={HADOOP_HOME.as_posix()}"

    if "HADOOP_HOME" in env_text:
        lines = env_text.splitlines()
        lines = [hadoop_line if l.startswith("HADOOP_HOME") else l for l in lines]
        ENV_FILE.write_text("\n".join(lines) + "\n")
        print(f"Updated HADOOP_HOME in {ENV_FILE.name}")
    else:
        with open(ENV_FILE, "a") as f:
            f.write(f"\n{hadoop_line}\n")
        print(f"Added HADOOP_HOME to {ENV_FILE.name}")


def main() -> None:
    check_platform()
    print("=== Windows Spark Setup ===\n")
    setup_hadoop()
    update_env()
    print("\nDone.")


if __name__ == "__main__":
    main()