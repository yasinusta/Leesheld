#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo 'Installeer eerst Python 3.10 of nieuwer via python.org.'
  read -r -p 'Druk op Enter om te sluiten.'
  exit 1
fi
python3 -m venv .piper-venv
.piper-venv/bin/python -m pip install 'piper-tts==1.4.2'
.piper-venv/bin/python download_models.py
.piper-venv/bin/python make_audio.py
printf '\nKLAAR! De volledige audio staat in audio/. Lees README_GITHUB_IPAD.md voor upload en de iPad-test.\n'
read -r -p 'Druk op Enter om te sluiten.'
