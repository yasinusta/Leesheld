importScripts('./audio-version.js');
const PREFIX = 'leesheld-' + encodeURIComponent(new URL(self.registration.scope).pathname) + '-';
const CORE = PREFIX + 'core-v5-' + self.LEESHELD_AUDIO_VERSION;
const AUDIO = PREFIX + 'audio-' + self.LEESHELD_AUDIO_VERSION;
const FILES = ['./', './index.html', './audio-player.js', './audio-version.js', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './audio-manifest.json', './audio-audit.json'];
const absolute = path => new URL(path, self.registration.scope).href;
self.addEventListener('install', event => event.waitUntil((async () => {
  const cache = await caches.open(CORE);
  await cache.addAll(FILES.map(path => new Request(absolute(path), {cache:'reload'})));
  await self.skipWaiting();
})()));
self.addEventListener('activate', event => event.waitUntil((async () => {
  const names = await caches.keys();
  await Promise.all(names.filter(name => (name.startsWith(PREFIX) && name !== CORE && name !== AUDIO) || name === 'leesheld-v2').map(name => caches.delete(name)));
  await self.clients.claim();
})()));

function rangeResponse(response, header) {
  return (async () => {
    const match = /^bytes=(\d*)-(\d*)$/.exec(header || '');
    // A server may ignore malformed/multiple ranges and send the full response.
    if (!match || (!match[1] && !match[2])) return response;
    const data = await response.arrayBuffer(), size = data.byteLength;
    const start = match[1] ? Number(match[1]) : Math.max(0, size - Number(match[2]));
    const end = match[1] ? (match[2] ? Math.min(Number(match[2]), size-1) : size-1) : size-1;
    const headers = new Headers(response.headers);
    headers.set('Accept-Ranges', 'bytes');
    if (start >= size || start > end || (!match[1] && Number(match[2]) === 0)) {
      headers.set('Content-Range', 'bytes */' + size); headers.set('Content-Length', '0');
      return new Response(null, {status:416, headers});
    }
    headers.set('Content-Range', `bytes ${start}-${end}/${size}`);
    headers.set('Content-Length', String(end-start+1));
    return new Response(data.slice(start,end+1), {status:206, headers});
  })();
}
async function audioResponse(request) {
  const cache = await caches.open(AUDIO);
  const url = new URL(request.url); url.search = '';
  let response = await cache.match(url.href);
  if (!response) {
    // Always fetch/cache the whole file, even when Safari requests two bytes.
    response = await fetch(new Request(url.href, {cache:'no-store'}));
    if (response.status === 200) await cache.put(url.href, response.clone());
  }
  if (response.ok && request.headers.has('Range')) return rangeResponse(response, request.headers.get('Range'));
  return response;
}
self.addEventListener('fetch', event => {
  const request = event.request, url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || !url.href.startsWith(self.registration.scope)) return;
  if (url.pathname.startsWith(new URL('audio/', self.registration.scope).pathname)) {
    event.respondWith(audioResponse(request).catch(() => new Response('Opname niet offline beschikbaar', {status:503, headers:{'Content-Type':'text/plain; charset=utf-8'}}))); return;
  }
  event.respondWith((async () => {
    const cache = await caches.open(CORE);
    const cached = request.mode === 'navigate' ? await cache.match(absolute('./index.html')) : await cache.match(request, {ignoreSearch:true});
    return cached || fetch(request);
  })());
});

let downloading = false;
self.addEventListener('message', event => {
  if (event.data?.type !== 'DOWNLOAD_AUDIO' || !event.ports[0]) return;
  const port = event.ports[0];
  event.waitUntil((async () => {
    if (downloading) { port.postMessage({error:'Een download is al bezig. Probeer het straks opnieuw.'}); return; }
    downloading = true;
    try {
      const core = await caches.open(CORE);
      const files = await (await core.match(absolute('audio-manifest.json'))).json();
      const audit = await (await core.match(absolute('audio-audit.json'))).json();
      if (!Array.isArray(files) || !files.length) throw Error('Geen audio aanwezig');
      const cache = await caches.open(AUDIO);
      let done = 0;
      for (const file of files) {
        if (!/^audio\/[a-z_]+\.wav$/.test(file)) throw Error('Ongeldig audiobestand');
        const key = file.slice(6,-4), meta = audit[key], url = absolute(file);
        if (!meta) throw Error('Audiogegevens ontbreken: ' + file);
        let response = await cache.match(url);
        if (!response) {
          const controller = new AbortController();
          const timeout = setTimeout(() => controller.abort(), 20000);
          try { response = await fetch(url, {cache:'no-store', signal:controller.signal}); }
          finally { clearTimeout(timeout); }
        }
        if (response.status !== 200) throw Error('Opname ontbreekt: ' + file);
        const data = await response.clone().arrayBuffer();
        const digest = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',data)), b => b.toString(16).padStart(2,'0')).join('');
        if (data.byteLength !== meta.bytes || digest !== meta.sha256) {
          await cache.delete(url);
          throw Error('Opname is onvolledig. Probeer de download opnieuw: ' + file);
        }
        await cache.put(url,response);
        port.postMessage({done:++done,total:files.length});
      }
      port.postMessage({complete:true,total:files.length});
    } catch (error) {
      port.postMessage({error:error.name === 'QuotaExceededError' ? 'Er is te weinig opslagruimte. Maak ruimte vrij en probeer opnieuw.' : error.name === 'AbortError' ? 'Download onderbroken. Houd de app open en probeer opnieuw.' : String(error.message || error)});
    } finally { downloading = false; port.close(); }
  })());
});
