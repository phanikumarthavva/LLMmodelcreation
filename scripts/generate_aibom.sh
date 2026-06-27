#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="${MODEL_ID:-distilgpt2}"
REPORTS_DIR="${GITHUB_WORKSPACE:-.}/reports"
AIBOM_OUT="${REPORTS_DIR}/aibom-${MODEL_ID//\//-}.json"

mkdir -p "${REPORTS_DIR}"

echo "Generating AIBOM for Hugging Face model: ${MODEL_ID}"

git clone --depth 1 https://github.com/GenAI-Security-Project/aibom-generator.git /tmp/aibom-generator
python -m pip install -r /tmp/aibom-generator/requirements.txt

cd /tmp/aibom-generator
python -m src.cli "${MODEL_ID}" --output "${AIBOM_OUT}" --verbose

echo "AIBOM written to ${AIBOM_OUT}"
