/* ================================================================
   Ownerdeck — lightweight i18n (v2, keyed to the Base44-style page)
   Languages: en (default), el (Greek), ru (Russian)
   - Text elements use [data-i18n]
   - Elements whose translation contains HTML use [data-i18n-html]
   - Placeholders use [data-i18n-ph]
   Choice is saved to localStorage ("od_lang") and reflected in <html lang>.
   NOTE: el/ru are machine-assisted — have a native speaker review.
================================================================ */
(function () {
  "use strict";

  var I18N = {
    /* ---------------------------------------------------------- EN */
    en: {
      "meta.title": "Ownerdeck — Every customer message, answered.",
      "nav.how": "How it works",
      "nav.features": "Features",
      "nav.pricing": "Pricing",
      "nav.demo": "Demo",
      "nav.faq": "FAQ",
      "cta.demo": "Watch the demo",
      "cta.seeHow": "See how it works",

      "hero.pill": "Live now · handling real bookings 24/7",
      "hero.title": "One AI that answers <span class=\"accent\">WhatsApp, Instagram and your website</span> — and takes the booking.",
      "hero.lede": "Ownerdeck sits on the channels your customers already use. It replies in two seconds, in any language, quotes real availability and prices, and captures bookings — while you sleep.",
      "hero.micro": "No app to install · Set up in a day · You stay in control",
      "hero.ch1": "WhatsApp",
      "hero.ch2": "Instagram DMs",
      "hero.ch3": "Website chat",

      "demo.kicker": "See it live",
      "demo.title": "Watch it handle a real enquiry.",
      "demo.lede": "A short recording of Ownerdeck answering, quoting and closing a booking — then try it yourself, right here on this page.",
      "demo.soonTitle": "Demo video coming soon",
      "demo.soonSub": "In the meantime, try the live demo below — it works right now.",
      "demo.tryKicker": "Try it yourself",
      "demo.tryTitle": "Have a conversation with it.",
      "demo.trySub": "A preset demo standing in for a tour company. Tap a reply to see how it answers.",
      "demo.botStatus": "Ownerdeck · answering now",
      "demo.restart": "Start over",
      "demo.doneTitle": "That whole conversation — no human involved.",
      "demo.doneSub": "This is a preset demo. The real thing uses your services, prices and availability.",
      "demo.channelsTitle": "Like what you saw? Message me directly.",
      "demo.channelsSub": "Pick whichever you actually use — I reply personally.",

      "final.kicker": "See it for yourself",
      "final.title": "Watch it work, then try it yourself.",
      "final.lede": "Two minutes, no form to fill in. Watch a real enquiry get answered, have a go yourself, then message me if it looks useful.",

      "stats.s1": "Conversations handled / month",
      "stats.s2": "Average reply time, any hour",
      "stats.s3": "Languages auto-detected & mirrored",
      "stats.s4": "Never misses an enquiry",

      "problem.kicker": "The problem",
      "problem.title": "Every missed message is a booking you'll never get back.",
      "problem.c1.t": "Enquiries at 2am go unanswered",
      "problem.c1.b": "Most messages arrive after hours. By morning, the customer went elsewhere.",
      "problem.c2.t": "Repetitive questions eat your day",
      "problem.c2.b": "Price, availability, what's included — the same questions, every single day.",
      "problem.c3.t": "Three inboxes, one you",
      "problem.c3.b": "WhatsApp, Instagram DMs, website chat — messages scattered across apps, and something always slips through.",
      "problem.c4.t": "Language barriers lose customers",
      "problem.c4.b": "Russian, German, Greek speakers give up when no one replies in their language.",

      "how.kicker": "How it works",
      "how.title": "One conversation, start to confirmed booking — no human in the loop.",
      "how.s1.t": "A customer messages you — anywhere",
      "how.s1.b": "WhatsApp, an Instagram DM, or the chat on your website. Same places they already use. No new app, no form, no waiting till morning.",
      "how.s2.t": "AI detects language & replies",
      "how.s2.b": "English, Russian, German, Greek and more — auto-detected and mirrored, in ~2 seconds.",
      "how.s3.t": "Checks your live availability",
      "how.s3.b": "Calls your real booking system. Only shows what's actually available on those dates, at that day's real price.",
      "how.s4.t": "Builds the quote",
      "how.s4.b": "Duration × rate, plus add-ons and extras. Accurate, not guessed from memory.",
      "how.s5.t": "Confirms & notifies you",
      "how.s5.b": "Collects only what's missing, sends a booking reference, and pings you the moment it lands.",

      "caps.kicker": "Capabilities",
      "caps.title": "Trained on your services, your prices, your policies.",
      "caps.lede": "It's not a generic chatbot with a company name swapped in. Each deployment learns your specific business.",
      "caps.c1.t": "Answers from your real terms",
      "caps.c1.b": "Pricing, deposits, cancellation windows, what's included, requirements — trained on your actual policies, not guesses.",
      "caps.c2.t": "Live availability & pricing",
      "caps.c2.b": "Calls your real booking system. It never quotes from memory — only what's actually available, at that day's actual price.",
      "caps.c3.t": "Multilingual by default",
      "caps.c3.b": "Auto-detects and mirrors the customer's language. A full booking completed start-to-finish in Russian, zero human involved.",
      "caps.c4.t": "One assistant, every channel",
      "caps.c4.b": "WhatsApp, Instagram DMs and website chat answered by the same trained assistant — same answers, same prices, wherever they ask.",
      "caps.c7.t": "Human handoff anytime",
      "caps.c7.b": "Flip a conversation to manual and the bot steps back. Complaints and edge cases route to a human, never the bot.",
      "caps.c5.t": "Full conversation logs",
      "caps.c5.b": "Every enquiry logged to a sheet you can read — a complete audit trail of what it handled and how.",
      "caps.c6.t": "Enforces your own rules",
      "caps.c6.b": "Minimum notice windows? It routes short-notice requests to a phone call instead of confirming. Your guardrails, not ours.",

      "price.kicker": "Pricing",
      "price.title": "One flat price. Every conversation covered.",
      "price.sub": "Full deployment, trained on your business.",
      "price.per": "/month",
      "price.once": "+ €400 one-time installation",
      "price.f1": "WhatsApp, Instagram DMs & website chat",
      "price.f2": "Unlimited conversations, 24/7",
      "price.f3": "Live integration with your booking system",
      "price.f4": "Multilingual — auto-detects any language",
      "price.f5": "Answers from your real policies & pricing",
      "price.f6": "Human handoff anytime — you stay in control",
      "price.f7": "Full conversation logging & audit trail",
      "price.f8": "Owner alerts the moment a booking lands",
      "price.note": "No long-term contract. Cancel anytime.",

      "faq.kicker": "FAQ",
      "faq.title": "Common questions, honest answers.",
      "faq.q1": "Which channels does it work on?",
      "faq.a1": "WhatsApp, Instagram DMs and the chat widget on your website — all handled by the same assistant, with the same answers and prices. Your customers message you exactly where they already do; nothing changes on their end and there's no new app for them to download.",
      "faq.q2": "How long does setup take?",
      "faq.a2": "About a day from when we have your details. We train the assistant on your business — your services, prices, availability, policies — and connect it to your WhatsApp Business number. You review and approve before it goes live.",
      "faq.q3": "What languages does it support?",
      "faq.a3": "English, Russian, German, Greek and more — detected automatically from the customer's message. If a customer writes in Russian, the assistant replies in Russian. You don't configure anything per conversation.",
      "faq.q4": "What happens if it gets a question it can't answer?",
      "faq.a4": "Anything outside the trained script gets flagged to you immediately. You'll receive a notification with the conversation so you can step in with a personal reply. The customer is told someone will follow up shortly — no dead ends.",
      "faq.q5": "Can I still reply to customers myself?",
      "faq.a5": "Yes. You can take over any conversation at any time. The assistant handles the first response and the routine questions — you stay in charge of anything you want to handle personally.",
      "faq.q6": "What does the €400 installation cover?",
      "faq.a6": "Everything: building and training the assistant on your specific business, connecting it to your WhatsApp Business account, booking-system integration, testing, and a review before go-live. There are no hidden fees — it's a one-time cost.",
      "faq.q7": "Can I cancel?",
      "faq.a7": "Yes, anytime. Month-to-month, no contracts, no cancellation fees. If you cancel, the assistant is deactivated and your WhatsApp returns to normal. We'd obviously prefer you stay — but there's no lock-in.",
      "faq.q8": "Does it work for my type of business?",
      "faq.a8": "If you take bookings or repetitive customer questions via WhatsApp — tours, rentals, salons, clinics, restaurants, or similar service businesses — yes. If you're not sure, send us a message and we'll tell you honestly whether it's a good fit.",
      "faq.q9": "Is my customers' data safe?",
      "faq.a9": "Yes. Conversations stay on WhatsApp's own encrypted platform, and we use them only to run your assistant — never to sell or share. Your data belongs to you, and it's deleted if you cancel. Full details are in our privacy policy.",

      "trust.kicker": "Why Ownerdeck",
      "trust.title": "Set up and supported by a real person.",
      "trust.quote": "“I set up and support every assistant myself. If it doesn't fit your business, I'll tell you straight — no hard sell.”",
      "trust.role": "Founder",

      "contact.kicker": "Get started",
      "contact.title": "See it answer your own WhatsApp.",
      "contact.lede": "Book a 20-minute demo. We'll connect your number, your availability, and your policies — and show it handling a real enquiry live.",
      "form.name": "Your name",
      "form.business": "Business name",
      "form.whatsapp": "WhatsApp number",
      "form.country": "Country",
      "form.volume": "Enquiries / month",
      "form.volumePh": "Select…",
      "form.notes": "Anything we should know?",
      "form.notesPh": "Your booking system, busiest season, languages your customers speak…",
      "form.submit": "Request my demo",
      "form.note": "No commitment. We'll reply within 24 hours. <a href=\"/privacy.html\">Privacy policy</a>.",

      "footer.copyright": "© 2026 Ownerdeck.",
      "footer.privacy": "Privacy Policy"
    },

    /* ---------------------------------------------------------- EL */
    el: {
      "meta.title": "Ownerdeck — Κάθε μήνυμα πελάτη, απαντημένο.",
      "nav.how": "Πώς λειτουργεί",
      "nav.features": "Δυνατότητες",
      "nav.pricing": "Τιμές",
      "nav.demo": "Demo",
      "nav.faq": "Συχνές ερωτήσεις",
      "cta.demo": "Δείτε το demo",
      "cta.seeHow": "Δείτε πώς λειτουργεί",

      "hero.pill": "Ζωντανά τώρα · πραγματικές κρατήσεις 24/7",
      "hero.title": "Μία τεχνητή νοημοσύνη που απαντά σε <span class=\"accent\">WhatsApp, Instagram και στον ιστότοπό σας</span> — και κλείνει την κράτηση.",
      "hero.lede": "Το Ownerdeck βρίσκεται στα κανάλια που ήδη χρησιμοποιούν οι πελάτες σας. Απαντά σε δύο δευτερόλεπτα, σε οποιαδήποτε γλώσσα, δίνει πραγματική διαθεσιμότητα και τιμές και καταγράφει κρατήσεις — ενώ εσείς κοιμάστε.",
      "hero.micro": "Χωρίς εφαρμογή · Έτοιμο σε μία ημέρα · Εσείς έχετε τον έλεγχο",
      "hero.ch1": "WhatsApp",
      "hero.ch2": "Μηνύματα Instagram",
      "hero.ch3": "Chat ιστοσελίδας",

      "demo.kicker": "Δείτε το ζωντανά",
      "demo.title": "Δείτε το να χειρίζεται ένα πραγματικό αίτημα.",
      "demo.lede": "Μια σύντομη καταγραφή του Ownerdeck που απαντά, δίνει τιμή και κλείνει μια κράτηση — και μετά δοκιμάστε το εσείς, εδώ στη σελίδα.",
      "demo.soonTitle": "Το βίντεο demo έρχεται σύντομα",
      "demo.soonSub": "Στο μεταξύ, δοκιμάστε το ζωντανό demo παρακάτω — λειτουργεί ήδη.",
      "demo.tryKicker": "Δοκιμάστε το",
      "demo.tryTitle": "Συνομιλήστε μαζί του.",
      "demo.trySub": "Ένα προκαθορισμένο demo για μια εταιρεία εκδρομών. Πατήστε μια απάντηση για να δείτε πώς απαντά.",
      "demo.botStatus": "Ownerdeck · απαντά τώρα",
      "demo.restart": "Από την αρχή",
      "demo.doneTitle": "Όλη αυτή η συνομιλία — χωρίς κανέναν άνθρωπο.",
      "demo.doneSub": "Αυτό είναι προκαθορισμένο demo. Το πραγματικό χρησιμοποιεί τις δικές σας υπηρεσίες, τιμές και διαθεσιμότητα.",
      "demo.channelsTitle": "Σας άρεσε; Στείλτε μου μήνυμα απευθείας.",
      "demo.channelsSub": "Διαλέξτε όποιο χρησιμοποιείτε — απαντώ προσωπικά.",

      "final.kicker": "Δείτε το μόνοι σας",
      "final.title": "Δείτε το να δουλεύει και δοκιμάστε το.",
      "final.lede": "Δύο λεπτά, χωρίς φόρμα. Δείτε ένα πραγματικό αίτημα να απαντιέται, δοκιμάστε το εσείς και στείλτε μου μήνυμα αν σας φανεί χρήσιμο.",

      "stats.s1": "Συνομιλίες τον μήνα",
      "stats.s2": "Μέσος χρόνος απάντησης, κάθε ώρα",
      "stats.s3": "Γλώσσες με αυτόματη αναγνώριση",
      "stats.s4": "Δεν χάνει ποτέ αίτημα",

      "problem.kicker": "Το πρόβλημα",
      "problem.title": "Κάθε χαμένο μήνυμα είναι μια κράτηση που δεν θα πάρετε ποτέ πίσω.",
      "problem.c1.t": "Τα αιτήματα στις 2 τα ξημερώματα μένουν αναπάντητα",
      "problem.c1.b": "Τα περισσότερα μηνύματα έρχονται εκτός ωραρίου. Μέχρι το πρωί, ο πελάτης έχει πάει αλλού.",
      "problem.c2.t": "Οι επαναλαμβανόμενες ερωτήσεις τρώνε τη μέρα σας",
      "problem.c2.b": "Τιμή, διαθεσιμότητα, τι περιλαμβάνεται — οι ίδιες ερωτήσεις, κάθε μέρα.",
      "problem.c3.t": "Τρία εισερχόμενα, ένας εσείς",
      "problem.c3.b": "WhatsApp, μηνύματα Instagram, chat ιστοσελίδας — μηνύματα διάσπαρτα σε εφαρμογές, και πάντα κάτι ξεφεύγει.",
      "problem.c4.t": "Τα γλωσσικά εμπόδια χάνουν πελάτες",
      "problem.c4.b": "Ρωσόφωνοι, Γερμανοί και Έλληνες πελάτες τα παρατούν όταν κανείς δεν απαντά στη γλώσσα τους.",

      "how.kicker": "Πώς λειτουργεί",
      "how.title": "Μία συνομιλία, από την αρχή έως την επιβεβαιωμένη κράτηση — χωρίς ανθρώπινη παρέμβαση.",
      "how.s1.t": "Ένας πελάτης σας γράφει — από οπουδήποτε",
      "how.s1.b": "WhatsApp, μήνυμα στο Instagram ή το chat της ιστοσελίδας σας. Εκεί που ήδη σας γράφουν. Χωρίς νέα εφαρμογή, χωρίς φόρμα, χωρίς αναμονή μέχρι το πρωί.",
      "how.s2.t": "Η ΤΝ αναγνωρίζει τη γλώσσα και απαντά",
      "how.s2.b": "Αγγλικά, Ρωσικά, Γερμανικά, Ελληνικά και άλλα — αυτόματη αναγνώριση και απάντηση σε ~2 δευτερόλεπτα.",
      "how.s3.t": "Ελέγχει τη ζωντανή διαθεσιμότητά σας",
      "how.s3.b": "Συνδέεται με το πραγματικό σας σύστημα κρατήσεων. Δείχνει μόνο ό,τι είναι όντως διαθέσιμο, στην πραγματική τιμή της ημέρας.",
      "how.s4.t": "Υπολογίζει την προσφορά",
      "how.s4.b": "Διάρκεια × τιμή, συν πρόσθετα και έξτρα. Με ακρίβεια, όχι από μνήμης.",
      "how.s5.t": "Επιβεβαιώνει και σας ειδοποιεί",
      "how.s5.b": "Ζητά μόνο ό,τι λείπει, στέλνει αριθμό κράτησης και σας ειδοποιεί τη στιγμή που ολοκληρώνεται.",

      "caps.kicker": "Δυνατότητες",
      "caps.title": "Εκπαιδευμένο στις υπηρεσίες, τις τιμές και τις πολιτικές σας.",
      "caps.lede": "Δεν είναι ένα γενικό chatbot με αλλαγμένο όνομα εταιρείας. Κάθε εγκατάσταση μαθαίνει τη συγκεκριμένη επιχείρησή σας.",
      "caps.c1.t": "Απαντά με τους πραγματικούς σας όρους",
      "caps.c1.b": "Τιμές, προκαταβολές, πολιτικές ακύρωσης, τι περιλαμβάνεται — εκπαιδευμένο στις πραγματικές σας πολιτικές, όχι σε εικασίες.",
      "caps.c2.t": "Ζωντανή διαθεσιμότητα και τιμές",
      "caps.c2.b": "Συνδέεται με το πραγματικό σας σύστημα κρατήσεων. Ποτέ δεν απαντά από μνήμης — μόνο ό,τι είναι όντως διαθέσιμο, στη σημερινή τιμή.",
      "caps.c3.t": "Πολύγλωσσο εξ ορισμού",
      "caps.c3.b": "Αναγνωρίζει αυτόματα τη γλώσσα του πελάτη. Ολόκληρη κράτηση ολοκληρωμένη στα Ρωσικά, χωρίς καμία ανθρώπινη συμμετοχή.",
      "caps.c4.t": "Ένας βοηθός, όλα τα κανάλια",
      "caps.c4.b": "WhatsApp, μηνύματα Instagram και chat ιστοσελίδας από τον ίδιο εκπαιδευμένο βοηθό — ίδιες απαντήσεις, ίδιες τιμές, όπου κι αν ρωτήσουν.",
      "caps.c7.t": "Παράδοση σε άνθρωπο ανά πάσα στιγμή",
      "caps.c7.b": "Γυρίστε μια συνομιλία σε χειροκίνητη λειτουργία και το bot αποσύρεται. Παράπονα και ειδικές περιπτώσεις πάνε πάντα σε άνθρωπο.",
      "caps.c5.t": "Πλήρες αρχείο συνομιλιών",
      "caps.c5.b": "Κάθε αίτημα καταγράφεται σε φύλλο που μπορείτε να διαβάσετε — πλήρες ιστορικό του τι χειρίστηκε και πώς.",
      "caps.c6.t": "Εφαρμόζει τους δικούς σας κανόνες",
      "caps.c6.b": "Ελάχιστος χρόνος ειδοποίησης; Τα αιτήματα τελευταίας στιγμής πάνε σε τηλεφώνημα αντί για αυτόματη επιβεβαίωση. Οι δικοί σας κανόνες, όχι οι δικοί μας.",

      "price.kicker": "Τιμές",
      "price.title": "Μία σταθερή τιμή. Κάθε συνομιλία καλυμμένη.",
      "price.sub": "Πλήρης εγκατάσταση, εκπαιδευμένο στην επιχείρησή σας.",
      "price.per": "/μήνα",
      "price.once": "+ €400 εφάπαξ εγκατάσταση",
      "price.f1": "WhatsApp, μηνύματα Instagram & chat ιστοσελίδας",
      "price.f2": "Απεριόριστες συνομιλίες, 24/7",
      "price.f3": "Ζωντανή σύνδεση με το σύστημα κρατήσεών σας",
      "price.f4": "Πολύγλωσσο — αυτόματη αναγνώριση γλώσσας",
      "price.f5": "Απαντά με τις πραγματικές σας πολιτικές και τιμές",
      "price.f6": "Παράδοση σε άνθρωπο ανά πάσα στιγμή — εσείς έχετε τον έλεγχο",
      "price.f7": "Πλήρης καταγραφή και ιστορικό συνομιλιών",
      "price.f8": "Ειδοποίηση τη στιγμή που έρχεται κράτηση",
      "price.note": "Χωρίς μακροχρόνιο συμβόλαιο. Ακύρωση όποτε θέλετε.",

      "faq.kicker": "Συχνές ερωτήσεις",
      "faq.title": "Συχνές ερωτήσεις, ειλικρινείς απαντήσεις.",
      "faq.q1": "Σε ποια κανάλια λειτουργεί;",
      "faq.a1": "WhatsApp, μηνύματα Instagram και το chat της ιστοσελίδας σας — όλα από τον ίδιο βοηθό, με τις ίδιες απαντήσεις και τιμές. Οι πελάτες σας γράφουν ακριβώς εκεί που ήδη γράφουν· τίποτα δεν αλλάζει για εκείνους και δεν χρειάζονται καμία νέα εφαρμογή.",
      "faq.q2": "Πόσο χρόνο παίρνει η εγκατάσταση;",
      "faq.a2": "Περίπου μία ημέρα από τη στιγμή που έχουμε τα στοιχεία σας. Εκπαιδεύουμε τον βοηθό στην επιχείρησή σας — υπηρεσίες, τιμές, διαθεσιμότητα, πολιτικές — και τον συνδέουμε με τον αριθμό σας στο WhatsApp Business. Τον ελέγχετε και τον εγκρίνετε πριν ενεργοποιηθεί.",
      "faq.q3": "Ποιες γλώσσες υποστηρίζει;",
      "faq.a3": "Αγγλικά, Ρωσικά, Γερμανικά, Ελληνικά και άλλα — με αυτόματη αναγνώριση από το μήνυμα του πελάτη. Αν ένας πελάτης γράψει στα Ρωσικά, ο βοηθός απαντά στα Ρωσικά.",
      "faq.q4": "Τι γίνεται αν λάβει μια ερώτηση που δεν μπορεί να απαντήσει;",
      "faq.a4": "Ό,τι ξεφεύγει από το εκπαιδευμένο σενάριο επισημαίνεται σε εσάς αμέσως. Λαμβάνετε ειδοποίηση με τη συνομιλία ώστε να παρέμβετε με προσωπική απάντηση. Ο πελάτης ενημερώνεται ότι κάποιος θα επικοινωνήσει σύντομα.",
      "faq.q5": "Μπορώ να απαντώ και ο ίδιος στους πελάτες;",
      "faq.a5": "Ναι. Μπορείτε να αναλάβετε οποιαδήποτε συνομιλία ανά πάσα στιγμή. Ο βοηθός χειρίζεται την πρώτη απάντηση και τις συνηθισμένες ερωτήσεις — εσείς έχετε τον έλεγχο σε ό,τι θέλετε να χειριστείτε προσωπικά.",
      "faq.q6": "Τι καλύπτει η εγκατάσταση των €400;",
      "faq.a6": "Τα πάντα: δημιουργία και εκπαίδευση του βοηθού στη συγκεκριμένη επιχείρησή σας, σύνδεση με τον λογαριασμό σας στο WhatsApp Business, σύνδεση με το σύστημα κρατήσεων, δοκιμές και έλεγχο πριν την ενεργοποίηση. Χωρίς κρυφές χρεώσεις — εφάπαξ κόστος.",
      "faq.q7": "Μπορώ να ακυρώσω;",
      "faq.a7": "Ναι, όποτε θέλετε. Μηνιαία βάση, χωρίς συμβόλαια, χωρίς χρεώσεις ακύρωσης. Αν ακυρώσετε, ο βοηθός απενεργοποιείται και το WhatsApp σας επανέρχεται στο κανονικό.",
      "faq.q8": "Λειτουργεί για τον τύπο της δικής μου επιχείρησης;",
      "faq.a8": "Αν δέχεστε κρατήσεις ή επαναλαμβανόμενες ερωτήσεις πελατών μέσω WhatsApp — εκδρομές, ενοικιάσεις, κομμωτήρια, κλινικές, εστιατόρια ή παρόμοιες επιχειρήσεις — ναι. Αν δεν είστε σίγουροι, στείλτε μας μήνυμα και θα σας πούμε ειλικρινά.",
      "faq.q9": "Είναι ασφαλή τα δεδομένα των πελατών μου;",
      "faq.a9": "Ναι. Οι συνομιλίες παραμένουν στην κρυπτογραφημένη πλατφόρμα του WhatsApp και τις χρησιμοποιούμε μόνο για τη λειτουργία του βοηθού σας — ποτέ για πώληση ή κοινοποίηση. Τα δεδομένα σας ανήκουν σε εσάς και διαγράφονται αν ακυρώσετε.",

      "trust.kicker": "Γιατί Ownerdeck",
      "trust.title": "Ρύθμιση και υποστήριξη από έναν πραγματικό άνθρωπο.",
      "trust.quote": "“Ρυθμίζω και υποστηρίζω κάθε βοηθό ο ίδιος. Αν δεν ταιριάζει στην επιχείρησή σας, θα σας το πω ειλικρινά — χωρίς πίεση.”",
      "trust.role": "Ιδρυτής · Λάρνακα, Κύπρος",

      "contact.kicker": "Ξεκινήστε",
      "contact.title": "Δείτε το να απαντά στο δικό σας WhatsApp.",
      "contact.lede": "Κλείστε ένα demo 20 λεπτών. Θα συνδέσουμε τον αριθμό, τη διαθεσιμότητα και τις πολιτικές σας — και θα το δείτε να χειρίζεται ένα πραγματικό αίτημα ζωντανά.",
      "form.name": "Το όνομά σας",
      "form.business": "Όνομα επιχείρησης",
      "form.whatsapp": "Αριθμός WhatsApp",
      "form.country": "Χώρα",
      "form.volume": "Αιτήματα / μήνα",
      "form.volumePh": "Επιλέξτε…",
      "form.notes": "Κάτι που πρέπει να γνωρίζουμε;",
      "form.notesPh": "Το σύστημα κρατήσεών σας, η πιο πολυάσχολη σεζόν, οι γλώσσες των πελατών σας…",
      "form.submit": "Ζητήστε demo",
      "form.note": "Καμία δέσμευση. Θα απαντήσουμε εντός 24 ωρών. <a href=\"/privacy.html\">Πολιτική απορρήτου</a>.",

      "footer.copyright": "© 2026 Ownerdeck. Φτιαγμένο στην Κύπρο.",
      "footer.privacy": "Πολιτική απορρήτου"
    },

    /* ---------------------------------------------------------- RU */
    ru: {
      "meta.title": "Ownerdeck — Каждое сообщение клиента с ответом.",
      "nav.how": "Как это работает",
      "nav.features": "Возможности",
      "nav.pricing": "Цены",
      "nav.demo": "Демо",
      "nav.faq": "Вопросы",
      "cta.demo": "Смотреть демо",
      "cta.seeHow": "Как это работает",

      "hero.pill": "Уже работает · реальные брони 24/7",
      "hero.title": "Один ИИ, который отвечает в <span class=\"accent\">WhatsApp, Instagram и на вашем сайте</span> — и оформляет бронь.",
      "hero.lede": "Ownerdeck работает в тех каналах, которыми ваши клиенты уже пользуются. Отвечает за две секунды, на любом языке, называет реальную доступность и цены и оформляет брони — пока вы спите.",
      "hero.micro": "Без установки приложений · Настройка за день · Контроль остаётся у вас",
      "hero.ch1": "WhatsApp",
      "hero.ch2": "Директ Instagram",
      "hero.ch3": "Чат на сайте",

      "demo.kicker": "Посмотрите вживую",
      "demo.title": "Посмотрите, как он обрабатывает реальный запрос.",
      "demo.lede": "Короткая запись того, как Ownerdeck отвечает, считает цену и закрывает бронь — а затем попробуйте сами, прямо на этой странице.",
      "demo.soonTitle": "Видео-демо скоро появится",
      "demo.soonSub": "А пока попробуйте живое демо ниже — оно уже работает.",
      "demo.tryKicker": "Попробуйте сами",
      "demo.tryTitle": "Поговорите с ним.",
      "demo.trySub": "Заготовленное демо для экскурсионной компании. Нажмите на ответ, чтобы увидеть, как он отвечает.",
      "demo.botStatus": "Ownerdeck · отвечает сейчас",
      "demo.restart": "Начать заново",
      "demo.doneTitle": "Весь этот диалог — без участия человека.",
      "demo.doneSub": "Это заготовленное демо. Настоящий ассистент использует ваши услуги, цены и доступность.",
      "demo.channelsTitle": "Понравилось? Напишите мне напрямую.",
      "demo.channelsSub": "Выберите удобный канал — отвечаю лично.",

      "final.kicker": "Убедитесь сами",
      "final.title": "Посмотрите, как он работает, и попробуйте сами.",
      "final.lede": "Две минуты, никаких форм. Посмотрите, как обрабатывается реальный запрос, попробуйте сами — и напишите мне, если это вам подходит.",

      "stats.s1": "Диалогов в месяц",
      "stats.s2": "Среднее время ответа, в любой час",
      "stats.s3": "Языков определяется автоматически",
      "stats.s4": "Не пропускает ни одного запроса",

      "problem.kicker": "Проблема",
      "problem.title": "Каждое пропущенное сообщение — это бронь, которую уже не вернуть.",
      "problem.c1.t": "Запросы в 2 ночи остаются без ответа",
      "problem.c1.b": "Большинство сообщений приходит в нерабочее время. К утру клиент уже ушёл к другим.",
      "problem.c2.t": "Однотипные вопросы съедают весь день",
      "problem.c2.b": "Цена, доступность, что включено — одни и те же вопросы, каждый день.",
      "problem.c3.t": "Три входящих, а вы один",
      "problem.c3.b": "WhatsApp, директ Instagram, чат на сайте — сообщения разбросаны по приложениям, и что-то всегда теряется.",
      "problem.c4.t": "Языковой барьер теряет клиентов",
      "problem.c4.b": "Русско-, немецко- и грекоязычные клиенты сдаются, если им не отвечают на их языке.",

      "how.kicker": "Как это работает",
      "how.title": "Один диалог — от первого сообщения до подтверждённой брони, без участия человека.",
      "how.s1.t": "Клиент пишет вам — откуда угодно",
      "how.s1.b": "WhatsApp, директ в Instagram или чат на вашем сайте. Там же, где пишут и сейчас. Без нового приложения, без формы, без ожидания до утра.",
      "how.s2.t": "ИИ определяет язык и отвечает",
      "how.s2.b": "Английский, русский, немецкий, греческий и другие — автоопределение и ответ за ~2 секунды.",
      "how.s3.t": "Проверяет реальную доступность",
      "how.s3.b": "Обращается к вашей реальной системе бронирования. Показывает только то, что действительно свободно, по актуальной цене.",
      "how.s4.t": "Составляет расчёт",
      "how.s4.b": "Длительность × тариф плюс дополнения. Точно, а не по памяти.",
      "how.s5.t": "Подтверждает и уведомляет вас",
      "how.s5.b": "Запрашивает только недостающее, отправляет номер брони и сразу уведомляет вас.",

      "caps.kicker": "Возможности",
      "caps.title": "Обучен на ваших услугах, ценах и правилах.",
      "caps.lede": "Это не шаблонный чат-бот с подставленным названием компании. Каждое внедрение изучает именно ваш бизнес.",
      "caps.c1.t": "Отвечает по вашим реальным условиям",
      "caps.c1.b": "Цены, депозиты, условия отмены, что включено — обучен на ваших реальных правилах, а не на догадках.",
      "caps.c2.t": "Реальная доступность и цены",
      "caps.c2.b": "Обращается к вашей системе бронирования. Никогда не отвечает по памяти — только то, что реально свободно, по сегодняшней цене.",
      "caps.c3.t": "Многоязычный по умолчанию",
      "caps.c3.b": "Автоматически определяет язык клиента. Полная бронь от начала до конца на русском — без участия человека.",
      "caps.c4.t": "Один ассистент, все каналы",
      "caps.c4.b": "WhatsApp, директ Instagram и чат на сайте обслуживает один и тот же обученный ассистент — одинаковые ответы и цены, где бы ни спросили.",
      "caps.c7.t": "Передача человеку в любой момент",
      "caps.c7.b": "Переведите диалог в ручной режим — и бот отступает. Жалобы и сложные случаи всегда идут человеку.",
      "caps.c5.t": "Полные логи диалогов",
      "caps.c5.b": "Каждый запрос записывается в таблицу, которую вы можете читать — полная история того, что и как обработано.",
      "caps.c6.t": "Соблюдает ваши правила",
      "caps.c6.b": "Минимальный срок брони? Запросы в последний момент направляются на звонок, а не подтверждаются автоматически. Ваши ограничения, не наши.",

      "price.kicker": "Цены",
      "price.title": "Одна фиксированная цена. Все диалоги включены.",
      "price.sub": "Полное внедрение, обучен на вашем бизнесе.",
      "price.per": "/мес",
      "price.once": "+ €400 разовая установка",
      "price.f1": "WhatsApp, директ Instagram и чат на сайте",
      "price.f2": "Неограниченные диалоги, 24/7",
      "price.f3": "Живая интеграция с вашей системой бронирования",
      "price.f4": "Многоязычный — автоопределение любого языка",
      "price.f5": "Отвечает по вашим реальным правилам и ценам",
      "price.f6": "Передача человеку в любой момент — контроль у вас",
      "price.f7": "Полное логирование диалогов",
      "price.f8": "Уведомление владельцу сразу после брони",
      "price.note": "Без долгосрочного контракта. Отмена в любой момент.",

      "faq.kicker": "Вопросы",
      "faq.title": "Частые вопросы, честные ответы.",
      "faq.q1": "В каких каналах это работает?",
      "faq.a1": "WhatsApp, директ Instagram и чат на вашем сайте — всё обслуживает один ассистент, с одинаковыми ответами и ценами. Клиенты пишут ровно туда, куда пишут и сейчас; для них ничего не меняется и ничего скачивать не нужно.",
      "faq.q2": "Сколько занимает настройка?",
      "faq.a2": "Около дня с момента получения ваших данных. Мы обучаем ассистента на вашем бизнесе — услуги, цены, доступность, правила — и подключаем его к вашему номеру WhatsApp Business. Вы проверяете и одобряете перед запуском.",
      "faq.q3": "Какие языки поддерживаются?",
      "faq.a3": "Английский, русский, немецкий, греческий и другие — определяются автоматически по сообщению клиента. Если клиент пишет по-русски, ассистент отвечает по-русски.",
      "faq.q4": "Что если будет вопрос, на который он не сможет ответить?",
      "faq.a4": "Всё, что выходит за рамки обученного сценария, сразу отмечается для вас. Вы получите уведомление с диалогом, чтобы вмешаться с личным ответом. Клиенту сообщают, что с ним скоро свяжутся.",
      "faq.q5": "Могу ли я отвечать клиентам сам?",
      "faq.a5": "Да. Вы можете взять любой диалог на себя в любой момент. Ассистент берёт на себя первый ответ и рутинные вопросы — вы остаётесь главным во всём, что хотите вести лично.",
      "faq.q6": "Что входит в установку за €400?",
      "faq.a6": "Всё: создание и обучение ассистента под ваш конкретный бизнес, подключение к вашему аккаунту WhatsApp Business, интеграция с системой бронирования, тестирование и проверка перед запуском. Скрытых платежей нет — это разовая оплата.",
      "faq.q7": "Можно ли отменить?",
      "faq.a7": "Да, в любой момент. Помесячно, без договоров, без штрафов за отмену. Если вы отмените, ассистент отключается, и ваш WhatsApp возвращается к обычному режиму.",
      "faq.q8": "Подходит ли это для моего типа бизнеса?",
      "faq.a8": "Если вы принимаете брони или повторяющиеся вопросы клиентов через WhatsApp — экскурсии, аренда, салоны, клиники, рестораны или похожий сервисный бизнес — да. Если не уверены, напишите нам, и мы честно скажем.",
      "faq.q9": "Данные моих клиентов в безопасности?",
      "faq.a9": "Да. Переписка остаётся в зашифрованной среде самого WhatsApp, и мы используем её только для работы вашего ассистента — никогда для продажи или передачи. Ваши данные принадлежат вам и удаляются при отмене.",

      "trust.kicker": "Почему Ownerdeck",
      "trust.title": "Настройка и поддержка — от живого человека.",
      "trust.quote": "“Я лично настраиваю и поддерживаю каждого ассистента. Если он не подойдёт вашему бизнесу — скажу честно, без навязывания.”",
      "trust.role": "Основатель · Ларнака, Кипр",

      "contact.kicker": "Начать",
      "contact.title": "Посмотрите, как он отвечает в вашем WhatsApp.",
      "contact.lede": "Запишитесь на 20-минутное демо. Мы подключим ваш номер, доступность и правила — и покажем, как он обрабатывает реальный запрос вживую.",
      "form.name": "Ваше имя",
      "form.business": "Название бизнеса",
      "form.whatsapp": "Номер WhatsApp",
      "form.country": "Страна",
      "form.volume": "Запросов / месяц",
      "form.volumePh": "Выберите…",
      "form.notes": "Что нам стоит знать?",
      "form.notesPh": "Ваша система бронирования, самый загруженный сезон, языки ваших клиентов…",
      "form.submit": "Запросить демо",
      "form.note": "Без обязательств. Мы ответим в течение 24 часов. <a href=\"/privacy.html\">Политика конфиденциальности</a>.",

      "footer.copyright": "© 2026 Ownerdeck. Сделано на Кипре.",
      "footer.privacy": "Политика конфиденциальности"
    }
  };

  var SUPPORTED = ["en", "el", "ru"];
  var STORAGE_KEY = "od_lang";

  function pickInitial() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;
    } catch (e) {}
    var nav = (navigator.language || "en").slice(0, 2).toLowerCase();
    return SUPPORTED.indexOf(nav) !== -1 ? nav : "en";
  }

  function t(lang, key) {
    var d = I18N[lang] || I18N.en;
    return (key in d) ? d[key] : (I18N.en[key] !== undefined ? I18N.en[key] : null);
  }

  function apply(lang) {
    if (SUPPORTED.indexOf(lang) === -1) lang = "en";
    document.documentElement.setAttribute("lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = t(lang, el.getAttribute("data-i18n"));
      if (v !== null) el.textContent = v;
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var v = t(lang, el.getAttribute("data-i18n-html"));
      if (v !== null) el.innerHTML = v;
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      var v = t(lang, el.getAttribute("data-i18n-ph"));
      if (v !== null) el.setAttribute("placeholder", v);
    });

    var title = t(lang, "meta.title");
    if (title) document.title = title;

    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}

    document.querySelectorAll(".lang-select").forEach(function (sel) {
      if (sel.value !== lang) sel.value = lang;
    });
  }

  function init() {
    var lang = pickInitial();
    apply(lang);
    document.querySelectorAll(".lang-select").forEach(function (sel) {
      sel.value = lang;
      sel.addEventListener("change", function () { apply(this.value); });
    });
  }

  var current = "en";
  var _apply = apply;
  apply = function (lang) { current = (SUPPORTED.indexOf(lang) === -1) ? "en" : lang; _apply(current); };

  window.OD_I18N = {
    apply: apply,
    supported: SUPPORTED,
    // used by demo.js for dynamically injected markup
    t: function (key) { return t(current, key); },
    refresh: function () { _apply(current); }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
