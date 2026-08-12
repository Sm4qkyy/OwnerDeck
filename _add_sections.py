# Inserts two sections into index.html and registers their strings for translation.
# Re-runnable: exits cleanly if the sections are already present.
import io, json, hashlib, re

def k(t): return 'k' + hashlib.md5(t.encode('utf-8')).hexdigest()[:8]

# ---- copy ----------------------------------------------------------------
# Every figure below is derived from Ownerdeck's own published prices and the
# quote shown in the conversation on this same page. Nothing is borrowed from
# an industry report, because a borrowed statistic is the first thing a
# sceptical owner checks and the fastest way to lose him.
WHO_EYE  = "Who it's for"
WHO_H2   = "If it has availability, a price and a booking."
WHO_P    = "Car rental is where it runs today, so that is the one that can be shown working. The shape of the problem is identical everywhere below."
WHO = [
  ("Car and buggy rental", "Fleet, rates, delivery, insurance, deposits."),
  ("Boat charters and tours", "Half day or full, group size, meeting point, weather held back for you."),
  ("Airport transfers", "Pickup time, flight number, vehicle size, one clear price."),
  ("Villa and apartment changeovers", "Dates, guest numbers, key handover, cleaning windows."),
  ("Salons and barbers", "Which service, which stylist, how long, what it costs."),
  ("Clinics and treatment rooms", "Appointment slots, practitioner, preparation, what to bring."),
]

MATH_EYE = "The maths"
MATH_H2  = "One booking a month and it has paid for itself."
MATH_P   = "Not a projection. These are the prices printed on this page and the quote from the conversation above."
MATH = [
  ("€150", "What one booking is worth",
   "Three days at €45, plus €15 hotel delivery. That is the exact total the assistant quoted in the conversation above."),
  ("€150", "What Ownerdeck costs",
   "Per month, no VAT, no setup fee while the early rate lasts, no contract."),
  ("€1,950", "One lost booking a week, one summer",
   "Thirteen weeks of June to August. More than a full year of Ownerdeck, gone to messages nobody answered."),
]
MATH_END = "The question is not whether €150 a month is cheap. It is whether you lose more than one booking a month to a message you were asleep for."

# ---- markup --------------------------------------------------------------
def eyebrow(txt):
    return (f'<div style="font-family:var(--font-mono);font-size:12px;letter-spacing:.08em;'
            f'text-transform:uppercase;color:var(--ink-mute);margin-bottom:20px">'
            f'<span style="color:var(--accent-strong)">//</span> '
            f'<span data-i18n="{k(txt)}">{txt}</span></div>')

def h2(txt):
    return (f'<h2 style="font-size:clamp(30px,4.2vw,50px);line-height:1.06;max-width:20em" '
            f'data-i18n="{k(txt)}">{txt}</h2>')

who_cards = ''.join(
  f'''
        <div style="background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px 24px 28px">
          <div style="font-family:var(--font-display);font-size:18px;font-weight:600;letter-spacing:-.02em;color:var(--ink)" data-i18n="{k(t)}">{t}</div>
          <p style="margin-top:8px;font-size:14.5px;line-height:1.55;color:var(--ink-mute)" data-i18n="{k(d)}">{d}</p>
        </div>''' for t, d in WHO)

WHO_SECTION = f'''
<section style="background:var(--paper);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:clamp(64px,8vw,104px) 24px">
  <div data-reveal="1" style="max-width:1140px;margin:0 auto">
    {eyebrow(WHO_EYE)}
    {h2(WHO_H2)}
    <p style="margin-top:18px;font-size:clamp(17px,1.5vw,20px);line-height:1.6;color:var(--ink-soft);max-width:44em" data-i18n="{k(WHO_P)}">{WHO_P}</p>
    <div class="od-swipe" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:clamp(20px,2.5vw,28px);margin-top:clamp(40px,5vw,56px)">{who_cards}
    </div>
  </div>
</section>
'''

math_cards = ''.join(
  f'''
        <div style="background:var(--card);border:1px solid var(--line);border-radius:18px;padding:28px 26px 30px">
          <div style="font-family:var(--font-display);font-size:clamp(36px,4vw,46px);font-weight:600;letter-spacing:-.045em;line-height:1;color:{'var(--accent-strong)' if i==2 else 'var(--ink)'}">{v}</div>
          <div style="margin-top:12px;font-family:var(--font-mono);font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-mute)" data-i18n="{k(lab)}">{lab}</div>
          <p style="margin-top:10px;font-size:14.5px;line-height:1.55;color:var(--ink-soft)" data-i18n="{k(sub)}">{sub}</p>
        </div>''' for i, (v, lab, sub) in enumerate(MATH))

MATH_SECTION = f'''
<section style="background:var(--card);padding:clamp(64px,8vw,104px) 24px">
  <div data-reveal="1" style="max-width:1140px;margin:0 auto">
    {eyebrow(MATH_EYE)}
    {h2(MATH_H2)}
    <p style="margin-top:18px;font-size:clamp(17px,1.5vw,20px);line-height:1.6;color:var(--ink-soft);max-width:44em" data-i18n="{k(MATH_P)}">{MATH_P}</p>
    <div class="od-swipe" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:clamp(20px,2.5vw,28px);margin-top:clamp(40px,5vw,56px)">{math_cards}
    </div>
    <p style="margin-top:clamp(30px,3vw,38px);font-size:clamp(17px,1.6vw,21px);line-height:1.55;color:var(--ink);max-width:36em;font-weight:500" data-i18n="{k(MATH_END)}">{MATH_END}</p>
  </div>
</section>
'''

# ---- insert --------------------------------------------------------------
p = 'index.html'
s = io.open(p, encoding='utf-8').read()

if k(MATH_H2) in s:
    print('  sections already present, nothing to do')
else:
    # "who it's for" goes after the capabilities section (#handles)
    i = s.find('<section', s.find('id="handles"') + 1)
    s = s[:i] + WHO_SECTION.strip() + '\n\n' + s[i:]
    # the maths goes immediately before pricing, so it frames the number
    j = s.find('<section id="pricing"')
    s = s[:j] + MATH_SECTION.strip() + '\n\n' + s[j:]
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  both sections inserted')

# ---- strings needing translation -----------------------------------------
strings = [WHO_EYE, WHO_H2, WHO_P, MATH_EYE, MATH_H2, MATH_P, MATH_END]
for t, d in WHO: strings += [t, d]
for _, lab, sub in MATH: strings += [lab, sub]
io.open('_new_strings.json', 'w', encoding='utf-8').write(
    json.dumps({k(t): t for t in strings}, ensure_ascii=False, indent=1))
print(f'  {len(strings)} strings need translating -> _new_strings.json')
