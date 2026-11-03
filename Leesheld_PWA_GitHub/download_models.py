"""Download the pinned CC0 voice, verify checksums, then install atomically."""
import hashlib
import json
from pathlib import Path
import urllib.request

base = Path(__file__).resolve().parent
lock = json.loads((base / 'voice-lock.json').read_text())
models = base / 'models'
models.mkdir(exist_ok=True)
for name, expected in lock['files'].items():
    target = models / name
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
        continue
    url = f"https://huggingface.co/{lock['repository']}/resolve/{lock['revision']}/nl/nl_NL/pim/medium/{name}"
    print('Download:', name, flush=True)
    temp = target.with_suffix(target.suffix + '.part')
    try:
        with urllib.request.urlopen(url, timeout=60) as response, temp.open('wb') as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)
        if hashlib.sha256(temp.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Checksum wijkt af: ' + name)
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)
print('Stemmodel gecontroleerd.')
