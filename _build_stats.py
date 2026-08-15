# Builds stats.html from the shared site chassis.
import io, re

src = io.open('terms.html', encoding='utf-8').read()
head = src[:src.find('<main>')]
foot = src[src.find('</main>') + len('</main>'):]

head = re.sub(r'<title>[^<]*</title>', '<title>Stats — Ownerdeck</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Private.">', head, count=1)
head = re.sub(r'<link rel="canonical" href="[^"]*">\n?', '', head, count=1)
if 'noindex' not in head:
    head = head.replace('<meta name="viewport"',
                        '<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"', 1)

EXTRA_CSS = """<style>
  /* Tokens come from brand.css; nothing here declares a colour of its own. */
  .lock{max-width:21rem;margin:var(--s7) 0 0}
  .lock input{width:100%;box-sizing:border-box;padding:var(--s3) var(--s4);font-size:1rem;
    font-family:var(--body);color:var(--ink);background:var(--bone);
    border:1px solid var(--rule);border-radius:var(--radius)}
  .lock input:focus-visible{outline:2px solid var(--clay);outline-offset:2px}
  .lock button{width:100%;margin-top:var(--s3);padding:var(--s3);font-size:1rem;font-weight:600;
    font-family:var(--body);color:var(--bone);background:var(--clay-deep);
    border:none;border-radius:var(--radius);cursor:pointer}
  .lock .msg{margin-top:var(--s3);font-size:.9375rem;color:var(--clay-deep);min-height:1.25rem}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));gap:var(--s4);margin-top:var(--s4)}
  .kpi{background:var(--bone-2);border:1px solid var(--rule);border-radius:var(--radius);padding:var(--s5)}
  .kpi b{display:block;font-family:var(--display);font-size:1.875rem;letter-spacing:-.03em;color:var(--ink)}
  .kpi span{font-size:.8125rem;color:var(--ink-soft);letter-spacing:.06em;text-transform:uppercase}
  .spark{display:flex;align-items:flex-end;gap:3px;height:5.5rem;margin-top:var(--s3)}
  .spark i{flex:1;background:var(--clay);border-radius:2px 2px 0 0;min-height:2px}
  .out{margin-top:var(--s7);font-size:.9375rem;color:var(--ink-soft);cursor:pointer;
    background:none;border:none;padding:0;font-family:var(--body);text-decoration:underline}
</style>
"""
head = head.replace('</head>', EXTRA_CSS + '</head>')

BODY = """<main>
  <div id="main" class="wrap section longform">
  <a class="back-link" href="/">Back to ownerdeck.com</a>
  <p class="eyebrow">Private</p>
  <h1>Stats</h1>

  <!-- Nothing below is filled in until the server accepts a password. The page
       ships with no numbers in it on purpose: if the data were here, the
       password would be decoration, because anyone can read page source. -->
  <div id="lock" class="lock">
    <form id="lockform" autocomplete="off">
      <input id="user" type="text" placeholder="Username" aria-label="Username"
             autocomplete="username" style="margin-bottom:10px">
      <input id="pw" type="password" placeholder="Password" aria-label="Password"
             autocomplete="current-password">
      <button type="submit">Sign in</button>
      <div class="msg" id="msg" role="status" aria-live="polite"></div>
    </form>
  </div>

  <div id="dash" hidden>
    <div class="kpis">
      <div class="kpi"><b id="k-today">&mdash;</b><span>Today</span></div>
      <div class="kpi"><b id="k-7">&mdash;</b><span>Last 7 days</span></div>
      <div class="kpi"><b id="k-30">&mdash;</b><span>Last 30 days</span></div>
      <div class="kpi"><b id="k-total">&mdash;</b><span>All time</span></div>
    </div>

    <h2>Last 30 days</h2>
    <div class="spark" id="spark"></div>

    <h2>Pages</h2>
    <table><thead><tr><th>Page</th><th>Views</th></tr></thead><tbody id="t-paths"></tbody></table>

    <h2>Where they came from</h2>
    <table><thead><tr><th>Source</th><th>Views</th></tr></thead><tbody id="t-refs"></tbody></table>

    <h2>Countries</h2>
    <table><thead><tr><th>Country</th><th>Views</th></tr></thead><tbody id="t-countries"></tbody></table>

    <div class="note" style="margin-top:30px">
      Counted by the site itself. Vercel &rarr; Analytics holds the same traffic
      plus the event breakdown: video played, chat opened, contact clicked.
    </div>
    <button class="out" id="out">Log out</button>
  </div>
  </div>
</main>"""

SCRIPT = """
<script>
(function () {
  "use strict";
  var KEY = 'od_stats_token';
  var lock = document.getElementById('lock');
  var dash = document.getElementById('dash');
  var msg  = document.getElementById('msg');

  function tok() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function setTok(t) { try { t ? localStorage.setItem(KEY, t) : localStorage.removeItem(KEY); } catch (e) {} }
  function n(x) { return (x || 0).toLocaleString(); }

  function rows(id, obj, fmt) {
    var el = document.getElementById(id);
    el.innerHTML = '';
    var ks = Object.keys(obj || {}).sort(function (a, b) { return obj[b] - obj[a]; }).slice(0, 12);
    if (!ks.length) {
      var tr = document.createElement('tr');
      var td = document.createElement('td');
      td.colSpan = 2; td.style.color = 'var(--ink-faint)'; td.textContent = 'Nothing yet';
      tr.appendChild(td); el.appendChild(tr); return;
    }
    ks.forEach(function (k) {
      var tr = document.createElement('tr');
      var a = document.createElement('td'); a.textContent = fmt ? fmt(k) : k;
      var b = document.createElement('td'); b.textContent = n(obj[k]);
      tr.appendChild(a); tr.appendChild(b); el.appendChild(tr);
    });
  }

  function paint(d) {
    document.getElementById('k-today').textContent = n(d.today);
    document.getElementById('k-7').textContent     = n(d.last7);
    document.getElementById('k-30').textContent    = n(d.last30);
    document.getElementById('k-total').textContent = n(d.total);

    var max = Math.max.apply(null, d.daily.map(function (x) { return x.views; }).concat([1]));
    var s = document.getElementById('spark');
    s.innerHTML = '';
    d.daily.forEach(function (x) {
      var i = document.createElement('i');
      i.style.height = Math.max(2, Math.round((x.views / max) * 88)) + 'px';
      i.title = x.date + ': ' + x.views;
      s.appendChild(i);
    });

    rows('t-paths', d.paths, function (p) {
      if (p === '/') return 'Home';
      return p.replace(/^\\//, '').replace(/\\.html$/, '');
    });
    rows('t-refs', d.refs);
    rows('t-countries', d.countries);

    lock.hidden = true;
    dash.hidden = false;
  }

  function load() {
    var t = tok();
    if (!t) return;
    fetch('/api/stats', { headers: { Authorization: 'Bearer ' + t } })
      .then(function (r) {
        if (r.status === 401) { setTok(''); throw new Error('expired'); }
        return r.json();
      })
      .then(function (d) {
        if (d.ready === false) { msg.textContent = 'Storage is not configured yet.'; return; }
        paint(d);
      })
      .catch(function () { /* stay locked */ });
  }

  document.getElementById('lockform').addEventListener('submit', function (e) {
    e.preventDefault();
    msg.textContent = '';
    var user = document.getElementById('user').value;
    var pw   = document.getElementById('pw').value;
    fetch('/api/stats', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ user: user, password: pw })
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, s: r.status, j: j }; }); })
      .then(function (o) {
        document.getElementById('pw').value = '';
        if (o.ok && o.j.token) { setTok(o.j.token); load(); return; }
        if (o.s === 429) { msg.textContent = o.j.message || 'Too many attempts. Locked for an hour.'; return; }
        if (o.s === 503) { msg.textContent = 'Not set up yet - STATS_USER or STATS_PASSWORD missing in Vercel.'; return; }
        msg.textContent = 'Wrong username or password.';
      })
      .catch(function () { msg.textContent = 'Could not reach the server.'; });
  });

  document.getElementById('out').addEventListener('click', function () {
    setTok(''); dash.hidden = true; lock.hidden = false;
  });

  load();
})();
</script>
"""

io.open('stats.html', 'w', encoding='utf-8', newline='').write(head + BODY + SCRIPT + foot)
print('  stats.html written')
