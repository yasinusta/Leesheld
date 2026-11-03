"""Offline pack integrity and coverage. Run: python3 tests/check_audio.py"""
import hashlib
import json
from pathlib import Path
import re
import struct
import wave

base = Path(__file__).resolve().parents[1] / 'Leesheld_PWA_GitHub'
html = (base/'index.html').read_text()
section = html.split('const sheets={',1)[1].split('};',1)[0]
sheets = re.findall(r"'([a-z]+)':\{top:`([^`]+)`,bottom:`([^`]+)`,story:`([^`]+)`\}",section)
assert {row[0] for row in sheets} == {'d','oe','z','ij','h'}
words = {w for _,top,bottom,_ in sheets for w in re.split(r'[|\s]+',top+'|'+bottom) if w}
expected = words | {'verhaal_'+row[0] for row in sheets} | {'klank_'+row[0] for row in sheets} | {'optie_'+k for k in 'abcd'}
audit = json.loads((base/'audio-audit.json').read_text())
manifest = json.loads((base/'audio-manifest.json').read_text())
assert set(audit) == expected
assert len(manifest) == len(expected) == 154
assert set(manifest) == {'audio/'+key+'.wav' for key in expected}
assert set(p.stem for p in (base/'audio').glob('*.wav')) == expected
for key, meta in audit.items():
    file = base/'audio'/(key+'.wav')
    raw = file.read_bytes()
    assert len(raw) == meta['bytes'],key
    assert hashlib.sha256(raw).hexdigest() == meta['sha256'],key
    with wave.open(str(file)) as audio:
        assert audio.getnchannels() == 1 and audio.getsampwidth() == 2 and audio.getframerate() == 22050,key
        duration = audio.getnframes()/audio.getframerate()
        assert abs(duration-meta['seconds']) < 0.001,key
        samples = struct.unpack('<'+'h'*audio.getnframes(),audio.readframes(audio.getnframes()))
    assert max(abs(x) for x in samples) > 300,key
    assert max(abs(x) for x in samples) < 32767,key
for key, ipa in {'d':'d','oe':'u','z':'z','ij':'ɛɪ','h':'h'}.items():
    assert audit['klank_'+key]['phonemes'] == [list(ipa)]
assert 'ˌɛm' not in str(audit['verhaal_ij']['phonemes'])
version = hashlib.sha256((base/'audio-audit.json').read_bytes()).hexdigest()[:16]
assert version in (base/'audio-version.js').read_text()
print(f'PASS: {len(words)} woorden + 5 verhalen + 5 klanken + 4 labels; alle bestanden, hashes, foneeminvoer, pieken en duren gecontroleerd.')
