/* Drives the real readStream() out of chat-widget.js against a fake
   Response, so the SSE parsing is tested without a browser. The function is
   sliced out of the shipped file rather than copied, so the test cannot
   silently drift from what actually deploys. */
const fs = require('fs');
const SRC = require('path').join(__dirname, 'chat-widget.js');
const src = fs.readFileSync(SRC, 'utf8');

const start = src.indexOf('  function readStream(');
const end   = src.indexOf('  /* ---------- send ---------- */');
if (start < 0 || end < 0) { console.error('  FAIL: could not locate readStream'); process.exit(1); }

// Stubs matching what the widget provides.
let removed = 0;
const T = (k, en) => en;
function makeLog() {
  return { scrollHeight: 100, scrollTop: 0, clientHeight: 100, _nodes: [] };
}
function bubble(log, who, text) {
  const n = { textContent: text, who };
  log._nodes.push(n);
  return n;
}
const dots = { remove() { removed++; } };

const readStream = new Function('T', 'bubble', 'TextDecoder',
  src.slice(start, end) + '\n return readStream;')(T, bubble, TextDecoder);

// A fake body that hands over bytes in awkward chunks: a frame split across
// two reads, two frames in one read, and a stray keep-alive line. If the
// parser only works on tidy input it is not a parser.
function bodyOf(chunks) {
  let i = 0;
  const enc = new TextEncoder();
  return { getReader: () => ({
    read: () => Promise.resolve(i < chunks.length
      ? { value: enc.encode(chunks[i++]), done: false }
      : { value: undefined, done: true })
  })};
}

async function run(name, chunks, expectText, expectOk) {
  removed = 0;
  const log = makeLog();
  const out = await readStream({ body: bodyOf(chunks) }, dots, log);
  const got = log._nodes.map(n => n.textContent).join('');
  const pass = got === expectText && out.ok === expectOk && removed === 1;
  console.log(`  ${pass ? 'PASS' : 'FAIL'}  ${name}`);
  if (!pass) console.log(`        got ${JSON.stringify(got)} ok=${out.ok} removed=${removed}\n        want ${JSON.stringify(expectText)} ok=${expectOk} removed=1`);
  return pass;
}

(async () => {
  let ok = true;
  ok &= await run('tokens split across reads',
    ['data: {"t":"Hel', 'lo"}\n\n', 'data: {"t":" there"}\n\n', 'data: {"done":true}\n\n'],
    'Hello there', true);

  ok &= await run('two frames in one read',
    ['data: {"t":"a"}\n\ndata: {"t":"b"}\n\n', 'data: {"done":true}\n\n'],
    'ab', true);

  ok &= await run('ignores keep-alives and junk',
    [': keep-alive\n\n', 'event: ping\ndata: {"t":"x"}\n\n', 'data: notjson\n\n', 'data: {"done":true}\n\n'],
    'x', true);

  ok &= await run('empty stream falls back',
    ['data: {"done":true}\n\n'],
    'Something went wrong. Email mark@ownerdeck.com and he will answer directly.', false);

  ok &= await run('unicode survives chunk boundary',
    ['data: {"t":"\u20ac6', '00"}\n\n', 'data: {"done":true}\n\n'],
    '\u20ac600', true);

  console.log(ok ? '\n  all stream tests passed' : '\n  FAILURES');
  process.exit(ok ? 0 : 1);
})();
