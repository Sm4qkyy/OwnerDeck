/* Drives the session-pass signing out of api/chat.js. This is the thing that
   decides whether a request counts as human-verified, so a hole in it is a
   free pass for anyone who notices. Lifted from the shipped file rather than
   copied, so the test cannot drift from what deploys. */
const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'api', 'chat.js'), 'utf8');

const a = src.indexOf('const crypto = require');
const b = src.indexOf('/* ---------- helpers ---------- */');
if (a < 0 || b < 0) { console.error('  FAIL: cannot locate the pass helpers'); process.exit(1); }

process.env.CHAT_PASS_SECRET = 'test-signing-key';
const M = new Function('require', 'process',
  src.slice(a, b) + '\n return { issuePass, passValid, PASS_TTL_MS };')(require, process);

let ok = true;
function check(name, cond, extra) {
  if (!cond) { ok = false; console.log(`  FAIL  ${name}${extra ? '  ' + extra : ''}`); }
  else console.log(`  PASS  ${name}`);
}

const IP = '203.0.113.7';
const good = M.issuePass(IP);

check('a freshly issued pass is accepted', M.passValid(good, IP) === true, good);
check('it is refused from another address', M.passValid(good, '198.51.100.2') === false);
check('garbage is refused', M.passValid('nonsense', IP) === false);
check('an empty pass is refused', M.passValid('', IP) === false);
check('a truncated pass is refused', M.passValid(good.split('.').slice(0, 2).join('.'), IP) === false);

// Extending your own expiry must break the signature rather than work.
const [exp, tag, sig] = good.split('.');
const forged = `${Number(exp) + 86400000}.${tag}.${sig}`;
check('a hand-edited expiry is refused', M.passValid(forged, IP) === false, forged.slice(0, 30));

// A flipped signature byte must not slip through a sloppy comparison.
const flipped = `${exp}.${tag}.${sig.slice(0, -1)}${sig.slice(-1) === 'A' ? 'B' : 'A'}`;
check('a tampered signature is refused', M.passValid(flipped, IP) === false);

// Expiry is honoured.
const stale = (() => {
  const body = `${Date.now() - 1000}.${require('crypto').createHash('sha256').update(IP).digest('hex').slice(0, 16)}`;
  const s = require('crypto').createHmac('sha256', 'test-signing-key').update(body).digest('base64url');
  return `${body}.${s}`;
})();
check('an expired pass is refused', M.passValid(stale, IP) === false);

// A pass signed with a different key must not verify under ours.
const foreign = (() => {
  const body = `${Date.now() + 60000}.${require('crypto').createHash('sha256').update(IP).digest('hex').slice(0, 16)}`;
  const s = require('crypto').createHmac('sha256', 'someone-elses-key').update(body).digest('base64url');
  return `${body}.${s}`;
})();
check('a pass signed with another key is refused', M.passValid(foreign, IP) === false);

check('the window is 30 minutes', M.PASS_TTL_MS === 30 * 60 * 1000, String(M.PASS_TTL_MS));
check('the address is not stored in the clear', !good.includes(IP), good);

console.log(ok ? '\n  all pass tests passed' : '\n  FAILURES');
process.exit(ok ? 0 : 1);
