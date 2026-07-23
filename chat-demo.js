/* ================================================================
   Hero chat mockup — cycles through different business types to show
   OwnerDeck works for any business (not just tourism).
   Messages are illustrative samples and stay in English across locales.
   Respects prefers-reduced-motion (stays on the first example).
================================================================ */
(function () {
  "use strict";

  var shell = document.querySelector(".chat-shell");
  if (!shell) return;
  var nameEl = shell.querySelector(".chat-name");
  var avatarEl = shell.querySelector(".chat-avatar");
  var messagesEl = shell.querySelector(".chat-messages");
  if (!nameEl || !avatarEl || !messagesEl) return;

  var businesses = [
    { name: "Sunset Watersports", avatar: "⛵", msgs: [
      { t: "in",  time: "09:47", text: "Hi! Do you have a jet ski tomorrow at 10am for 2 people?" },
      { t: "out", time: "09:47", text: "Hi! Yes, we have slots at 10:00 and 11:30 🎉 Which works better for you?" },
      { t: "in",  time: "09:48", text: "10:00 please! How much for 30 min?" },
      { t: "out", time: "09:48", text: "€80 for 2 people, 30 min 🏄 Can I get your name to hold the slot?" }
    ]},
    { name: "Bella Hair Studio", avatar: "💇", msgs: [
      { t: "in",  time: "14:12", text: "Hi! Any slot for a haircut tomorrow around 3pm?" },
      { t: "out", time: "14:12", text: "Hi! Yes — 3:00 or 4:30 are free 💇 Which suits you?" },
      { t: "in",  time: "14:13", text: "3:00 please. How much for a cut and blow-dry?" },
      { t: "out", time: "14:13", text: "€35 for cut & blow-dry 💫 Can I take your name to hold it?" }
    ]},
    { name: "Marina Dental Clinic", avatar: "🦷", msgs: [
      { t: "in",  time: "09:05", text: "Hi, can I book a cleaning this week?" },
      { t: "out", time: "09:05", text: "Hi! We have Thu 11:00 or Fri 16:00 🦷 Which works?" },
      { t: "in",  time: "09:06", text: "Thursday 11:00. How long does it take?" },
      { t: "out", time: "09:06", text: "About 45 minutes 😊 Can I get your name and number to confirm?" }
    ]},
    { name: "Nikos Taverna", avatar: "🍽️", msgs: [
      { t: "in",  time: "18:30", text: "Hi! Table for 4 tonight at 8?" },
      { t: "out", time: "18:30", text: "Hi! Yes, 8:00 works 🍽️ Inside or on the terrace?" },
      { t: "in",  time: "18:31", text: "Terrace please. Any vegetarian options?" },
      { t: "out", time: "18:31", text: "Plenty 🌿 Booked a terrace table for 4 at 8:00. See you tonight!" }
    ]},
    { name: "Coastal Car Rental", avatar: "🚗", msgs: [
      { t: "in",  time: "11:20", text: "Hi, any automatic car free this weekend?" },
      { t: "out", time: "11:20", text: "Hi! Yes, options from €35/day 🚗 Which dates exactly?" },
      { t: "in",  time: "11:21", text: "Sat to Mon. How much in total?" },
      { t: "out", time: "11:21", text: "€105 for 3 days, insurance included ✅ Shall I hold it for you?" }
    ]}
  ];

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(b) {
    avatarEl.textContent = b.avatar;
    nameEl.textContent = b.name;
    var html = "";
    for (var k = 0; k < b.msgs.length; k++) {
      var m = b.msgs[k];
      var cls = m.t === "in" ? "msg-in" : "msg-out";
      var tick = m.t === "out" ? " ✓✓" : "";
      html += '<div class="msg ' + cls + '"><div class="msg-bubble">' + esc(m.text) +
              '</div><div class="msg-time">' + esc(m.time) + tick + "</div></div>";
    }
    messagesEl.innerHTML = html;
  }

  var idx = 0;
  render(businesses[0]);

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || businesses.length < 2) return;

  setInterval(function () {
    shell.classList.add("is-swapping");
    setTimeout(function () {
      idx = (idx + 1) % businesses.length;
      render(businesses[idx]);
      shell.classList.remove("is-swapping");
    }, 400);
  }, 4200);
})();
