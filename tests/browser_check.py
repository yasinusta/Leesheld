"""Real WebKit integration: pip install playwright; playwright install webkit.
Run from the repository: python3 tests/browser_check.py
"""
import asyncio, json, os, tempfile, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.async_api import async_playwright

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO/'test-results'
ROOT.mkdir(exist_ok=True)
profile = tempfile.TemporaryDirectory(prefix='leesheld-webkit-')
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
server = ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(REPO)))
threading.Thread(target=server.serve_forever,daemon=True).start()
URL=f'http://127.0.0.1:{server.server_port}/Leesheld_PWA_GitHub/'
results=[]

def check(name, value):
    assert value, name
    results.append(name)
    print('PASS:',name,flush=True)

async def run():
    async with async_playwright() as p:
        context=await p.webkit.launch_persistent_context(profile.name,headless=True,viewport={'width':820,'height':1180},is_mobile=True,has_touch=True)
        page=context.pages[0]
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(URL)
        await page.evaluate('navigator.serviceWorker.ready')
        await page.wait_for_function('navigator.serviceWorker.controller !== null')
        check('Serviceworker actief op submappad',True)
        await page.click('#letterSounds button:nth-child(2)')
        await page.wait_for_function("voice.buffers.has('klank_oe')")
        await page.wait_for_function('voice.source === null')
        check('Echte klankopname gedecodeerd en afgespeeld na tik',await page.locator('#audioStatus').inner_text()=='')
        await page.evaluate("start('d')")
        await page.click('#controls button:first-child')
        await page.wait_for_timeout(40)
        await page.click('button:has-text("ABCD luisteren")')
        await page.evaluate("window.played=[];const originalLoad=voice.load.bind(voice);voice.load=async(...args)=>{played.push(args[0]);return originalLoad(...args)};true")
        await page.click('button:has-text("Alle keuzes horen")')
        await page.wait_for_function('played.length === 8 && voice.source === null',timeout=30000)
        check('ABCD speelt vier gesproken labels en vier woorden op volgorde',await page.evaluate("JSON.stringify(played)===JSON.stringify(options.flatMap((_,i)=>optionKeys(i)))"))
        check('ABCD toont uitsluitend letters, ook in toegankelijke labels',await page.evaluate("[...document.querySelectorAll('.choice')].every((b,i)=>b.textContent.trim()==='ABCD'[i]+' 🔊'&&b.getAttribute('aria-label')==='Luister naar antwoord '+'ABCD'[i])"))
        await page.click('#c0')
        check('Eerste tik luistert; nog geen beoordeling',await page.evaluate('!answered'))
        await page.click('#c0')
        check('Tweede tik bevestigt keuze',await page.evaluate('answered'))
        await page.evaluate("start('test')")
        check('Toets verbergt woordhulp en sterren',await page.locator('#controls').is_hidden() and await page.locator('#stars').is_hidden())
        correct=await page.evaluate('options.indexOf(queue[index].word)')
        await page.click('#c'+str(correct));await page.click('#c'+str(correct))
        check('Toets lekt geen juistheid via kleur of feedback',await page.locator('.correct,.wrong').count()==0 and await page.locator('#feedback').inner_text()=='Antwoord opgeslagen.' and await page.locator('#stars').is_hidden())
        # Cancellation during loading/playback must not revive an old sequence.
        await page.evaluate("start('mix');showChoices();played=[]")
        await page.click('button:has-text("Alle keuzes horen")')
        await page.wait_for_timeout(100)
        await page.click('button:has-text("⌂ Menu")')
        count=await page.evaluate('played.length')
        await page.wait_for_timeout(2200)
        check('Menu annuleert de hele afspeellijst',await page.evaluate('voice.source===null') and await page.evaluate('played.length')==count)
        # Offline before downloading must report failure rather than success.
        await context.set_offline(True)
        await page.click('#downloadButton')
        await page.wait_for_function("!offlineBusy && document.querySelector('#offlineStatus').textContent.includes('⚠️')")
        check('Onvolledige offline-download wordt als fout gemeld',True)
        await context.set_offline(False)
        await page.click('#downloadButton')
        await page.wait_for_function("!offlineBusy && document.querySelector('#offlineStatus').textContent.includes('✅')",timeout=90000)
        check('Alle 154 bestanden gedownload en SHA-256 gecontroleerd', '154' in await page.locator('#offlineStatus').inner_text())
        await context.set_offline(True)
        await page.reload()
        await page.wait_for_selector('#letterSounds button')
        count=await page.evaluate("(async()=>{let n=0;const manifest=await(await fetch('audio-manifest.json')).json();const c=new AudioContext();for(const f of manifest){const r=await fetch(f);if(!r.ok)throw Error(f);await c.decodeAudioData(await r.arrayBuffer());n++}await c.close();return n})()")
        check('Alle 154 WAV-bestanden offline gedecodeerd in WebKit',count==154)
        ranges=await page.evaluate("""(async()=>{
          const url='audio/doos.wav';const full=await(await fetch(url)).arrayBuffer();const out=[];
          for(const range of ['bytes=0-1','bytes=100-','bytes=-12','bytes=0-99999999','bytes=99999999-','bytes=-0']){
           const r=await fetch(url,{headers:{Range:range}});const b=await r.arrayBuffer();out.push({range,status:r.status,size:b.byteLength,contentRange:r.headers.get('Content-Range')});
          }return {size:full.byteLength,out};})()""")
        check('Safari bytebereiken en ongeldige bereiken correct offline', [x['status'] for x in ranges['out']]==[206,206,206,206,416,416] and ranges['out'][0]['size']==2 and ranges['out'][2]['size']==12 and ranges['out'][3]['size']==ranges['size'])
        await page.click('#letterSounds button:first-child')
        await page.wait_for_function("voice.buffers.has('klank_d')")
        await page.wait_for_function('voice.source===null')
        check('Klank afspelen na offline herladen',await page.locator('#audioStatus').inner_text()=='')
        await page.evaluate("voice.play(['bestaat_niet'])")
        check('Ontbrekende audio meldt fout zonder apparaatstem',bool(await page.locator('#audioStatus').inner_text()))
        await page.screenshot(path=str(ROOT/'ipad-webkit.png'),full_page=True)
        if errors: print('Browser errors:',errors,flush=True)
        check('Geen JavaScript-fouten',not errors)
        await context.close()
        context=await p.webkit.launch_persistent_context(profile.name,headless=True,viewport={'width':820,'height':1180},is_mobile=True,has_touch=True,offline=True)
        page=context.pages[0]
        await page.goto(URL)
        check('Offline opnieuw openen na sluiten browser',await page.locator('h1').inner_text()=='🌟 Leesheld AI')
        await context.close()
    (ROOT/'browser-results.json').write_text(json.dumps({'checks':results,'rangeResponses':ranges,'errors':errors},ensure_ascii=False,indent=2))

try:
    asyncio.run(run())
finally:
    server.shutdown()
    profile.cleanup()
