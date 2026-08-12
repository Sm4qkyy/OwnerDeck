# Widens the site's stated scope from car rental to any booking business.
#
# The distinction that matters: copy which describes SCOPE gets broadened,
# copy which shows PROOF stays exactly as it is. The two WhatsApp
# conversations, "Voyage Rent A Car", and "running on a car rental company's
# WhatsApp" are the only concrete evidence on the page. Genericising those
# would leave claims with nothing behind them — and they are already framed
# as an example rather than as the limit of who this serves.
import io, json, hashlib, re

def k(t): return 'k' + hashlib.md5(t.encode('utf-8')).hexdigest()[:8]

# old English -> new English. Keys are recomputed from the new text.
REWRITES = [
 # the five questions: kept vivid, but no longer only answerable by a car hire
 ("Do you have an automatic. How much for three days. Can you deliver to my hotel. Is insurance included. Do I need a deposit. In August that arrives a hundred times a day.",
  "Are you free on Saturday. How much for three. Can you come to us. Is everything included. Do I pay a deposit now. In a busy month that arrives a hundred times a day."),

 ("A tourist messages four rental companies at once. The first reply wins the booking. You were asleep — and that is the only reason you lost it.",
  "A customer messages four businesses at once. The first reply wins the booking. You were asleep — and that is the only reason you lost it."),

 ("Your fleet, your rates, your locations, delivery fees, insurance, deposits, the policies you repeat every day. One conversation, and it's mine to build.",
  "What you offer, your rates, your locations, your extras, your deposits, the policies you repeat every day. One conversation, and it's mine to build."),

 ("It reads your own booking system. It never guesses a rate, and never promises a car you don't have free.",
  "It reads your own booking system. It never guesses a rate, and never promises something you don't have free."),

 ("Photos of the actual car",
  "Photos of the actual thing"),

 ("When someone settles on one vehicle, it sends the photos — the way you would if you were holding the phone.",
  "When someone settles on one option, it sends the photos — the way you would if you were holding the phone."),

 ("It doesn't take payment. It doesn't handle complaints or accidents. It doesn't manage your contracts or your fleet. And it doesn't replace anyone on your team — the person answering WhatsApp at 11pm is you, and this gives you that hour back.",
  "It doesn't take payment. It doesn't handle complaints or disputes. It doesn't manage your contracts or your diary. And it doesn't replace anyone on your team — the person answering WhatsApp at 11pm is you, and this gives you that hour back."),

 # the maths: keep the concrete example, stop implying it is the only case
 ("Three days at €45, plus €15 hotel delivery. That is the exact total the assistant quoted in the conversation above.",
  "Whatever an average booking is worth to you. In the conversation above it was €150 — three days of hire plus delivery."),

 ("One lost booking a week, one summer",
  "One lost booking a week, one season"),

 ("Thirteen weeks of June to August. More than a full year of Ownerdeck, gone to messages nobody answered.",
  "Across a thirteen-week season at that value. More than a full year of Ownerdeck, gone to messages nobody answered."),

 # footer strapline
 ("A WhatsApp assistant for owner-run rental, tourism and appointment businesses. Any language, any timezone.",
  "A WhatsApp assistant for any owner-run business that takes bookings. Any language, any timezone."),
]

p = 'index.html'
s = io.open(p, encoding='utf-8').read()

changed, new_strings = 0, {}
for old, new in REWRITES:
    ko, kn = k(old), k(new)
    if f'data-i18n="{ko}"' not in s:
        print(f'  MISS  {old[:58]}')
        continue
    s = s.replace(f'data-i18n="{ko}"', f'data-i18n="{kn}"')
    s = s.replace(old, new)
    new_strings[kn] = new
    changed += 1

# title + meta + og: state the broad scope
s = s.replace('WhatsApp Booking Bot for Rental &amp; Tourism | Ownerdeck',
              'WhatsApp Booking Bot for Any Business | Ownerdeck')
s = s.replace('An AI assistant on your own WhatsApp number. Answers in about 2 seconds, in any language, with your real prices and availability — then takes the booking.',
              'An AI assistant on your own WhatsApp number. Answers in about 2 seconds, in any language, with your real prices and availability — then takes the booking.')

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print(f'\n  rewritten: {changed}/{len(REWRITES)}')
io.open('_broadened.json', 'w', encoding='utf-8').write(json.dumps(new_strings, ensure_ascii=False, indent=1))

# retire the old keys from every pack so nothing serves the narrow wording
old_keys = [k(o) for o, _ in REWRITES]
for c in ['el', 'ru', 'de', 'he', 'ar']:
    f = f'lang/{c}.json'
    d = json.load(io.open(f, encoding='utf-8'))
    removed = sum(1 for ok in old_keys if d.pop(ok, None) is not None)
    io.open(f, 'w', encoding='utf-8', newline='').write(json.dumps(d, ensure_ascii=False, indent=1))
    print(f'  {c}: retired {removed} narrow strings, {len(d)} keys left')
