#!/bin/bash
set -e
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then echo 'Installeer eerst Python 3 via python.org'; read -r; exit 1; fi
python3 -m venv .piper-venv
source .piper-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install piper-tts
mkdir -p models audio
python -m piper.download_voices nl_NL-pim-medium --data-dir models
python make_audio.py
printf '\nKLAAR! Open index.html in Safari op je Mac. Upload daarna alle bestanden uit deze map naar GitHub Pages (zie README_GITHUB_IPAD.md).\n'
read -r -p 'Druk op Enter om te sluiten.'
