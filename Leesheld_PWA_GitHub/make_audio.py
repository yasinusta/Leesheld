import re,subprocess, pathlib, json
base=pathlib.Path(__file__).resolve().parent
html=(base/'index.html').read_text()
# Lees de vijf werkbladen rechtstreeks uit de app.
section=html.split('const sheets={',1)[1].split('};',1)[0]
words=set(re.findall(r'[a-z]+', ' '.join(re.findall(r'(?:top|bottom):`([^`]+)`',section))))
stories=dict(re.findall(r"'([a-z]+)':\{top:`[^`]+`,bottom:`[^`]+`,story:`([^`]+)`\}",section))
model=base/'models/nl_NL-pim-medium.onnx'
if not model.exists():
    matches=list((base/'models').rglob('nl_NL-pim-medium.onnx'))
    if not matches: raise SystemExit('Piper-model niet gevonden')
    model=matches[0]
items={w:w for w in words}
for k,story in stories.items():items['verhaal_'+k]=story.replace('\\n',' ').replace('\n',' ')
for i,(key,text) in enumerate(sorted(items.items()),1):
    name=re.sub(r'[^a-z0-9]','_',key.lower()).strip('_')
    out=base/'audio'/(name+'.wav')
    if out.exists():continue
    print(f'{i}/{len(items)}: {key}',flush=True)
    subprocess.run(['python','-m','piper','--model',str(model),'--output_file',str(out)],input=text+'\n',text=True,check=True)
print(f'Gereed: {len(items)} audiobestanden.')

# Update precache list after audio generation.
audio_files=sorted('audio/'+f.name for f in (base/'audio').glob('*.wav'))
(base/'audio-manifest.json').write_text(json.dumps(audio_files,ensure_ascii=False,indent=2))
print('Audio manifest bijgewerkt:',len(audio_files))
