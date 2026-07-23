/* ================================================================
   OwnerDeck — lightweight i18n
   Languages: en (default), el (Greek), ru (Russian)
   - Text elements use [data-i18n]
   - Elements whose translation contains HTML use [data-i18n-html]
   - Placeholders use [data-i18n-ph]
   Choice is saved to localStorage ("od_lang") and reflected in <html lang>.
   NOTE: el/ru translations are machine-assisted — have a native speaker
   review before relying on them in production.
================================================================ */
(function () {
  "use strict";

  var I18N = {
    /* ---------------------------------------------------------- EN */
    en: {
      "meta.title": "OwnerDeck — Never lose a booking to a slow reply",
      "cta.getStarted": "Get started",
      "cta.seeHow": "See how it works",

      "nav.how": "How it works",
      "nav.features": "Features",
      "nav.pricing": "Pricing",
      "nav.faq": "FAQ",

      "hero.eyebrow": "Now live in Cyprus",
      "hero.title": "Never lose a booking to <em>a&nbsp;slow reply.</em>",
      "hero.lede": "Your WhatsApp assistant answers every customer inquiry in seconds — 24/7, in their language. While you're with a customer, on the road, or off the clock.",
      "hero.builtFor": "Built for salons · clinics · rentals · tours · any business that books over WhatsApp",
      "hero.trust": "Already handling live bookings in Cyprus — average reply time under 5 seconds",

      "chat.online": "Online",
      "chat.speed": "Replied in 4 seconds",

      "problem.eyebrow": "The problem",
      "problem.title": "Customers don't wait. <em>They move on.</em>",
      "problem.lede": "When someone wants to book, they message two or three businesses at once and go with whoever replies first. Speed isn't a nice-to-have — it's the whole game.",
      "problem.c1.title": "They message everyone at once",
      "problem.c1.body": "Customers open WhatsApp, send the same question to two or three businesses, and book with whoever replies fastest. You're not competing on price — you're competing on speed.",
      "problem.c2.title": "Busy hours mean you're never free",
      "problem.c2.body": "You're mid-appointment, serving a customer, or just trying to have lunch. Your phone fills up with inquiries you can't answer in time — so you lose bookings you never knew you had.",
      "problem.c3.title": "Every slow reply costs real money",
      "problem.c3.body": "A missed inquiry isn't a minor inconvenience — it's real revenue gone to a faster competitor. Multiply that across a month and the cost of not automating becomes obvious.",

      "how.eyebrow": "How it works",
      "how.title": "Three steps. <em>Zero missed inquiries.</em>",
      "how.lede": "No new app for your customers. No new platform for you to learn. It plugs straight into WhatsApp and runs in the background.",
      "how.s1.num": "01 · Inquiry",
      "how.s1.title": "Arrives on WhatsApp",
      "how.s1.body": "A customer messages your WhatsApp number asking about availability, price, or how to book. Exactly as they do today — nothing changes on their end.",
      "how.s2.num": "02 · Reply",
      "how.s2.title": "Instant reply in their language",
      "how.s2.body": "Your assistant responds within seconds — in English, Russian, Hebrew, Polish, German, or Greek, automatically detected. It answers availability, price, and policy questions from your playbook.",
      "how.s3.num": "03 · Capture",
      "how.s3.title": "Booking captured, you're pinged",
      "how.s3.body": "Date, time, party size, and activity are captured and logged. Your calendar updates automatically. You get pinged only when something needs a personal touch — anything outside the script comes straight to you.",

      "feat.eyebrow": "What you get",
      "feat.title": "Built for busy operators.",
      "feat.lede": "Not a generic chatbot. Trained on your business, your prices, your policies — and available around the clock so you don't have to be.",
      "feat.f1.tag": "Always on",
      "feat.f1.title": "Instant replies, 24/7",
      "feat.f1.body": "Every inquiry gets answered in seconds — 2am or 2pm, Sunday or August bank holiday. No more \"sorry for the late reply\" messages. No more bookings lost while you sleep.",
      "feat.f2.tag": "Multilingual",
      "feat.f2.title": "Speaks your customers' language",
      "feat.f2.body": "English, Russian, Hebrew, Polish, German, and Greek — detected automatically from the first message. No setup per language. Your assistant handles the conversation natively regardless of where the tourist is from.",
      "feat.f3.tag": "Booking capture",
      "feat.f3.title": "Details logged, calendar updated",
      "feat.f3.body": "Date, time, party size, and activity captured from the conversation and dropped into your calendar. Booking summaries sent to you as soon as a slot is confirmed — no manual entry needed.",
      "feat.f4.tag": "Owner in control",
      "feat.f4.title": "Pinged for anything unusual",
      "feat.f4.body": "Group of 20? Unusual request? Complaint? Anything outside the trained script is flagged immediately and handed to you. You stay in control of every edge case without watching the chat 24/7.",
      "feat.f4.secondary": "Also handles Instagram DMs",

      "price.eyebrow": "Pricing",
      "price.title": "Simple pricing. <em>No surprises.</em>",
      "price.lede": "One setup fee, one monthly rate. Cancel any time. Your assistant is live within 48 hours of signing up.",
      "price.cardEyebrow": "Full service · everything included",
      "price.setup": "one-time setup",
      "price.month": "per month",
      "price.terms": "Cancel anytime · No lock-in · Live in 48 hours",
      "price.f1": "Full assistant setup & training",
      "price.f2": "Multilingual (6 languages)",
      "price.f3": "Automatic booking capture",
      "price.f4": "Calendar integration",
      "price.f5": "Owner notifications",
      "price.f6": "Ongoing support & updates",
      "price.f7": "WhatsApp Business integration",
      "price.f8": "48-hour go-live",
      "price.footnote": "No commitment at this stage — tell us about your business and we'll be in touch within 24 hours.",

      "contact.eyebrow": "Get started",
      "contact.title": "Ready to stop missing bookings?",
      "contact.lede": "Tell us about your business. We'll reach out within 24 hours to get you set up — no commitment, no sales call.",
      "form.name": "Your name",
      "form.business": "Business name",
      "form.whatsapp": "WhatsApp number",
      "form.type": "What do you operate?",
      "form.typePlaceholder": "Select your business type",
      "form.type.salon": "Salon / spa / clinic",
      "form.type.restaurant": "Restaurant / café",
      "form.type.tourism": "Boat charter / watersports / tours",
      "form.type.car": "Car rental",
      "form.type.other": "Other",
      "form.notes": "Anything else?",
      "form.optional": "(optional)",
      "form.notesPlaceholder": "How many inquiries do you get per day? Any specific languages? Anything that would help us prepare…",
      "form.submit": "Send my details",
      "form.footnote": "No commitment. We'll reply within 24 hours. <a href=\"/privacy.html\">Privacy policy</a>.",

      "faq.eyebrow": "FAQ",
      "faq.title": "Common questions, <em>honest answers.</em>",
      "faq.q1": "Does my customer need to download anything?",
      "faq.a1": "No. Your customers message your existing WhatsApp number exactly as they do today. Nothing changes on their end — they don't need a new app, account, or link. The assistant just makes you reply faster.",
      "faq.q2": "How long does setup take?",
      "faq.a2": "48 hours from when we have your details. We train the assistant on your business — your services, prices, availability, policies — and connect it to your WhatsApp Business number. You review and approve before it goes live.",
      "faq.q3": "What languages does it support?",
      "faq.a3": "English, Russian, Hebrew, Polish, German, and Greek — detected automatically from the customer's message. If a tourist writes in Russian, the assistant replies in Russian. You don't configure anything per conversation.",
      "faq.q4": "What happens if it gets a question it can't answer?",
      "faq.a4": "Anything outside the trained script gets flagged to you immediately. You'll receive a notification with the conversation so you can step in with a personal reply. The customer is told someone will follow up shortly — no dead ends.",
      "faq.q5": "Can I still reply to customers myself?",
      "faq.a5": "Yes. You can take over any conversation at any time. The assistant handles the first response and the routine questions — you stay in charge of anything you want to handle personally.",
      "faq.q6": "What does the €400 setup cover?",
      "faq.a6": "Everything: building and training the assistant on your specific business, connecting it to your WhatsApp Business account, calendar integration, testing, and a review call before go-live. There are no hidden fees — the setup is a one-time cost.",
      "faq.q7": "Can I cancel?",
      "faq.a7": "Yes, anytime. Month-to-month, no contracts, no cancellation fees. If you cancel, the assistant is deactivated and your WhatsApp returns to normal. We'd obviously prefer you stay — but there's no lock-in.",
      "faq.q8": "Does it work for my type of business?",
      "faq.a8": "If you take bookings or repetitive customer questions via WhatsApp — salons, clinics, rentals, tours, restaurants, or similar service businesses — yes. If you're not sure, send us a message and we'll tell you honestly whether it's a good fit.",
      "faq.q9": "Is my customers' data safe?",
      "faq.a9": "Yes. Conversations stay on WhatsApp's own encrypted platform, and we use them only to run your assistant — never to sell or share. Your data belongs to you, and it's deleted if you cancel. Full details are in our privacy policy.",

      "final.title": "Stop losing bookings. <em>Start today.</em>",
      "final.lede": "Takes 2 minutes to fill in the form. We'll be in touch within 24 hours and your assistant can be live in 48.",

      "trust.eyebrow": "Why OwnerDeck",
      "trust.title": "Set up and supported by <em>a real person.</em>",
      "trust.quote": "“I set up and support every assistant myself. If it doesn't fit your business, I'll tell you straight — no hard sell.”",
      "trust.role": "Founder · Larnaca, Cyprus",

      "footer.tagline": "AI-powered WhatsApp booking assistant for businesses in Cyprus.",
      "footer.product": "Product",
      "footer.company": "Company",
      "footer.getInTouch": "Get in touch",
      "footer.privacy": "Privacy Policy",
      "footer.copyright": "© 2026 OwnerDeck. Built in Cyprus.",
      "footer.location": "Larnaca, Cyprus"
    },

    /* ---------------------------------------------------------- EL */
    el: {
      "meta.title": "OwnerDeck — Μη χάνετε ποτέ μια κράτηση από μια αργή απάντηση",
      "cta.getStarted": "Ξεκινήστε",
      "cta.seeHow": "Δείτε πώs λειτουργεί",

      "nav.how": "Πώς λειτουργεί",
      "nav.features": "Δυνατότητες",
      "nav.pricing": "Τιμές",
      "nav.faq": "Συχνές ερωτήσεις",

      "hero.eyebrow": "Διαθέσιμο τώρα στην Κύπρο",
      "hero.title": "Μη χάνετε ποτέ μια κράτηση από <em>μια αργή απάντηση.</em>",
      "hero.lede": "Ο βοηθός σας στο WhatsApp απαντά σε κάθε ερώτηση πελάτη μέσα σε δευτερόλεπτα — 24/7, στη γλώσσα του. Ενώ εσείς εξυπηρετείτε έναν πελάτη, είστε στον δρόμο ή εκτός ωραρίου.",
      "hero.builtFor": "Φτιαγμένο για κομμωτήρια · κλινικές · ενοικιάσεις · εκδρομές · κάθε επιχείρηση που δέχεται κρατήσεις μέσω WhatsApp",
      "hero.trust": "Ήδη διαχειριζόμαστε ζωντανές κρατήσεις στην Κύπρο — μέσος χρόνος απάντησης κάτω από 5 δευτερόλεπτα",

      "chat.online": "Σε σύνδεση",
      "chat.speed": "Απάντηση σε 4 δευτερόλεπτα",

      "problem.eyebrow": "Το πρόβλημα",
      "problem.title": "Οι πελάτες δεν περιμένουν. <em>Προχωρούν παρακάτω.</em>",
      "problem.lede": "Όταν κάποιος θέλει να κλείσει, στέλνει μήνυμα σε δύο-τρεις επιχειρήσεις ταυτόχρονα και επιλέγει όποιον απαντήσει πρώτος. Η ταχύτητα δεν είναι πολυτέλεια — είναι όλο το παιχνίδι.",
      "problem.c1.title": "Στέλνουν μήνυμα σε όλους ταυτόχρονα",
      "problem.c1.body": "Οι πελάτες ανοίγουν το WhatsApp, στέλνουν την ίδια ερώτηση σε δύο-τρεις επιχειρήσεις και κλείνουν με όποιον απαντήσει πιο γρήγορα. Δεν ανταγωνίζεστε στην τιμή — ανταγωνίζεστε στην ταχύτητα.",
      "problem.c2.title": "Οι ώρες αιχμής σημαίνουν ότι δεν είστε ποτέ ελεύθεροι",
      "problem.c2.body": "Είστε στη μέση ενός ραντεβού, εξυπηρετείτε έναν πελάτη ή απλώς προσπαθείτε να φάτε. Το τηλέφωνό σας γεμίζει με αιτήματα που δεν προλαβαίνετε να απαντήσετε — έτσι χάνετε κρατήσεις που ποτέ δεν μάθατε ότι υπήρχαν.",
      "problem.c3.title": "Κάθε αργή απάντηση κοστίζει πραγματικά χρήματα",
      "problem.c3.body": "Ένα χαμένο αίτημα δεν είναι μικρή ταλαιπωρία — είναι πραγματικά έσοδα που πάνε σε έναν πιο γρήγορο ανταγωνιστή. Πολλαπλασιάστε το σε έναν μήνα και το κόστος του να μην αυτοματοποιείτε γίνεται προφανές.",

      "how.eyebrow": "Πώς λειτουργεί",
      "how.title": "Τρία βήματα. <em>Καμία χαμένη ερώτηση.</em>",
      "how.lede": "Καμία νέα εφαρμογή για τους πελάτες σας. Καμία νέα πλατφόρμα να μάθετε. Συνδέεται απευθείας στο WhatsApp και λειτουργεί στο παρασκήνιο.",
      "how.s1.num": "01 · Ερώτηση",
      "how.s1.title": "Φτάνει στο WhatsApp",
      "how.s1.body": "Ένας πελάτης στέλνει μήνυμα στον αριθμό σας στο WhatsApp ρωτώντας για διαθεσιμότητα, τιμή ή πώς να κλείσει. Ακριβώς όπως κάνουν σήμερα — τίποτα δεν αλλάζει για εκείνους.",
      "how.s2.num": "02 · Απάντηση",
      "how.s2.title": "Άμεση απάντηση στη γλώσσα τους",
      "how.s2.body": "Ο βοηθός σας απαντά μέσα σε δευτερόλεπτα — στα Αγγλικά, Ρωσικά, Εβραϊκά, Πολωνικά, Γερμανικά ή Ελληνικά, με αυτόματη αναγνώριση. Απαντά σε ερωτήσεις διαθεσιμότητας, τιμής και πολιτικής βάσει των οδηγιών σας.",
      "how.s3.num": "03 · Καταγραφή",
      "how.s3.title": "Η κράτηση καταγράφεται, ειδοποιείστε",
      "how.s3.body": "Ημερομηνία, ώρα, αριθμός ατόμων και δραστηριότητα καταγράφονται αυτόματα. Το ημερολόγιό σας ενημερώνεται μόνο του. Ειδοποιείστε μόνο όταν κάτι χρειάζεται προσωπική προσοχή — ό,τι ξεφεύγει από το σενάριο έρχεται κατευθείαν σε εσάς.",

      "feat.eyebrow": "Τι αποκτάτε",
      "feat.title": "Φτιαγμένο για πολυάσχολους επαγγελματίες.",
      "feat.lede": "Όχι ένα γενικό chatbot. Εκπαιδευμένο στην επιχείρησή σας, στις τιμές σας, στις πολιτικές σας — και διαθέσιμο όλο το 24ωρο ώστε να μην χρειάζεται να είστε εσείς.",
      "feat.f1.tag": "Πάντα ενεργό",
      "feat.f1.title": "Άμεσες απαντήσεις, 24/7",
      "feat.f1.body": "Κάθε αίτημα απαντάται μέσα σε δευτερόλεπτα — 2 το πρωί ή 2 το μεσημέρι, Κυριακή ή αργία τον Αύγουστο. Τέλος τα μηνύματα «συγγνώμη για την καθυστέρηση». Τέλος οι κρατήσεις που χάνονται όσο κοιμάστε.",
      "feat.f2.tag": "Πολύγλωσσο",
      "feat.f2.title": "Μιλά τη γλώσσα των πελατών σας",
      "feat.f2.body": "Αγγλικά, Ρωσικά, Εβραϊκά, Πολωνικά, Γερμανικά και Ελληνικά — με αυτόματη αναγνώριση από το πρώτο μήνυμα. Καμία ρύθμιση ανά γλώσσα. Ο βοηθός σας διαχειρίζεται τη συνομιλία φυσικά, ανεξάρτητα από το πού έρχεται ο τουρίστας.",
      "feat.f3.tag": "Καταγραφή κρατήσεων",
      "feat.f3.title": "Στοιχεία καταγραμμένα, ημερολόγιο ενημερωμένο",
      "feat.f3.body": "Ημερομηνία, ώρα, αριθμός ατόμων και δραστηριότητα καταγράφονται από τη συνομιλία και περνούν στο ημερολόγιό σας. Σύνοψη κράτησης σας αποστέλλεται μόλις επιβεβαιωθεί μια θέση — χωρίς χειροκίνητη καταχώριση.",
      "feat.f4.tag": "Ο ιδιοκτήτης έχει τον έλεγχο",
      "feat.f4.title": "Ειδοποίηση για οτιδήποτε ασυνήθιστο",
      "feat.f4.body": "Γκρουπ των 20; Ασυνήθιστο αίτημα; Παράπονο; Ό,τι ξεφεύγει από το εκπαιδευμένο σενάριο επισημαίνεται αμέσως και έρχεται σε εσάς. Διατηρείτε τον έλεγχο σε κάθε ιδιαίτερη περίπτωση χωρίς να παρακολουθείτε τη συνομιλία όλο το 24ωρο.",
      "feat.f4.secondary": "Διαχειρίζεται και μηνύματα Instagram",

      "price.eyebrow": "Τιμές",
      "price.title": "Απλή τιμολόγηση. <em>Καμία έκπληξη.</em>",
      "price.lede": "Ένα κόστος ρύθμισης, μία μηνιαία χρέωση. Ακυρώστε όποτε θέλετε. Ο βοηθός σας είναι ενεργός εντός 48 ωρών από την εγγραφή.",
      "price.cardEyebrow": "Πλήρης υπηρεσία · όλα περιλαμβάνονται",
      "price.setup": "εφάπαξ ρύθμιση",
      "price.month": "τον μήνα",
      "price.terms": "Ακύρωση όποτε θέλετε · Χωρίς δέσμευση · Ενεργό σε 48 ώρες",
      "price.f1": "Πλήρης ρύθμιση & εκπαίδευση βοηθού",
      "price.f2": "Πολύγλωσσο (6 γλώσσες)",
      "price.f3": "Αυτόματη καταγραφή κρατήσεων",
      "price.f4": "Σύνδεση με ημερολόγιο",
      "price.f5": "Ειδοποιήσεις ιδιοκτήτη",
      "price.f6": "Συνεχής υποστήριξη & ενημερώσεις",
      "price.f7": "Ενσωμάτωση WhatsApp Business",
      "price.f8": "Ενεργοποίηση σε 48 ώρες",
      "price.footnote": "Καμία δέσμευση σε αυτό το στάδιο — πείτε μας για την επιχείρησή σας και θα επικοινωνήσουμε εντός 24 ωρών.",

      "contact.eyebrow": "Ξεκινήστε",
      "contact.title": "Έτοιμοι να σταματήσετε να χάνετε κρατήσεις;",
      "contact.lede": "Πείτε μας για την επιχείρησή σας. Θα επικοινωνήσουμε εντός 24 ωρών για να σας ρυθμίσουμε — καμία δέσμευση, καμία κλήση πωλήσεων.",
      "form.name": "Το όνομά σας",
      "form.business": "Όνομα επιχείρησης",
      "form.whatsapp": "Αριθμός WhatsApp",
      "form.type": "Τι επιχείρηση έχετε;",
      "form.typePlaceholder": "Επιλέξτε τον τύπο της επιχείρησής σας",
      "form.type.salon": "Κομμωτήριο / spa / κλινική",
      "form.type.restaurant": "Εστιατόριο / καφέ",
      "form.type.tourism": "Ενοικίαση σκαφών / θαλάσσια σπορ / εκδρομές",
      "form.type.car": "Ενοικίαση αυτοκινήτων",
      "form.type.other": "Άλλο",
      "form.notes": "Κάτι άλλο;",
      "form.optional": "(προαιρετικό)",
      "form.notesPlaceholder": "Πόσα αιτήματα λαμβάνετε την ημέρα; Συγκεκριμένες γλώσσες; Οτιδήποτε θα μας βοηθούσε να προετοιμαστούμε…",
      "form.submit": "Στείλτε τα στοιχεία μου",
      "form.footnote": "Καμία δέσμευση. Θα απαντήσουμε εντός 24 ωρών. <a href=\"/privacy.html\">Πολιτική απορρήτου</a>.",

      "faq.eyebrow": "Συχνές ερωτήσεις",
      "faq.title": "Συχνές ερωτήσεις, <em>ειλικρινείς απαντήσεις.</em>",
      "faq.q1": "Χρειάζεται ο πελάτης μου να κατεβάσει κάτι;",
      "faq.a1": "Όχι. Οι πελάτες σας στέλνουν μήνυμα στον υπάρχοντα αριθμό σας στο WhatsApp ακριβώς όπως κάνουν σήμερα. Τίποτα δεν αλλάζει για εκείνους — δεν χρειάζονται νέα εφαρμογή, λογαριασμό ή σύνδεσμο. Ο βοηθός απλώς σας κάνει να απαντάτε πιο γρήγορα.",
      "faq.q2": "Πόσο χρόνο παίρνει η ρύθμιση;",
      "faq.a2": "48 ώρες από τη στιγμή που έχουμε τα στοιχεία σας. Εκπαιδεύουμε τον βοηθό στην επιχείρησή σας — υπηρεσίες, τιμές, διαθεσιμότητα, πολιτικές — και τον συνδέουμε με τον αριθμό σας στο WhatsApp Business. Τον ελέγχετε και τον εγκρίνετε πριν ενεργοποιηθεί.",
      "faq.q3": "Ποιες γλώσσες υποστηρίζει;",
      "faq.a3": "Αγγλικά, Ρωσικά, Εβραϊκά, Πολωνικά, Γερμανικά και Ελληνικά — με αυτόματη αναγνώριση από το μήνυμα του πελάτη. Αν ένας τουρίστας γράψει στα Ρωσικά, ο βοηθός απαντά στα Ρωσικά. Δεν ρυθμίζετε τίποτα ανά συνομιλία.",
      "faq.q4": "Τι γίνεται αν λάβει μια ερώτηση που δεν μπορεί να απαντήσει;",
      "faq.a4": "Ό,τι ξεφεύγει από το εκπαιδευμένο σενάριο επισημαίνεται σε εσάς αμέσως. Λαμβάνετε ειδοποίηση με τη συνομιλία ώστε να παρέμβετε με προσωπική απάντηση. Ο πελάτης ενημερώνεται ότι κάποιος θα επικοινωνήσει σύντομα — κανένα αδιέξοδο.",
      "faq.q5": "Μπορώ να απαντώ και ο ίδιος στους πελάτες;",
      "faq.a5": "Ναι. Μπορείτε να αναλάβετε οποιαδήποτε συνομιλία ανά πάσα στιγμή. Ο βοηθός χειρίζεται την πρώτη απάντηση και τις συνηθισμένες ερωτήσεις — εσείς έχετε τον έλεγχο σε ό,τι θέλετε να χειριστείτε προσωπικά.",
      "faq.q6": "Τι καλύπτει η ρύθμιση των €400;",
      "faq.a6": "Τα πάντα: δημιουργία και εκπαίδευση του βοηθού στη συγκεκριμένη επιχείρησή σας, σύνδεση με τον λογαριασμό σας στο WhatsApp Business, σύνδεση ημερολογίου, δοκιμές και μια κλήση ελέγχου πριν την ενεργοποίηση. Δεν υπάρχουν κρυφές χρεώσεις — η ρύθμιση είναι εφάπαξ κόστος.",
      "faq.q7": "Μπορώ να ακυρώσω;",
      "faq.a7": "Ναι, όποτε θέλετε. Μηνιαία βάση, χωρίς συμβόλαια, χωρίς χρεώσεις ακύρωσης. Αν ακυρώσετε, ο βοηθός απενεργοποιείται και το WhatsApp σας επανέρχεται στο κανονικό. Φυσικά θα προτιμούσαμε να μείνετε — αλλά δεν υπάρχει δέσμευση.",
      "faq.q8": "Λειτουργεί για τον τύπο της δικής μου επιχείρησης;",
      "faq.a8": "Αν δέχεστε κρατήσεις ή επαναλαμβανόμενες ερωτήσεις πελατών μέσω WhatsApp — κομμωτήρια, κλινικές, ενοικιάσεις, εκδρομές, εστιατόρια ή παρόμοιες επιχειρήσεις υπηρεσιών — ναι. Αν δεν είστε σίγουροι, στείλτε μας μήνυμα και θα σας πούμε ειλικρινά αν ταιριάζει.",
      "faq.q9": "Είναι ασφαλή τα δεδομένα των πελατών μου;",
      "faq.a9": "Ναι. Οι συνομιλίες παραμένουν στην κρυπτογραφημένη πλατφόρμα του WhatsApp και τις χρησιμοποιούμε μόνο για τη λειτουργία του βοηθού σας — ποτέ για πώληση ή κοινοποίηση. Τα δεδομένα σας ανήκουν σε εσάς και διαγράφονται αν ακυρώσετε. Αναλυτικά στην πολιτική απορρήτου μας.",

      "final.title": "Σταματήστε να χάνετε κρατήσεις. <em>Ξεκινήστε σήμερα.</em>",
      "final.lede": "Χρειάζονται 2 λεπτά για να συμπληρώσετε τη φόρμα. Θα επικοινωνήσουμε εντός 24 ωρών και ο βοηθός σας μπορεί να είναι ενεργός σε 48.",

      "trust.eyebrow": "Γιατί OwnerDeck",
      "trust.title": "Ρύθμιση και υποστήριξη από <em>έναν πραγματικό άνθρωπο.</em>",
      "trust.quote": "“Ρυθμίζω και υποστηρίζω κάθε βοηθό ο ίδιος. Αν δεν ταιριάζει στην επιχείρησή σας, θα σας το πω ειλικρινά — χωρίς πίεση.”",
      "trust.role": "Ιδρυτής · Λάρνακα, Κύπρος",

      "footer.tagline": "Βοηθός κρατήσεων WhatsApp με τεχνητή νοημοσύνη για επιχειρήσεις στην Κύπρο.",
      "footer.product": "Προϊόν",
      "footer.company": "Εταιρεία",
      "footer.getInTouch": "Επικοινωνία",
      "footer.privacy": "Πολιτική απορρήτου",
      "footer.copyright": "© 2026 OwnerDeck. Φτιαγμένο στην Κύπρο.",
      "footer.location": "Λάρνακα, Κύπρος"
    },

    /* ---------------------------------------------------------- RU */
    ru: {
      "meta.title": "OwnerDeck — Не теряйте брони из-за медленного ответа",
      "cta.getStarted": "Начать",
      "cta.seeHow": "Как это работает",

      "nav.how": "Как это работает",
      "nav.features": "Возможности",
      "nav.pricing": "Цены",
      "nav.faq": "Вопросы",

      "hero.eyebrow": "Уже работает на Кипре",
      "hero.title": "Не теряйте брони из-за <em>медленного ответа.</em>",
      "hero.lede": "Ваш ассистент в WhatsApp отвечает на каждый запрос клиента за секунды — круглосуточно, на его языке. Пока вы заняты с клиентом, в дороге или отдыхаете.",
      "hero.builtFor": "Для салонов · клиник · аренды · экскурсий · любого бизнеса, который принимает брони через WhatsApp",
      "hero.trust": "Уже обрабатываем реальные брони на Кипре — среднее время ответа менее 5 секунд",

      "chat.online": "В сети",
      "chat.speed": "Ответ за 4 секунды",

      "problem.eyebrow": "Проблема",
      "problem.title": "Клиенты не ждут. <em>Они уходят к другим.</em>",
      "problem.lede": "Когда человек хочет забронировать, он пишет сразу двум-трём компаниям и выбирает того, кто ответит первым. Скорость — это не приятный бонус, это всё.",
      "problem.c1.title": "Они пишут всем сразу",
      "problem.c1.body": "Клиенты открывают WhatsApp, отправляют один и тот же вопрос двум-трём компаниям и бронируют у того, кто ответит быстрее. Вы конкурируете не ценой — вы конкурируете скоростью.",
      "problem.c2.title": "В часы пик у вас нет ни минуты",
      "problem.c2.body": "Вы посреди приёма, обслуживаете клиента или просто пытаетесь пообедать. Телефон наполняется запросами, на которые вы не успеваете ответить — и вы теряете брони, о которых даже не узнали.",
      "problem.c3.title": "Каждый медленный ответ стоит реальных денег",
      "problem.c3.body": "Упущенный запрос — это не мелкое неудобство, а реальная выручка, ушедшая к более быстрому конкуренту. Умножьте это на месяц, и цена отказа от автоматизации станет очевидной.",

      "how.eyebrow": "Как это работает",
      "how.title": "Три шага. <em>Ни одного упущенного запроса.</em>",
      "how.lede": "Никаких новых приложений для ваших клиентов. Никаких новых платформ для изучения. Подключается прямо к WhatsApp и работает в фоне.",
      "how.s1.num": "01 · Запрос",
      "how.s1.title": "Приходит в WhatsApp",
      "how.s1.body": "Клиент пишет на ваш номер WhatsApp с вопросом о наличии, цене или о том, как забронировать. Точно так же, как и сегодня — для него ничего не меняется.",
      "how.s2.num": "02 · Ответ",
      "how.s2.title": "Мгновенный ответ на их языке",
      "how.s2.body": "Ваш ассистент отвечает за секунды — на английском, русском, иврите, польском, немецком или греческом, определяя язык автоматически. Отвечает на вопросы о наличии, цене и правилах по вашим инструкциям.",
      "how.s3.num": "03 · Фиксация",
      "how.s3.title": "Бронь зафиксирована, вы уведомлены",
      "how.s3.body": "Дата, время, число гостей и активность фиксируются автоматически. Ваш календарь обновляется сам. Вас уведомляют только тогда, когда нужно личное участие — всё, что выходит за рамки сценария, приходит напрямую к вам.",

      "feat.eyebrow": "Что вы получаете",
      "feat.title": "Создано для занятых владельцев бизнеса.",
      "feat.lede": "Не обычный чат-бот. Обучен на вашем бизнесе, ваших ценах, ваших правилах — и доступен круглосуточно, чтобы вам не приходилось.",
      "feat.f1.tag": "Всегда на связи",
      "feat.f1.title": "Мгновенные ответы, 24/7",
      "feat.f1.body": "На каждый запрос ответ за секунды — в 2 ночи или в 2 дня, в воскресенье или в праздник. Больше никаких «извините за поздний ответ». Больше никаких броней, упущенных, пока вы спите.",
      "feat.f2.tag": "Многоязычный",
      "feat.f2.title": "Говорит на языке ваших клиентов",
      "feat.f2.body": "Английский, русский, иврит, польский, немецкий и греческий — определяются автоматически с первого сообщения. Никаких настроек для каждого языка. Ассистент ведёт диалог естественно, откуда бы ни был турист.",
      "feat.f3.tag": "Фиксация броней",
      "feat.f3.title": "Данные записаны, календарь обновлён",
      "feat.f3.body": "Дата, время, число гостей и активность извлекаются из диалога и заносятся в ваш календарь. Сводка по брони приходит вам, как только место подтверждено — без ручного ввода.",
      "feat.f4.tag": "Владелец под контролем",
      "feat.f4.title": "Уведомление обо всём необычном",
      "feat.f4.body": "Группа из 20 человек? Необычный запрос? Жалоба? Всё, что выходит за рамки обученного сценария, сразу отмечается и передаётся вам. Вы контролируете каждый особый случай, не следя за чатом круглосуточно.",
      "feat.f4.secondary": "Также обрабатывает сообщения в Instagram",

      "price.eyebrow": "Цены",
      "price.title": "Простые цены. <em>Без сюрпризов.</em>",
      "price.lede": "Одна плата за настройку, один ежемесячный тариф. Отмена в любой момент. Ваш ассистент работает в течение 48 часов после регистрации.",
      "price.cardEyebrow": "Полный сервис · всё включено",
      "price.setup": "разовая настройка",
      "price.month": "в месяц",
      "price.terms": "Отмена в любой момент · Без обязательств · Запуск за 48 часов",
      "price.f1": "Полная настройка и обучение ассистента",
      "price.f2": "Многоязычность (6 языков)",
      "price.f3": "Автоматическая фиксация броней",
      "price.f4": "Интеграция с календарём",
      "price.f5": "Уведомления владельцу",
      "price.f6": "Постоянная поддержка и обновления",
      "price.f7": "Интеграция с WhatsApp Business",
      "price.f8": "Запуск за 48 часов",
      "price.footnote": "Никаких обязательств на этом этапе — расскажите о своём бизнесе, и мы свяжемся с вами в течение 24 часов.",

      "contact.eyebrow": "Начать",
      "contact.title": "Готовы перестать упускать брони?",
      "contact.lede": "Расскажите о своём бизнесе. Мы свяжемся в течение 24 часов, чтобы всё настроить — без обязательств и без звонков от продавцов.",
      "form.name": "Ваше имя",
      "form.business": "Название бизнеса",
      "form.whatsapp": "Номер WhatsApp",
      "form.type": "Чем вы занимаетесь?",
      "form.typePlaceholder": "Выберите тип вашего бизнеса",
      "form.type.salon": "Салон / спа / клиника",
      "form.type.restaurant": "Ресторан / кафе",
      "form.type.tourism": "Аренда лодок / водный спорт / экскурсии",
      "form.type.car": "Аренда авто",
      "form.type.other": "Другое",
      "form.notes": "Что-нибудь ещё?",
      "form.optional": "(необязательно)",
      "form.notesPlaceholder": "Сколько запросов вы получаете в день? Какие-то конкретные языки? Всё, что поможет нам подготовиться…",
      "form.submit": "Отправить мои данные",
      "form.footnote": "Без обязательств. Мы ответим в течение 24 часов. <a href=\"/privacy.html\">Политика конфиденциальности</a>.",

      "faq.eyebrow": "Вопросы",
      "faq.title": "Частые вопросы, <em>честные ответы.</em>",
      "faq.q1": "Нужно ли моему клиенту что-то скачивать?",
      "faq.a1": "Нет. Ваши клиенты пишут на ваш существующий номер WhatsApp точно так же, как и сегодня. Для них ничего не меняется — не нужно новое приложение, аккаунт или ссылка. Ассистент просто помогает вам отвечать быстрее.",
      "faq.q2": "Сколько занимает настройка?",
      "faq.a2": "48 часов с момента получения ваших данных. Мы обучаем ассистента на вашем бизнесе — услуги, цены, наличие, правила — и подключаем его к вашему номеру WhatsApp Business. Вы проверяете и одобряете перед запуском.",
      "faq.q3": "Какие языки поддерживаются?",
      "faq.a3": "Английский, русский, иврит, польский, немецкий и греческий — определяются автоматически по сообщению клиента. Если турист пишет по-русски, ассистент отвечает по-русски. Вам не нужно ничего настраивать для каждого диалога.",
      "faq.q4": "Что если будет вопрос, на который он не сможет ответить?",
      "faq.a4": "Всё, что выходит за рамки обученного сценария, сразу отмечается для вас. Вы получите уведомление с диалогом, чтобы вмешаться с личным ответом. Клиенту сообщают, что с ним скоро свяжутся — никаких тупиков.",
      "faq.q5": "Могу ли я отвечать клиентам сам?",
      "faq.a5": "Да. Вы можете взять любой диалог на себя в любой момент. Ассистент берёт на себя первый ответ и рутинные вопросы — вы остаётесь главным во всём, что хотите вести лично.",
      "faq.q6": "Что входит в настройку за €400?",
      "faq.a6": "Всё: создание и обучение ассистента под ваш конкретный бизнес, подключение к вашему аккаунту WhatsApp Business, интеграция с календарём, тестирование и проверочный звонок перед запуском. Скрытых платежей нет — настройка оплачивается один раз.",
      "faq.q7": "Можно ли отменить?",
      "faq.a7": "Да, в любой момент. Помесячно, без договоров, без штрафов за отмену. Если вы отмените, ассистент отключается, и ваш WhatsApp возвращается к обычному режиму. Конечно, мы предпочли бы, чтобы вы остались — но никаких обязательств нет.",
      "faq.q8": "Подходит ли это для моего типа бизнеса?",
      "faq.a8": "Если вы принимаете брони или повторяющиеся вопросы клиентов через WhatsApp — салоны, клиники, аренда, экскурсии, рестораны или похожий сервисный бизнес — да. Если не уверены, напишите нам, и мы честно скажем, подойдёт ли это вам.",
      "faq.q9": "Данные моих клиентов в безопасности?",
      "faq.a9": "Да. Переписка остаётся в зашифрованной среде самого WhatsApp, и мы используем её только для работы вашего ассистента — никогда для продажи или передачи. Ваши данные принадлежат вам и удаляются при отмене. Подробности — в нашей политике конфиденциальности.",

      "final.title": "Перестаньте терять брони. <em>Начните сегодня.</em>",
      "final.lede": "Заполнить форму — 2 минуты. Мы свяжемся в течение 24 часов, и ваш ассистент может заработать за 48.",

      "trust.eyebrow": "Почему OwnerDeck",
      "trust.title": "Настройка и поддержка — <em>от живого человека.</em>",
      "trust.quote": "“Я лично настраиваю и поддерживаю каждого ассистента. Если он не подойдёт вашему бизнесу — скажу честно, без навязывания.”",
      "trust.role": "Основатель · Ларнака, Кипр",

      "footer.tagline": "ИИ-ассистент бронирования в WhatsApp для бизнеса на Кипре.",
      "footer.product": "Продукт",
      "footer.company": "Компания",
      "footer.getInTouch": "Связаться",
      "footer.privacy": "Политика конфиденциальности",
      "footer.copyright": "© 2026 OwnerDeck. Сделано на Кипре.",
      "footer.location": "Ларнака, Кипр"
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

  // expose for debugging
  window.OD_I18N = { apply: apply, supported: SUPPORTED };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
