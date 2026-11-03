"""Generate the complete, versioned audio pack; run with the Piper virtualenv."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import wave

import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

BASE = Path(__file__).resolve().parent
LETTERS = {"d": "d", "oe": "u", "z": "z", "ij": "ɛɪ", "h": "h"}


def sources():
    html = (BASE / "index.html").read_text(encoding="utf-8")
    section = html.split("const sheets={", 1)[1].split("};", 1)[0]
    sheets = re.findall(r"'([a-z]+)':\{top:`([^`]+)`,bottom:`([^`]+)`,story:`([^`]+)`\}", section)
    if {s[0] for s in sheets} != set(LETTERS):
        raise ValueError("De vijf werkbladen konden niet volledig worden gelezen")
    words = sorted({w for _, top, bottom, _ in sheets for w in re.split(r"[|\s]+", top + "|" + bottom) if w})
    items = {w: {"text": w, "kind": "word", "scale": 1.35} for w in words}
    for key, _, _, story in sheets:
        items["verhaal_" + key] = {"text": story.replace("\\n", "\n").replace("mmmm", "[[mː]]"), "kind": "story", "scale": 1.25}
    for key, ipa in LETTERS.items():
        # A stop /d/ is short. Never add a vowel (duh/dee) to lengthen it.
        items["klank_" + key] = {"text": "[[" + ipa + "]]", "kind": "phoneme", "scale": 1.65 if key in ("oe", "z", "ij") else 1.0}
    for key, ipa in zip("abcd", ("aː", "beː", "seː", "deː")):
        items["optie_" + key] = {"text": "Optie [[" + ipa + "]]", "kind": "label", "scale": 1.2}
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Genereer alles opnieuw")
    args = parser.parse_args()
    lock = json.loads((BASE / "voice-lock.json").read_text())
    for name, expected in lock["files"].items():
        path = BASE / "models" / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit("Stemmodel ontbreekt of wijkt af: " + name + ". Gebruik Maak_AI_stem.command.")
    voice = PiperVoice.load(BASE / "models" / "nl_NL-pim-medium.onnx")
    items = sources()
    audio_dir = BASE / "audio"
    audio_dir.mkdir(exist_ok=True)
    audit_path = BASE / "audio-audit.json"
    previous = json.loads(audit_path.read_text()) if audit_path.exists() else {}
    records = {}
    for i, (key, item) in enumerate(sorted(items.items()), 1):
        config = SynthesisConfig(length_scale=item["scale"], noise_scale=0.5, noise_w_scale=0.65, volume=0.85)
        fingerprint = hashlib.sha256(json.dumps({"item": item, "model": lock, "generator": 1, "piper": "1.4.2"}, sort_keys=True).encode()).hexdigest()
        out = audio_dir / (key + ".wav")
        old = previous.get(key, {})
        if args.force or not out.exists() or old.get("input_sha256") != fingerprint or hashlib.sha256(out.read_bytes()).hexdigest() != old.get("sha256"):
            chunks = []
            for line in item["text"].splitlines():
                chunks.extend(c.audio_float_array for c in voice.synthesize(line, syn_config=config))
                chunks.append(np.zeros(int(voice.config.sample_rate * 0.32), dtype=np.float32))
            audio = np.concatenate(chunks)
            audio = np.concatenate([np.zeros(int(voice.config.sample_rate * 0.08)), audio])
            pcm = (np.clip(audio, -0.98, 0.98) * 32767).astype("<i2")
            temp = out.with_suffix(".tmp.wav")
            with wave.open(str(temp), "wb") as wav:
                wav.setparams((1, 2, voice.config.sample_rate, 0, "NONE", "not compressed"))
                wav.writeframes(pcm.tobytes())
            temp.replace(out)
        with wave.open(str(out)) as wav:
            duration = wav.getnframes() / wav.getframerate()
            pcm = np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2")
        if duration < 0.15 or np.max(np.abs(pcm.astype(float))) < 300:
            raise ValueError("Lege of onbruikbare opname: " + key)
        records[key] = {**item, "phonemes": voice.phonemize(item["text"]), "seconds": round(duration, 3), "bytes": out.stat().st_size, "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "input_sha256": fingerprint}
        print(f"{i}/{len(items)}: {key} ({duration:.2f}s)", flush=True)
    audit_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = ["audio/" + key + ".wav" for key in sorted(records)]
    (BASE / "audio-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    pack_hash = hashlib.sha256(audit_path.read_bytes()).hexdigest()[:16]
    (BASE / "audio-version.js").write_text("self.LEESHELD_AUDIO_VERSION = '" + pack_hash + "';\n")
    print(f"Gereed: {len(records)} bestanden, {sum(r['bytes'] for r in records.values()) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
