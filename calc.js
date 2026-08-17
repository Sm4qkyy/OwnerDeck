/* ==========================================================================
   Ownerdeck — "how many bookings pay for it?"

   The pricing page answers "what does it cost". This answers the question the
   owner is actually asking, which is what it has to earn back. €249 is a
   number to flinch at; 1.4 bookings is a number to weigh.

   Progressive enhancement: the markup ships with a working default already in
   it, so with scripting off the section still reads as a complete sentence —
   "1.4 bookings a month covers it" — rather than an empty control.
   ========================================================================== */
(function () {
  'use strict';

  var range = document.getElementById('calc-value');
  var plan = document.getElementById('calc-plan');
  var out = document.getElementById('calc-value-out');
  var n = document.getElementById('calc-n');
  if (!range || !plan || !out || !n) return;

  function euro(v) {
    return '€' + Number(v).toLocaleString('en-GB');
  }

  function update() {
    var booking = Number(range.value) || 1;
    var monthly = Number(plan.value) || 0;
    var needed = monthly / booking;

    out.textContent = euro(booking);

    /* One decimal below ten, none above. "1.4 bookings" is precise enough to
       be persuasive; "12.4 bookings" is just noise, and at that point the
       honest answer is that the plan is wrong for them. */
    // Tested at the boundary: 299/30 is 9.967, which toFixed(1) renders as
    // "10.0" — a decimal point on a whole number. Compare against 9.95 so it
    // crosses over cleanly.
    n.textContent = needed < 9.95 ? needed.toFixed(1) : String(Math.ceil(needed));

    // Fill the track to the left of the thumb, which <input type=range> will
    // not do on its own in any browser that matters.
    var pct = (booking - range.min) / (range.max - range.min) * 100;
    range.style.setProperty('--fill', pct.toFixed(1) + '%');
  }

  range.addEventListener('input', update);
  plan.addEventListener('change', update);
  update();
})();
