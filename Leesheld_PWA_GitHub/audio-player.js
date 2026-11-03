/* A user gesture resumes Web Audio before asynchronous loading (iPad Safari). */
class RecordedVoice {
  constructor(report) {
    this.report = report;
    this.context = null;
    this.token = 0;
    this.source = null;
    this.finish = null;
    this.abort = null;
    this.buffers = new Map();
  }
  stop() {
    this.token++;
    if (this.abort) this.abort.abort();
    this.abort = null;
    if (this.source) { try { this.source.stop(); } catch {} }
    this.source = null;
    if (this.finish) this.finish(false);
    this.finish = null;
  }
  async load(key, signal) {
    if (!/^[a-z_]+$/.test(key)) throw Error('Onbekende opname');
    if (this.buffers.has(key)) return this.buffers.get(key);
    const response = await fetch(new URL('audio/' + key + '.wav', location.href), {signal});
    if (!response.ok) throw Error('Opname ontbreekt');
    const buffer = await this.context.decodeAudioData(await response.arrayBuffer());
    // Bound memory: stories can be much longer than individual words.
    if (this.buffers.size >= 32) this.buffers.delete(this.buffers.keys().next().value);
    this.buffers.set(key, buffer);
    return buffer;
  }
  async play(keys) {
    this.stop();
    const token = this.token;
    try {
      const Context = window.AudioContext || window.webkitAudioContext;
      if (!Context) throw Error('Deze browser heeft geen audio-ondersteuning');
      if (!this.context) this.context = new Context();
      // Called directly from the tap, before fetch/decode awaits.
      await this.context.resume();
      if (token !== this.token) return false;
      if (this.context.state !== 'running') throw Error('Tik opnieuw om geluid aan te zetten');
      this.report('');
      for (const key of keys) {
        if (token !== this.token) return false;
        const controller = new AbortController();
        this.abort = controller;
        const timeout = setTimeout(() => controller.abort(), 15000);
        let buffer;
        try { buffer = await this.load(key, controller.signal); }
        finally { clearTimeout(timeout); if (this.abort === controller) this.abort = null; }
        if (token !== this.token) return false;
        const ended = await new Promise(resolve => {
          const source = this.context.createBufferSource();
          source.buffer = buffer;
          source.connect(this.context.destination);
          this.source = source;
          this.finish = resolve;
          source.onended = () => {
            source.disconnect();
            if (this.source === source) { this.source = null; this.finish = null; }
            resolve(token === this.token);
          };
          source.start();
        });
        if (!ended || token !== this.token) return false;
      }
      return true;
    } catch (error) {
      if (token === this.token) this.report('Geluid kon niet worden afgespeeld. Controleer je verbinding of download de stemmen opnieuw. Tik daarna opnieuw.');
      return false;
    }
  }
}
