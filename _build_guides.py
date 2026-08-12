# Generates the long-tail landing pages from the shared site chassis.
# Re-runnable: rewrites each page from the content below, so edits happen
# here rather than in five near-identical HTML files that drift apart.
import io, json, re

# Chassis is read from a live page each run, so these guides inherit header,
# theme handling, footer and script tags automatically instead of drifting.
_src = io.open('terms.html', encoding='utf-8').read()
HEAD = _src[:_src.find('<main>')]
FOOT = _src[_src.find('</main>') + len('</main>'):]
BASE = 'https://www.ownerdeck.com/'

PAGES = [
{
 'slug':'whatsapp-bot-car-rental.html',
 'title':'WhatsApp Bot for Car Rental Companies | Ownerdeck',
 'desc':'An AI assistant that answers rental enquiries on your own WhatsApp number in about two seconds — quoting your real rates and live availability, then capturing the booking.',
 'h1':'A WhatsApp bot for car rental companies',
 'lede':'Most rental enquiries arrive as a WhatsApp message, and most of them ask the same five things. Here is what it looks like when those get answered without you.',
 'body':"""
<h2>The five questions</h2>
<p>Do you have an automatic. How much for three days. Can you deliver to my hotel. Is insurance included. Do I need a deposit. In August that arrives a hundred times a day, and every single one of them is a booking waiting to happen or a booking about to be lost.</p>
<p>The problem is not that the questions are hard. It is that they are relentless, they arrive at 11pm, and the person who has to answer them is you — after a changeover day and an airport pickup at six.</p>

<h2>Why the timing matters more than the answer</h2>
<p>A tourist looking for a car does not message one company. They message four, at the same time, and take whichever answer arrives first with a clear price. This is not disloyalty; they are standing in an airport with luggage and want the problem solved.</p>
<p>Which means the booking is usually decided before you have read the message. Not on price, not on your fleet, not on your reviews — on who replied. That is the part an assistant fixes, and it is the only part that has to happen instantly.</p>

<h2>What it actually does</h2>
<ul>
  <li>Answers on your existing WhatsApp Business number, in about two seconds, at any hour.</li>
  <li>Detects the customer's language and replies in it — English, Russian, German, Polish, Arabic and more — including if they switch mid-conversation.</li>
  <li>Reads live availability and rates from the system you already use, so it never quotes a car that is out or a July price in August.</li>
  <li>Works out the whole quote: days times rate, hotel or airport delivery, extras like CDW. One clear total, not a maybe.</li>
  <li>Sends photos of the actual vehicle once someone settles on one.</li>
  <li>Captures the booking with dates, times, pickup and drop-off, name and contact, confirmed back with a reference number.</li>
  <li>Messages you the moment a booking lands, and writes every conversation to a log you can read.</li>
</ul>

<h2>What it will not do</h2>
<p>It does not take payment. It does not handle complaints or accidents. It does not manage your contracts or your fleet. And when a question falls outside what you have told it, it says so and passes the conversation to you rather than guessing — which is the behaviour that makes the rest of it trustworthy.</p>

<h2>The honest part about accuracy</h2>
<p>An assistant that invents a rate is worse than no assistant. This one quotes only from your own prices and your own availability; it does not answer from memory. If your rates live in a spreadsheet, that works too. You will see every handoff in the log, so you can check what it chose not to answer.</p>

<h2>Setup</h2>
<p>Live in 48 hours. You tell me your fleet, rates, locations and policies once — that is your part. I build it, test it, and switch it on. It runs on the number already printed on your cards and listings, so nothing changes for your customers and there is no app for anyone to install.</p>
<p>€150 per month, no VAT. No minimum term, no notice period. Cancel by email and it stops.</p>
""",
 'faq':[
  ('Do I need a new phone number for a WhatsApp bot?',
   'No. It runs on the WhatsApp Business number you already give out, so your customers message the same number as always and nothing on your cards or listings has to change.'),
  ('Can it quote real prices and availability?',
   'Yes. It reads live availability and rates from the system you already use, so it cannot sell a car that is out or quote a rate that has changed. If your availability lives in a spreadsheet, that works too.'),
  ('What happens if a customer asks something it does not know?',
   'It says so and passes the conversation to you rather than guessing. Every one of those handoffs appears in the log so you can see what it declined to answer.'),
 ]},

{
 'slug':'whatsapp-booking-bot-boat-charter-tours.html',
 'title':'WhatsApp Booking Bot for Boat Charters and Tours | Ownerdeck',
 'desc':'Answer charter and tour enquiries on WhatsApp in about two seconds, with your real availability and prices, and capture the booking — day or night, in any language.',
 'h1':'A WhatsApp booking bot for boat charters and tours',
 'lede':'Charters and tours have the same shape as any rental: availability, a price, and a booking. That is all an assistant needs to handle the enquiry for you.',
 'body':"""
<h2>Why this works the same way</h2>
<p>Ownerdeck runs today on a car rental company's WhatsApp. Charters and tours are not a different problem — they are the same problem with different nouns. Something is available on some dates, it costs an amount that depends on duration and extras, and a customer wants to book it before someone else does.</p>
<p>If your business has those three things, the assistant fits without being rebuilt.</p>

<h2>The enquiries it takes off you</h2>
<ul>
  <li>Is the boat free on Saturday, and for how many people.</li>
  <li>Half day or full day, and what is the difference in price.</li>
  <li>Is the skipper included. Is fuel included. What about lunch.</li>
  <li>Where do we meet you, and what time.</li>
  <li>What happens if the weather turns.</li>
</ul>
<p>Every one of them is a question you have answered a thousand times, and every one arrives while you are on the water and cannot reach your phone.</p>

<h2>The part that costs you money</h2>
<p>Peak season enquiries do not wait. A group deciding what to do tomorrow messages three operators and books with whoever confirms first. When you are out running today's charter, you are structurally unable to win tomorrow's — which is the exact hour you most need the booking.</p>
<p>An assistant answering in two seconds does not make you better than your competitors. It makes you reachable at the moment the decision gets made, which turns out to be most of it.</p>

<h2>Weather, deposits and the things a bot should not decide</h2>
<p>Some questions genuinely need you. A weather call, an unusual group size, a special request — the assistant is told what it does not know, and hands those to you instead of improvising an answer. That boundary is set when it is built, and you can move it whenever you like.</p>

<h2>What you get</h2>
<p>A message the moment a booking lands, with dates, times, meeting point, group size and contact details, confirmed back to the customer with a reference. Every conversation written to a log only you and I can open. And the ability to take over any chat yourself — you reply, it steps back.</p>
<p>€150 per month, no VAT, live in 48 hours, on the number you already use. Cancel any time.</p>
""",
 'faq':[
  ('Does this only work for car rental?',
   'No. Car rental is where it runs today, so that is what can be shown working. Anything with availability, a price and a booking works the same way — boat charters, buggy and quad hire, airport transfers, villa changeovers, salons and clinics.'),
  ('Can it handle group sizes and half-day versus full-day pricing?',
   'Yes. It quotes from the rules you give it, including duration tiers, per-person pricing and extras, and works out one clear total rather than an estimate.'),
  ('What about weather cancellations?',
   'That is a judgement call, so it is one of the things the assistant is told to hand to you rather than answer. It says it will check with the owner and passes the conversation over.'),
 ]},

{
 'slug':'stop-losing-bookings-slow-whatsapp-replies.html',
 'title':'Stop Losing Bookings to Slow Replies | Ownerdeck',
 'desc':'Customers message several businesses at once and book with whoever replies first. Here is why speed decides the booking, and what an owner-operator can actually do about it.',
 'h1':'How to stop losing bookings to slow replies',
 'lede':'The booking is usually decided before you have read the message. That is uncomfortable, but it is also the most fixable problem in the business.',
 'body':"""
<h2>What actually happens</h2>
<p>A customer needs something — a car, a boat, an appointment. They do not research. They open WhatsApp, find three or four businesses, and send the same message to all of them. Then they take the first clear answer.</p>
<p>You did not lose that booking on price. You did not lose it on quality. You lost it because you were driving, or asleep, or with another customer — and someone else was not.</p>

<h2>Why the usual fixes do not work</h2>
<p><strong>Answering faster yourself.</strong> You are already answering as fast as a human can. The problem is not your speed, it is that you sleep and the enquiries do not.</p>
<p><strong>An auto-reply.</strong> "Thanks, we'll get back to you shortly" does not win the booking. The customer still has three other conversations open, and one of them contains an actual price.</p>
<p><strong>Hiring someone.</strong> For most owner-operators the numbers do not work, and the enquiries cluster into evenings and August anyway — the two times a part-timer is least available.</p>
<p><strong>Taking bookings only through a website form.</strong> This moves the problem rather than solving it. People message on WhatsApp because it is where they already are.</p>

<h2>What actually closes the gap</h2>
<p>The reply has to contain a real answer, and it has to arrive in seconds. Both, or neither counts. An assistant that says "we have three automatics free on Saturday, the cheapest is €45 a day, three days is €135, where should I bring it?" has effectively taken the booking. One that says "hello, how can I help?" has not.</p>
<p>That means it needs your actual prices and your actual availability, not a script. Anything less is an auto-reply wearing a costume.</p>

<h2>What to measure</h2>
<p>Before changing anything, look at your own WhatsApp for the last week. Count the enquiries that arrived between 8pm and 8am. Count how many of those you replied to the next morning. Count how many of those became bookings.</p>
<p>Most owners find the overnight reply rate is where the money is going, and that it is worse in exactly the month they can least afford it.</p>

<h2>What this costs</h2>
<p>Ownerdeck answers on your own WhatsApp number in about two seconds, in the customer's language, with your real prices and live availability, then captures the booking and messages you. €150 per month, no VAT, live in 48 hours, cancel any time.</p>
<p>If it is not earning that back, one lost booking a month in most rental businesses, you say so and it stops.</p>
""",
 'faq':[
  ('How fast does the assistant reply?',
   'About two seconds, at any hour. The 2am enquiry gets the same answer as the 2pm one, so nobody waits for you to wake up.'),
  ('Is an auto-reply not enough?',
   'No. An auto-reply acknowledges the message but does not answer it, so the customer keeps talking to the businesses that quoted a price. The reply has to contain the actual answer to win the booking.'),
  ('Will customers know they are talking to an assistant?',
   'Yes. It states that it is an automated assistant and not a person, and anyone can ask for you at any time. That is both an EU AI Act requirement and simply better business.'),
 ]},

{
 'slug':'do-i-need-a-new-number-whatsapp-bot.html',
 'title':'Do You Need a New Number for a WhatsApp Bot? | Ownerdeck',
 'desc':'No. A WhatsApp assistant runs on the WhatsApp Business number you already give out, so nothing changes for your customers, your cards or your listings.',
 'h1':'Do you need a new number for a WhatsApp bot?',
 'lede':'No. And if a provider tells you otherwise, that is worth asking about — because a new number quietly costs you everything the old one had.',
 'body':"""
<h2>The short answer</h2>
<p>A WhatsApp assistant runs on the WhatsApp Business number you already use. Your customers message the same number they always have. Nothing on your business cards, your listings, your van, your Google profile or your Instagram bio needs to change.</p>

<h2>Why this matters more than it sounds</h2>
<p>Your number is not just a contact detail. It carries your chat history with returning customers, the reviews and listings that point at it, the years of people who saved it, and the recognition when it appears on their phone.</p>
<p>Move to a new number and you leave all of that behind. Every returning customer messages the old one and gets silence. Every printed card is wrong. Every listing needs updating, and the ones you forget quietly send people nowhere.</p>
<p>That is a real cost, and it is usually paid to make setup easier for the provider rather than better for you.</p>

<h2>What about WhatsApp Business versus a personal number?</h2>
<p>If you are running the business from a personal WhatsApp account, moving to WhatsApp Business is worth doing regardless — it is free, keeps the same number, and adds a business profile, catalogue and labels. That is a different change from being handed a new number by a software company.</p>

<h2>Does the assistant lock me out of my own chats?</h2>
<p>No, and this is worth checking with anyone you buy from. You keep full access to your WhatsApp. You can read every conversation, and you can take over any chat at any time — you reply, the assistant steps back, and you hand it back when you are done.</p>
<p>Conversations stay in your WhatsApp and in a log only you and I can open. If you stop using the service, your number, your customers and your history stay exactly where they are.</p>

<h2>What actually changes for the customer</h2>
<p>They message the same number and get an answer in about two seconds instead of the next morning. The assistant states plainly that it is automated and not a person, and they can ask for you whenever they like.</p>
<p>Nothing to install, no new number to save, no form to fill in.</p>
""",
 'faq':[
  ('Do I need a new phone number?',
   'No. It runs on the WhatsApp Business number you already give out. Your customers message the same number as always, and nothing on your cards or listings has to change.'),
  ('Can I still use WhatsApp normally?',
   'Yes. You keep full access, you can read every conversation, and you can take over any chat at any time. You reply and the assistant steps back.'),
  ('What happens to my chats if I cancel?',
   'Nothing. Your number, your customers and your conversation history stay exactly where they are. Message to cancel and it simply stops answering.'),
 ]},

{
 'slug':'whatsapp-auto-reply-vs-ai-assistant.html',
 'title':'WhatsApp Auto-Reply vs AI Assistant | Ownerdeck',
 'desc':'WhatsApp Business away messages and quick replies are free but do not answer the question. Here is the difference, and when each is genuinely enough.',
 'h1':'WhatsApp auto-reply vs an AI assistant',
 'lede':'WhatsApp Business already has away messages and quick replies, and they are free. It is worth being clear about where they stop, and where they are all you need.',
 'body':"""
<h2>What WhatsApp Business already gives you</h2>
<p>An <strong>away message</strong> fires automatically outside your working hours. A <strong>greeting message</strong> fires when someone messages for the first time in a while. <strong>Quick replies</strong> let you insert a saved answer with a keyboard shortcut.</p>
<p>All three are free, built in, and worth turning on. If you are not using them, do that before you spend money on anything.</p>

<h2>Where they stop</h2>
<p>They are fixed text. They cannot look at Saturday, see three automatics free, and quote €135 for three days plus €15 delivery. They cannot answer in Russian because the customer wrote in Russian. They cannot capture the booking.</p>
<p>Which means the customer still has to wait for you. An away message tells them they are waiting; it does not stop them messaging your competitor while they do.</p>

<h2>The comparison, plainly</h2>
<ul>
  <li><strong>Answers instantly:</strong> both.</li>
  <li><strong>Answers the actual question:</strong> auto-reply no, assistant yes.</li>
  <li><strong>Uses your live prices and availability:</strong> auto-reply no, assistant yes.</li>
  <li><strong>Replies in the customer's language:</strong> auto-reply no, assistant yes.</li>
  <li><strong>Captures the booking:</strong> auto-reply no, assistant yes.</li>
  <li><strong>Cost:</strong> auto-reply free, assistant €150 per month.</li>
</ul>

<h2>When an auto-reply is genuinely enough</h2>
<p>If you get a handful of enquiries a week, if they are not time-critical, or if your customers are mostly repeat business who already know your prices — an away message is fine and you should not buy anything. This is not a product every business needs.</p>
<p>It becomes worth paying for when enquiries are frequent, competitive and time-sensitive. Practically: when you are losing bookings overnight in season, and you can count them.</p>

<h2>The middle option people try</h2>
<p>Rule-based chatbots — the ones with buttons and menus — sit between the two. They are cheaper than an assistant and better than an away message, but they break the moment a customer types something the menu did not anticipate, which is most of the time. Tourists do not pick from menus; they ask questions in their own words, often in their own language.</p>

<h2>How to decide</h2>
<p>Count the enquiries that arrived outside your working hours last week, and how many became bookings. If that number is zero and there were more than a few enquiries, the gap is real and measurable. If it is not, turn on your away message and spend the money elsewhere.</p>
""",
 'faq':[
  ('Is WhatsApp Business auto-reply free?',
   'Yes. Away messages, greeting messages and quick replies are all built into WhatsApp Business at no cost, and are worth turning on before paying for anything.'),
  ('Why not just use a rule-based chatbot with buttons?',
   'They break when a customer types something the menu did not anticipate, which is most of the time. Tourists ask questions in their own words and often in their own language.'),
  ('When is an AI assistant worth the money?',
   'When enquiries are frequent, competitive and time-sensitive — practically, when you are losing bookings overnight in season and can count them. If you get a handful of enquiries a week, an away message is enough.'),
 ]},
]


def build(p):
    # cleanUrls is on, so the public URL has no extension even though the
    # file on disk still does. Canonical must name the served URL.
    url = BASE + p['slug'].replace('.html', '')
    faq_html = ''.join(
        f'\n  <h2>{q}</h2>\n  <p>{a}</p>' for q, a in p['faq'])

    schema = {
      "@context":"https://schema.org",
      "@graph":[
        {"@type":"Article","headline":p['h1'],"description":p['desc'],
         "url":url,"inLanguage":"en",
         "author":{"@type":"Person","name":"Mark Saade"},
         "publisher":{"@type":"Organization","name":"Ownerdeck","url":BASE},
         "mainEntityOfPage":url},
        {"@type":"FAQPage","mainEntity":[
          {"@type":"Question","name":q,
           "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p['faq']]},
        {"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Ownerdeck","item":BASE},
          {"@type":"ListItem","position":2,"name":p['h1'],"item":url}]}
      ]}

    head = HEAD
    head = re.sub(r'<title>[^<]*</title>', f"<title>{p['title']}</title>", head, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{p["desc"]}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">',
                  f'<link rel="canonical" href="{url}">', head, count=1)
    # these pages must be indexable — the chassis came from a noindex page
    head = re.sub(r'\s*<meta name="robots" content="noindex">', '', head)
    social = (f'<meta property="og:type" content="article">\n'
              f'<meta property="og:url" content="{url}">\n'
              f'<meta property="og:site_name" content="Ownerdeck">\n'
              f'<meta property="og:title" content="{p["h1"]}">\n'
              f'<meta property="og:description" content="{p["desc"]}">\n'
              f'<meta property="og:image" content="{BASE}og-image.png">\n'
              f'<meta name="twitter:card" content="summary_large_image">\n'
              f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>\n')
    head = head.replace('</head>', social + '</head>')

    body = f"""<main>
  <a href="/" class="back">&larr; Back to ownerdeck.com</a>
  <div class="eyebrow"><span class="s">//</span> Guide</div>
  <h1>{p['h1']}</h1>
  <p class="lede">{p['lede']}</p>
{p['body']}
  <h2>Questions people ask</h2>{faq_html}

  <div class="note">
    <strong>See it working.</strong> Watch it handle a real enquiry, then message the
    live assistant yourself and ask it anything — price, setup, whether it fits your
    business. <a href="/demo">Open the demo</a>, or read
    <a href="/">what Ownerdeck does</a>.
  </div>
</main>"""

    io.open(p['slug'], 'w', encoding='utf-8', newline='').write(head + body + FOOT)
    return p['slug']

for p in PAGES:
    print('  wrote', build(p))
