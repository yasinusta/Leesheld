"""Check upgrading an installed original v2 PWA without clearing progress.
Requires the original commit in the local Git clone and Playwright WebKit.
"""
import asyncio
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
from playwright.async_api import async_playwright

repo=Path(__file__).resolve().parents[1]
original='d818b586af3703e1aa25becf1ac29b2a6f2865bb'
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*_): pass

async def run():
    with tempfile.TemporaryDirectory(prefix='leesheld-upgrade-') as temp:
        root=Path(temp)
        files=subprocess.check_output(['git','ls-tree','-r','--name-only',original,'Leesheld_PWA_GitHub'],cwd=repo,text=True).splitlines()
        for name in files:
            path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(subprocess.check_output(['git','show',original+':'+name],cwd=repo))
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(root)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            async with async_playwright() as p:
                browser=await p.webkit.launch(headless=True)
                context=await browser.new_context(viewport={'width':820,'height':1180},is_mobile=True,has_touch=True)
                page=await context.new_page()
                url=f'http://127.0.0.1:{server.server_port}/Leesheld_PWA_GitHub/'
                await page.goto(url)
                await page.evaluate('navigator.serviceWorker.ready')
                await page.wait_for_function('!!navigator.serviceWorker.controller')
                await page.reload()
                assert await page.locator('#letterSounds').count()==0
                await page.evaluate("localStorage.setItem('leesheld3',JSON.stringify({stars:42,seen:{doos:1},errors:{},tests:[]}))")
                current=repo/'Leesheld_PWA_GitHub'
                for source in current.rglob('*'):
                    if not source.is_file() or any(part in ('models','.piper-venv','__pycache__') for part in source.relative_to(current).parts): continue
                    target=root/'Leesheld_PWA_GitHub'/source.relative_to(current)
                    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
                await page.evaluate("""async()=>{
                  const reg=await navigator.serviceWorker.ready;
                  const changed=new Promise(resolve=>navigator.serviceWorker.addEventListener('controllerchange',resolve,{once:true}));
                  await reg.update();await changed;
                }""")
                await page.reload()
                assert await page.locator('#letterSounds button').count()==5
                assert await page.locator('#stars').inner_text()=='⭐ 42'
                assert await page.evaluate("(async()=>!(await caches.keys()).includes('leesheld-v2'))()")
                await context.set_offline(True)
                await page.reload()
                assert await page.locator('#letterSounds button').count()==5
                assert await page.locator('#stars').inner_text()=='⭐ 42'
                print('PASS: originele v2-cache bijgewerkt; nieuwe app offline geopend; voortgang met 42 sterren behouden.',flush=True)
                await browser.close()
        finally:server.shutdown()

asyncio.run(run())
