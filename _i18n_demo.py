# Key map for the /demo walkthrough strings.
# Same scheme as the rest of the site: 'k' + md5(english)[:8], so editing the
# English changes the key, the lookup misses, and the element falls back to the
# English already in the DOM. Run this after changing any string below and
# update demo.html / demo.js / lang/*.json with what it prints.
import hashlib, io, json

EN = [
  # header + stepper
  "Back to site",
  "Watch", "Try it", "Ask it anything", "Get in touch",
  "See Ownerdeck work — watch it, try it, then get in touch",
  # step 1
  "Step 1 · See it live",
  "Watch it handle a real enquiry.",
  "A short recording of Ownerdeck answering, quoting a real price and closing a booking — start to finish, with nobody typing.",
  "Next — try it yourself",
  # step 2
  "Step 2 · Try it yourself",
  "Have a conversation with it.",
  "A preset demo standing in for a tour company. Tap a reply and watch how it answers — including in another language.",
  "Back",
  "Next — ask it anything",
  # step 3
  "Step 3 · Ask it anything",
  "Now ask it yourself.",
  "This one is live — type a real question about pricing, setup, languages, or whether it suits your business. Same assistant, answering here on the page.",
  "Next — get in touch",
  # step 4
  "Step 4 · Get in touch",
  "Want this on your own number?",
  "Message on whichever you actually use. You'll get a straight answer about whether it fits your business — and what it would take to set up.",
  # demo.js chrome
  "Demo video coming soon",
  "In the meantime, try the live demo below — it works right now.",
  "Ownerdeck · answering now",
  "Start over",
  "That whole conversation — no human involved.",
  "This is a preset demo. The real thing uses your services, prices and availability.",
  "Like what you saw? Message me directly.",
  "Pick whichever you actually use — I reply personally.",
  "Hi! I saw the Ownerdeck demo and I'd like to know more.",
  # demo.js conversation
  "Hey! \U0001F44B I'm Ownerdeck, answering for a demo business — Blue Bay Tours. Ask me what a real customer would ask.",
  "Any space on the sunset cruise Friday?",
  "How much for 2 people?",
  "Friday's 18:00 sunset cruise has 6 seats left — €35 per person.",
  "Want me to hold a couple for you?",
  "Yes, 2 people please",
  "What's included?",
  "€35 per person — so €70 for two.",
  "That covers hotel pickup, a welcome drink and the full 2-hour cruise.",
  "Great, Friday works",
  "Pickup from your hotel, a welcome drink, two hours on the water and a swim stop.",
  "Shall I put two seats down for Friday?",
  "Yes please, book it",
  "Done ✓ Booking #TC-2291 — Friday 18:00, 2 seats, hotel pickup included.",
  "Confirmation sent, and I've pinged the owner.",
  "Language auto-detected — no setup needed",
  "Try asking in Russian",
  "Try asking in German",
  "Switch back",
]

def key(s):
    return 'k' + hashlib.md5(s.encode('utf-8')).hexdigest()[:8]

if __name__ == '__main__':
    have = json.load(io.open('lang/el.json', encoding='utf-8'))
    seen = {}
    for s in EN:
        k = key(s)
        if k in seen:
            print('!! COLLISION', k, repr(s), 'vs', repr(seen[k]))
        seen[k] = s
        print('%s  %-6s %s' % (k, 'EXISTS' if k in have else 'new', s))
    print('\n%d strings, %d unique keys' % (len(EN), len(seen)))
