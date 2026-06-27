"""Download the configured HF model and run ModelScan + PickleScan."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from huggingface_hub import snapshot_download

from app.model import MODEL_NAME

REPORTS_DIR = Path("reports")


def run(command: list[str]) -> None:
    print(f"\n>> {' '.join(command)}", flush=True)
    subprocess.run(command, check=True)


def main() -> int:
    REPORTS_DIR.mkdir(exist_ok=True)

    print(f"Model under test: {MODEL_NAME}")

    model_path = snapshot_download(MODEL_NAME)
    print(f"Downloaded to: {model_path}")

    modelscan_report = REPORTS_DIR / "modelscan.json"
    run(
        [
            "modelscan",
            "-p",
            str(model_path),
            "-r",
            "json",
            "-o",
            str(modelscan_report),
        ]
    )
    print(f"ModelScan report: {modelscan_report}")

    run(["picklescan", "--huggingface", MODEL_NAME])
    print("PickleScan: no malicious pickle patterns detected")

    print("\nAI model security scans passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
