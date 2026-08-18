# Regenerates the language packs from _en_source.json.
#
# The English string is the key here, not the hash, because a human has to be
# able to read and correct this file. The hashing happens below, against the
# same normalisation _build_site.py uses, so the two cannot drift.
#
# Greek and Russian are complete. The other four packs are left alone by this
# script — rewriting them from an incomplete table would delete translations
# that are still good.
#
# el/ru are machine-assisted and should be read by a native speaker before
# being leaned on commercially.
#
# Run:  python _translate.py
import hashlib
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ['el', 'ru']

ENT = {'&rsquo;': '’', '&lsquo;': '‘', '&euro;': '€',
       '&middot;': '·', '&mdash;': '—', '&ndash;': '–',
       '&amp;': '&', '&quot;': '"'}


def decode(s):
    for a, b in ENT.items():
        s = s.replace(a, b)
    return s


# English -> (Greek, Russian)
T = {
    # ---- chrome, navigation, buttons ----
    'Skip to content': ('Μετάβαση στο περιεχόμενο', 'Перейти к содержимому'),
    'What we build': ('Τι φτιάχνουμε', 'Что мы создаём'),
    'How it works': ('Πώς λειτουργεί', 'Как это работает'),
    'Pricing': ('Τιμές', 'Цены'),
    "Who it's for": ('Για ποιους είναι', 'Для кого это'),
    'Questions': ('Ερωτήσεις', 'Вопросы'),
    'Terms': ('Όροι', 'Условия'),
    'Privacy': ('Απόρρητο', 'Конфиденциальность'),
    'Cookies': ('Cookies', 'Cookies'),
    'Legal notice': ('Νομικές πληροφορίες', 'Правовая информация'),
    'Talk to us': ('Μιλήστε μας', 'Свяжитесь с нами'),
    'Message us on WhatsApp': ('Στείλτε μας στο WhatsApp', 'Напишите нам в WhatsApp'),
    'See pricing': ('Δείτε τις τιμές', 'Посмотреть цены'),
    'See how it works': ('Δείτε πώς λειτουργεί', 'Посмотреть, как это работает'),
    'Previous': ('Προηγούμενο', 'Назад'),
    'Next': ('Επόμενο', 'Вперёд'),
    'Contact': ('Επικοινωνία', 'Контакты'),
    'Reading': ('Διαβάστε', 'Читать'),
    'The cards': ('Οι κάρτες', 'Карты'),
    'Legal': ('Νομικά', 'Правовое'),
    'WhatsApp': ('WhatsApp', 'WhatsApp'),
    'Built and run by Ownerdeck.': ('Φτιάχτηκε και συντηρείται από το Ownerdeck.',
                                    'Создано и обслуживается Ownerdeck.'),
    'We build and run the online side of small owner-operated businesses. One set of facts drives the website, the messages, the bookings and the follow-up.':
        ('Φτιάχνουμε και τρέχουμε την ψηφιακή πλευρά μικρών επιχειρήσεων. Ένα σύνολο δεδομένων τροφοδοτεί την ιστοσελίδα, τα μηνύματα, τις κρατήσεις και την επικοινωνία μετά.',
         'Мы создаём и обслуживаем онлайн-часть небольших бизнесов. Один набор данных управляет сайтом, сообщениями, бронированиями и последующей связью.'),

    # ---- the cards ----
    'Answer': ('Answer', 'Answer'),
    'Site': ('Site', 'Site'),
    'Data': ('Data', 'Data'),
    'Book': ('Book', 'Book'),
    'Reach': ('Reach', 'Reach'),
    'Return': ('Return', 'Return'),
    'Deck': ('Deck', 'Deck'),
    'Full Deck': ('Full Deck', 'Full Deck'),
    'The deck': ('Η τράπουλα', 'Колода'),
    'Five cards. One system.': ('Πέντε κάρτες. Ένα σύστημα.', 'Пять карт. Одна система.'),
    'Enquiries handled on WhatsApp, Instagram DMs and website chat. Any language, any hour.':
        ('Απαντάμε σε ερωτήματα στο WhatsApp, στα Instagram DMs και στο chat της ιστοσελίδας. Σε κάθε γλώσσα, κάθε ώρα.',
         'Обработка запросов в WhatsApp, Instagram DM и чате сайта. На любом языке, в любое время.'),
    'A fast website that reads live from your prices, so it never goes stale.':
        ('Μια γρήγορη ιστοσελίδα που διαβάζει ζωντανά τις τιμές σας, ώστε να μην παλιώνει ποτέ.',
         'Быстрый сайт, который читает ваши цены напрямую, поэтому он никогда не устаревает.'),
    'Real availability, confirmations, deposits and a calendar that fills itself in.':
        ('Πραγματική διαθεσιμότητα, επιβεβαιώσεις, προκαταβολές και ένα ημερολόγιο που συμπληρώνεται μόνο του.',
         'Реальная доступность, подтверждения, депозиты и календарь, который заполняется сам.'),
    'Your Google listing set up properly, and a review request after every booking.':
        ('Η καταχώρισή σας στο Google σωστά ρυθμισμένη και αίτημα αξιολόγησης μετά από κάθε κράτηση.',
         'Ваш профиль в Google, настроенный правильно, и запрос отзыва после каждого бронирования.'),
    'Reminders, off-season offers, and past customers who come back.':
        ('Υπενθυμίσεις, προσφορές εκτός σεζόν και παλιοί πελάτες που επιστρέφουν.',
         'Напоминания, предложения вне сезона и возвращающиеся клиенты.'),
    'Who it is for': ('Για ποιους είναι', 'Для кого это'),
    'Owners who lose bookings to slow replies.':
        ('Ιδιοκτήτες που χάνουν κρατήσεις από αργές απαντήσεις.',
         'Владельцев, теряющих брони из-за медленных ответов.'),
    'Anyone whose website has not been touched in years.':
        ('Όποιον δεν έχει αγγίξει την ιστοσελίδα του εδώ και χρόνια.',
         'Всех, чей сайт не обновлялся годами.'),
    'Businesses still taking bookings by phone and paper.':
        ('Επιχειρήσεις που κρατούν ακόμη ραντεβού με τηλέφωνο και χαρτί.',
         'Бизнесов, которые всё ещё принимают брони по телефону и на бумаге.'),
    'Owners who are hard to find and rarely reviewed.':
        ('Ιδιοκτήτες που δύσκολα βρίσκονται και σπάνια αξιολογούνται.',
         'Владельцев, которых трудно найти и редко оценивают.'),
    'Seasonal businesses with quiet months to fill.':
        ('Εποχικές επιχειρήσεις με ήσυχους μήνες προς κάλυψη.',
         'Сезонных бизнесов с тихими месяцами.'),
    'Underneath all of it': ('Κάτω από όλα αυτά', 'В основе всего'),
    'Why it matters': ('Γιατί έχει σημασία', 'Почему это важно'),
    'The database every card reads from. Your services, prices, seasons, availability, hours and policies, in one place with an admin screen you can actually use.':
        ('Η βάση δεδομένων από την οποία διαβάζει κάθε κάρτα. Οι υπηρεσίες, οι τιμές, οι σεζόν, η διαθεσιμότητα, οι ώρες και οι πολιτικές σας, σε ένα σημείο με μια οθόνη διαχείρισης που μπορείτε πραγματικά να χρησιμοποιήσετε.',
         'База данных, из которой читает каждая карта. Ваши услуги, цены, сезоны, доступность, часы работы и правила — в одном месте, с админ-панелью, которой действительно можно пользоваться.'),
    'Without it, a price change means editing the website, correcting the assistant and remembering what you told Google. With it, you change one number.':
        ('Χωρίς αυτήν, μια αλλαγή τιμής σημαίνει επεξεργασία της ιστοσελίδας, διόρθωση του βοηθού και να θυμάστε τι είπατε στο Google. Με αυτήν, αλλάζετε έναν αριθμό.',
         'Без неё изменение цены означает правку сайта, исправление ассистента и попытку вспомнить, что вы указали в Google. С ней вы меняете одно число.'),
    'Start with the card you need and add the rest as you grow. Each one reads from the same set of facts.':
        ('Ξεκινήστε με την κάρτα που χρειάζεστε και προσθέστε τις υπόλοιπες καθώς μεγαλώνετε. Καθεμία διαβάζει από τα ίδια δεδομένα.',
         'Начните с нужной карты и добавляйте остальные по мере роста. Каждая читает из одного набора данных.'),
    'Start with the card you need and add the rest as you grow. Every card reads from the same set of facts, so nothing you own can contradict anything else you own.':
        ('Ξεκινήστε με την κάρτα που χρειάζεστε και προσθέστε τις υπόλοιπες καθώς μεγαλώνετε. Κάθε κάρτα διαβάζει από τα ίδια δεδομένα, ώστε τίποτα δικό σας να μην έρχεται σε αντίφαση με κάτι άλλο δικό σας.',
         'Начните с нужной карты и добавляйте остальные по мере роста. Каждая карта читает из одного набора данных, поэтому ничто из вашего не может противоречить другому.'),
    'What each card does': ('Τι κάνει κάθε κάρτα', 'Что делает каждая карта'),

    # ---- hero, reality, one idea ----
    'Run the online side of your business.':
        ('Τρέξτε την ψηφιακή πλευρά της επιχείρησής σας.',
         'Управляйте онлайн-частью вашего бизнеса.'),
    'Ownerdeck runs the online side of your business — your website, your enquiries, your bookings and the follow-up after. Set your prices once and everything says the same thing.':
        ('Το Ownerdeck τρέχει την ψηφιακή πλευρά της επιχείρησής σας — την ιστοσελίδα, τα ερωτήματα, τις κρατήσεις και την επικοινωνία μετά. Ορίστε τις τιμές σας μία φορά και όλα λένε το ίδιο πράγμα.',
         'Ownerdeck управляет онлайн-частью вашего бизнеса — сайтом, запросами, бронированиями и последующей связью. Задайте цены один раз, и везде будет одно и то же.'),
    'No VAT. No long contract on the entry plan.':
        ('Χωρίς ΦΠΑ. Χωρίς μακροχρόνιο συμβόλαιο στο εισαγωγικό πακέτο.',
         'Без НДС. Без долгосрочного договора на начальном тарифе.'),
    'The reality': ('Η πραγματικότητα', 'Реальность'),
    'The online side runs whether you are watching or not.':
        ('Η ψηφιακή πλευρά τρέχει είτε την παρακολουθείτε είτε όχι.',
         'Онлайн-часть работает, смотрите вы за ней или нет.'),
    'Enquiries arrive at 11pm and wait until morning.':
        ('Τα ερωτήματα φτάνουν στις 11 το βράδυ και περιμένουν ως το πρωί.',
         'Запросы приходят в 11 вечера и ждут до утра.'),
    'Prices are out of date in three different places.':
        ('Οι τιμές είναι ξεπερασμένες σε τρία διαφορετικά σημεία.',
         'Цены устарели сразу в трёх местах.'),
    'Customers move on while they wait for a reply.':
        ('Οι πελάτες φεύγουν όσο περιμένουν απάντηση.',
         'Клиенты уходят, пока ждут ответа.'),
    'The website has not been touched since it was built.':
        ('Η ιστοσελίδα δεν έχει αγγιχτεί από τότε που φτιάχτηκε.',
         'Сайт не трогали с момента создания.'),
    'The one idea': ('Η μία ιδέα', 'Одна идея'),
    'Tell it once. It runs everything.':
        ('Πείτε το μία φορά. Τα τρέχει όλα.', 'Скажите один раз. Оно управляет всем.'),
    'You give Ownerdeck the facts about your business one time. That single set of facts becomes everything your customers see. Change a price in one place and everything says the same thing.':
        ('Δίνετε στο Ownerdeck τα δεδομένα της επιχείρησής σας μία φορά. Αυτό το σύνολο δεδομένων γίνεται ό,τι βλέπουν οι πελάτες σας. Αλλάξτε μια τιμή σε ένα σημείο και όλα λένε το ίδιο.',
         'Вы один раз передаёте Ownerdeck данные о вашем бизнесе. Этот набор данных становится всем, что видят клиенты. Измените цену в одном месте — и везде будет одно и то же.'),
    'How it fits together': ('Πώς δένουν όλα μαζί', 'Как всё связано'),
    'What you tell us once': ('Τι μας λέτε μία φορά', 'Что вы говорите один раз'),
    'What it runs': ('Τι τρέχει', 'Чем оно управляет'),
    'What reads from it': ('Τι διαβάζει από αυτό', 'Что из этого читает'),
    'Services': ('Υπηρεσίες', 'Услуги'),
    'Prices': ('Τιμές', 'Цены'),
    'Availability': ('Διαθεσιμότητα', 'Доступность'),
    'Hours': ('Ωράριο', 'Часы работы'),
    'Policies': ('Πολιτικές', 'Правила'),
    'Photos': ('Φωτογραφίες', 'Фотографии'),
    'Seasons': ('Σεζόν', 'Сезоны'),
    'Website': ('Ιστοσελίδα', 'Сайт'),
    'Messages': ('Μηνύματα', 'Сообщения'),
    'Bookings': ('Κρατήσεις', 'Бронирования'),
    'Google': ('Google', 'Google'),
    'Follow-up': ('Επικοινωνία μετά', 'Последующая связь'),
    'Your website': ('Η ιστοσελίδα σας', 'Ваш сайт'),
    'WhatsApp replies': ('Απαντήσεις WhatsApp', 'Ответы в WhatsApp'),
    'Instagram DMs': ('Instagram DMs', 'Instagram DM'),
    'Website chat': ('Chat ιστοσελίδας', 'Чат на сайте'),
    'Booking confirmations': ('Επιβεβαιώσεις κρατήσεων', 'Подтверждения броней'),
    'Google listing': ('Καταχώριση Google', 'Профиль в Google'),
    'Follow-up messages': ('Μηνύματα επικοινωνίας', 'Последующие сообщения'),
    'The wiring': ('Η καλωδίωση', 'Как это соединено'),
    'One set of facts, five outputs.':
        ('Ένα σύνολο δεδομένων, πέντε εξόδους.', 'Один набор данных, пять результатов.'),
    'Change a price in one place and every one of those changes with it.':
        ('Αλλάξτε μια τιμή σε ένα σημείο και όλα τα παραπάνω αλλάζουν μαζί.',
         'Измените цену в одном месте — и всё перечисленное изменится вместе с ней.'),

    # ---- chat mock ----
    'Do you have a jeep for tomorrow? What&rsquo;s the price for 3 days?':
        ('Έχετε τζιπ για αύριο; Ποια είναι η τιμή για 3 μέρες;',
         'У вас есть джип на завтра? Сколько стоит на 3 дня?'),
    'Yes — a Suzuki Jimny is free tomorrow. Three days is &euro;135, insurance included. Want me to hold it?':
        ('Ναι — ένα Suzuki Jimny είναι ελεύθερο αύριο. Οι τρεις μέρες είναι 135 €, με την ασφάλεια. Θέλετε να το κρατήσω;',
         'Да — Suzuki Jimny свободен завтра. Три дня — 135 €, страховка включена. Забронировать?'),
    'Yes please': ('Ναι, παρακαλώ', 'Да, пожалуйста'),
    'Booking confirmed. Deposit taken, added to the July calendar.':
        ('Η κράτηση επιβεβαιώθηκε. Η προκαταβολή ελήφθη και προστέθηκε στο ημερολόγιο Ιουλίου.',
         'Бронирование подтверждено. Депозит принят, добавлено в календарь на июль.'),

    # ---- proof ----
    'Proof &middot; Limassol': ('Απόδειξη · Λεμεσός', 'Доказательство · Лимасол'),
    'enquiries booked between 9pm and 8am last month':
        ('ερωτήματα έγιναν κρατήσεις μεταξύ 9 μ.μ. και 8 π.μ. τον περασμένο μήνα',
         'запросов превратились в брони между 21:00 и 8:00 в прошлом месяце'),
    'A car rental operator in Limassol, live at &euro;150 a month. The after-hours coverage booked those 14 enquiries automatically — ones the owner would otherwise have picked up the next morning, if they were still waiting.':
        ('Μια εταιρεία ενοικίασης αυτοκινήτων στη Λεμεσό, ενεργή στα 150 € τον μήνα. Η κάλυψη εκτός ωραρίου έκλεισε αυτά τα 14 ερωτήματα αυτόματα — αυτά που ο ιδιοκτήτης θα έπιανε το επόμενο πρωί, αν περίμεναν ακόμη.',
         'Прокат автомобилей в Лимасоле, работает за 150 € в месяц. Покрытие в нерабочие часы автоматически закрыло эти 14 запросов — те, которые владелец увидел бы только утром, если бы они ещё ждали.'),
    'A car rental operator in Limassol, live at &euro;150 a month. Those 14 were booked while the owner was asleep.':
        ('Μια εταιρεία ενοικίασης αυτοκινήτων στη Λεμεσό, ενεργή στα 150 € τον μήνα. Αυτά τα 14 κλείστηκαν όσο ο ιδιοκτήτης κοιμόταν.',
         'Прокат автомобилей в Лимасоле, работает за 150 € в месяц. Эти 14 броней были сделаны, пока владелец спал.'),
    'Car rental, Limassol': ('Ενοικίαση αυτοκινήτων, Λεμεσός', 'Прокат авто, Лимасол'),
    'Enquiries answered': ('Ερωτήματα που απαντήθηκαν', 'Отвечено на запросы'),
    'Answered after hours': ('Απαντήθηκαν εκτός ωραρίου', 'Отвечено вне рабочих часов'),
    'Average reply time': ('Μέσος χρόνος απάντησης', 'Среднее время ответа'),
    'under a minute': ('κάτω από ένα λεπτό', 'меньше минуты'),

    # ---- how it works ----
    'You tell us the facts': ('Μας λέτε τα δεδομένα', 'Вы сообщаете нам факты'),
    'We build it around them': ('Το χτίζουμε γύρω από αυτά', 'Мы строим вокруг них'),
    'It runs, and we keep it running': ('Τρέχει, και το κρατάμε να τρέχει',
                                        'Оно работает, а мы поддерживаем работу'),
    'Most small businesses keep the same facts in four places and keep three of them wrong. Ownerdeck keeps them in one place and points everything else at it.':
        ('Οι περισσότερες μικρές επιχειρήσεις κρατούν τα ίδια δεδομένα σε τέσσερα σημεία και τα τρία είναι λάθος. Το Ownerdeck τα κρατά σε ένα σημείο και στρέφει όλα τα υπόλοιπα εκεί.',
         'Большинство малых бизнесов хранят одни и те же данные в четырёх местах, и в трёх они неверны. Ownerdeck хранит их в одном месте и направляет туда всё остальное.'),
    'Services, prices, seasons, availability, opening hours, deposit and cancellation policy, photos. One conversation, usually about an hour.':
        ('Υπηρεσίες, τιμές, σεζόν, διαθεσιμότητα, ωράριο, πολιτική προκαταβολής και ακύρωσης, φωτογραφίες. Μία συζήτηση, συνήθως περίπου μία ώρα.',
         'Услуги, цены, сезоны, доступность, часы работы, правила депозита и отмены, фотографии. Один разговор, обычно около часа.'),
    'The database, then the website on top of it, then the assistant that answers from it, then bookings and the follow-up if you have taken those cards.':
        ('Πρώτα η βάση δεδομένων, μετά η ιστοσελίδα πάνω της, μετά ο βοηθός που απαντά από αυτήν, μετά οι κρατήσεις και η επικοινωνία μετά, αν έχετε πάρει αυτές τις κάρτες.',
         'Сначала база данных, затем сайт поверх неё, затем ассистент, который отвечает из неё, затем бронирования и последующая связь, если вы взяли эти карты.'),
    'Hosting, backups, updates and the changes you ask for are the monthly fee. You send a message, we make the change.':
        ('Η φιλοξενία, τα αντίγραφα ασφαλείας, οι ενημερώσεις και οι αλλαγές που ζητάτε είναι η μηνιαία συνδρομή. Στέλνετε μήνυμα, κάνουμε την αλλαγή.',
         'Хостинг, резервные копии, обновления и запрошенные вами изменения входят в ежемесячную плату. Вы пишете — мы вносим изменение.'),
    'The first week': ('Η πρώτη εβδομάδα', 'Первая неделя'),
    'What actually happens.': ('Τι γίνεται στην πράξη.', 'Что происходит на самом деле.'),
    'No project plan, no kick-off deck. A conversation, a build, a check, and then it is live.':
        ('Χωρίς πλάνο έργου, χωρίς παρουσίαση εκκίνησης. Μια συζήτηση, μια κατασκευή, ένας έλεγχος, και μετά είναι ζωντανό.',
         'Никакого плана проекта и презентаций. Разговор, сборка, проверка — и всё работает.'),
    'We talk for an hour and write down everything your business charges for.':
        ('Μιλάμε για μία ώρα και καταγράφουμε όλα όσα χρεώνει η επιχείρησή σας.',
         'Мы час разговариваем и записываем всё, за что берёт деньги ваш бизнес.'),
    'You get the database and the admin screen, filled in, to correct.':
        ('Παίρνετε τη βάση δεδομένων και την οθόνη διαχείρισης, συμπληρωμένες, για να τις διορθώσετε.',
         'Вы получаете заполненную базу данных и админ-панель, чтобы всё проверить.'),
    'The site and the assistant are live on a test link for you to try.':
        ('Η ιστοσελίδα και ο βοηθός είναι ζωντανά σε δοκιμαστικό σύνδεσμο για να τα δοκιμάσετε.',
         'Сайт и ассистент доступны по тестовой ссылке — попробуйте.'),
    'We point your number and your domain at it, and it goes live.':
        ('Στρέφουμε τον αριθμό και το domain σας σε αυτό, και βγαίνει ζωντανά.',
         'Мы направляем на него ваш номер и домен — и всё запускается.'),
    'Where the line is': ('Πού είναι το όριο', 'Где проходит граница'),
    'The assistant knows your prices. It does not invent them.':
        ('Ο βοηθός ξέρει τις τιμές σας. Δεν τις επινοεί.',
         'Ассистент знает ваши цены. Он их не выдумывает.'),
    'It answers from your database and nothing else. When it does not know, it says so and hands the conversation to you rather than guessing. You can take over any conversation at any time.':
        ('Απαντά από τη βάση δεδομένων σας και από τίποτε άλλο. Όταν δεν ξέρει, το λέει και σας παραδίδει τη συνομιλία αντί να μαντεύει. Μπορείτε να αναλάβετε οποιαδήποτε συνομιλία, οποιαδήποτε στιγμή.',
         'Он отвечает только из вашей базы данных. Если он не знает, он так и говорит и передаёт разговор вам, а не гадает. Вы можете вмешаться в любой разговор в любой момент.'),

    # ---- pricing ----
    'Pick a hand. Add cards as you grow.':
        ('Διαλέξτε χέρι. Προσθέστε κάρτες καθώς μεγαλώνετε.',
         'Выберите руку. Добавляйте карты по мере роста.'),
    'A one-off fee to build it, then a monthly fee to run it. The monthly covers hosting, the database, the assistant, backups and the changes you ask for. No VAT is charged.':
        ('Μια εφάπαξ χρέωση για την κατασκευή, μετά μια μηνιαία για τη λειτουργία. Η μηνιαία καλύπτει φιλοξενία, βάση δεδομένων, τον βοηθό, αντίγραφα ασφαλείας και τις αλλαγές που ζητάτε. Δεν χρεώνεται ΦΠΑ.',
         'Разовая плата за создание, затем ежемесячная за обслуживание. Ежемесячная покрывает хостинг, базу данных, работу ассистента, резервные копии и запрошенные изменения. НДС не начисляется.'),
    'one-off, to build it': ('εφάπαξ, για την κατασκευή', 'разово, за создание'),
    'per month after': ('τον μήνα μετά', 'в месяц далее'),
    'Common choice': ('Συνήθης επιλογή', 'Частый выбор'),
    'Not included:': ('Δεν περιλαμβάνεται:', 'Не входит:'),
    'The AI assistant, plus a basic website of your own. Everything a small business needs to be found and to reply.':
        ('Ο βοηθός τεχνητής νοημοσύνης, μαζί με μια βασική δική σας ιστοσελίδα. Ό,τι χρειάζεται μια μικρή επιχείρηση για να βρίσκεται και να απαντά.',
         'ИИ-ассистент плюс собственный базовый сайт. Всё, что нужно малому бизнесу, чтобы его находили и он отвечал.'),
    'The website, the database behind it, the assistant answering, and the bookings landing on your phone.':
        ('Η ιστοσελίδα, η βάση δεδομένων από πίσω, ο βοηθός που απαντά και οι κρατήσεις που φτάνουν στο κινητό σας.',
         'Сайт, база данных за ним, отвечающий ассистент и брони, которые приходят вам на телефон.'),
    'All five cards. Everything above, plus your Google listing set up properly and customers who come back.':
        ('Και οι πέντε κάρτες. Όλα τα παραπάνω, μαζί με τη σωστή ρύθμιση της καταχώρισής σας στο Google και πελάτες που επιστρέφουν.',
         'Все пять карт. Всё вышеперечисленное плюс правильно настроенный профиль в Google и возвращающиеся клиенты.'),
    'AI assistant on WhatsApp, Instagram DMs and website chat':
        ('Βοηθός AI σε WhatsApp, Instagram DMs και chat ιστοσελίδας',
         'ИИ-ассистент в WhatsApp, Instagram DM и чате сайта'),
    'A basic website — your services, prices and contact details':
        ('Μια βασική ιστοσελίδα — υπηρεσίες, τιμές και στοιχεία επικοινωνίας',
         'Базовый сайт — услуги, цены и контакты'),
    'Hosting, domain and certificate': ('Φιλοξενία, domain και πιστοποιητικό',
                                        'Хостинг, домен и сертификат'),
    'Answers in any language your customers write in':
        ('Απαντήσεις σε όποια γλώσσα γράφουν οι πελάτες σας',
         'Ответы на любом языке, на котором пишут клиенты'),
    'Handover to you whenever it is unsure':
        ('Παράδοση σε εσάς όποτε δεν είναι σίγουρος', 'Передача вам при любой неуверенности'),
    'Changes when you need them': ('Αλλαγές όποτε τις χρειάζεστε', 'Изменения, когда нужно'),
    'Live database and admin screen': ('Ζωντανή βάση δεδομένων και οθόνη διαχείρισης',
                                       'Живая база данных и админ-панель'),
    'Bookings, deposits and calendar': ('Κρατήσεις, προκαταβολές και ημερολόγιο',
                                        'Брони, депозиты и календарь'),
    'Follow-up campaigns': ('Καμπάνιες επικοινωνίας', 'Кампании последующей связи'),
    'Everything in Answer': ('Όλα του Answer', 'Всё из Answer'),
    'Everything in Deck': ('Όλα του Deck', 'Всё из Deck'),
    'A website that reads live from your prices':
        ('Μια ιστοσελίδα που διαβάζει ζωντανά τις τιμές σας',
         'Сайт, который читает ваши цены напрямую'),
    'The database and an admin screen you control':
        ('Η βάση δεδομένων και μια οθόνη διαχείρισης που ελέγχετε',
         'База данных и админ-панель под вашим контролем'),
    'Real availability, confirmations and deposits':
        ('Πραγματική διαθεσιμότητα, επιβεβαιώσεις και προκαταβολές',
         'Реальная доступность, подтверждения и депозиты'),
    'A calendar that fills itself in': ('Ένα ημερολόγιο που συμπληρώνεται μόνο του',
                                        'Календарь, который заполняется сам'),
    'Google Business Profile set up and kept current':
        ('Το Google Business Profile ρυθμισμένο και ενημερωμένο',
         'Google Business Profile настроен и поддерживается актуальным'),
    'A review request after every booking': ('Αίτημα αξιολόγησης μετά από κάθε κράτηση',
                                             'Запрос отзыва после каждой брони'),
    'Reminders and off-season offers': ('Υπενθυμίσεις και προσφορές εκτός σεζόν',
                                        'Напоминания и предложения вне сезона'),
    'Past customers brought back': ('Παλιοί πελάτες που επιστρέφουν',
                                    'Возвращение прошлых клиентов'),
    'Start with Answer': ('Ξεκινήστε με το Answer', 'Начать с Answer'),
    'Get the Deck': ('Πάρτε το Deck', 'Выбрать Deck'),
    'Get the Full Deck': ('Πάρτε το Full Deck', 'Выбрать Full Deck'),
    'Starting from nothing': ('Ξεκινώντας από το μηδέν', 'Начиная с нуля'),
    'New business? Everything from zero in a week.':
        ('Νέα επιχείρηση; Τα πάντα από το μηδέν σε μία εβδομάδα.',
         'Новый бизнес? Всё с нуля за неделю.'),
    'Nothing upfront. &euro;249 a month on a twelve month term, and you get the Deck — the site, the database, the assistant and the bookings — built from scratch.':
        ('Τίποτα προκαταβολικά. 249 € τον μήνα με δωδεκάμηνη δέσμευση, και παίρνετε το Deck — την ιστοσελίδα, τη βάση δεδομένων, τον βοηθό και τις κρατήσεις — φτιαγμένα από την αρχή.',
         'Без предоплаты. 249 € в месяц на двенадцать месяцев, и вы получаете Deck — сайт, базу данных, ассистента и бронирования — созданные с нуля.'),
    'Start from zero': ('Ξεκινήστε από το μηδέν', 'Начать с нуля'),
    'What the monthly covers': ('Τι καλύπτει η μηνιαία', 'Что покрывает ежемесячная плата'),
    'Running it is the job, not an extra.':
        ('Η λειτουργία είναι η δουλειά, όχι έξτρα.', 'Обслуживание — это работа, а не доплата.'),
    'Hosting and domain': ('Φιλοξενία και domain', 'Хостинг и домен'),
    'The site, the certificate and the domain renewal.':
        ('Η ιστοσελίδα, το πιστοποιητικό και η ανανέωση του domain.',
         'Сайт, сертификат и продление домена.'),
    'The assistant running': ('Η λειτουργία του βοηθού', 'Работа ассистента'),
    'Every message answered, every hour, at our cost not yours.':
        ('Κάθε μήνυμα απαντημένο, κάθε ώρα, με δικό μας κόστος και όχι δικό σας.',
         'Каждое сообщение, в любой час, за наш счёт, а не за ваш.'),
    'Backups and updates': ('Αντίγραφα ασφαλείας και ενημερώσεις',
                            'Резервные копии и обновления'),
    'Kept online, kept current, kept backed up.':
        ('Πάντα online, πάντα ενημερωμένο, πάντα με αντίγραφα.',
         'Всегда онлайн, всегда актуально, всегда с резервной копией.'),
    'Changes you ask for': ('Αλλαγές που ζητάτε', 'Изменения по вашему запросу'),
    'New prices, new services, new photos. You message, we change it.':
        ('Νέες τιμές, νέες υπηρεσίες, νέες φωτογραφίες. Στέλνετε μήνυμα, το αλλάζουμε.',
         'Новые цены, услуги, фотографии. Вы пишете — мы меняем.'),
    'Not covered: rebuilding the site from scratch, adding a card you did not take, or work outside the online side of the business. We will quote before doing any of it.':
        ('Δεν καλύπτεται: ανακατασκευή της ιστοσελίδας από την αρχή, προσθήκη κάρτας που δεν πήρατε, ή εργασία εκτός της ψηφιακής πλευράς. Θα δώσουμε προσφορά πριν κάνουμε οτιδήποτε από αυτά.',
         'Не покрывается: пересборка сайта с нуля, добавление невзятой карты или работа вне онлайн-части бизнеса. Мы дадим смету, прежде чем что-либо делать.'),
    'Money questions': ('Ερωτήσεις για τα χρήματα', 'Вопросы о деньгах'),
    'The awkward ones, answered.': ('Οι δύσκολες, απαντημένες.', 'Неудобные — с ответами.'),
    'Why is there a build fee now?': ('Γιατί υπάρχει τώρα χρέωση κατασκευής;',
                                      'Почему теперь есть плата за создание?'),
    'Because building a website, a database and a working assistant takes real days, and a monthly-only price means every new client starts deeply underwater. The build fee covers the build at cost. The monthly is what keeps it running.':
        ('Επειδή η κατασκευή ιστοσελίδας, βάσης δεδομένων και ενός βοηθού που δουλεύει παίρνει πραγματικές μέρες, και μια τιμή μόνο μηνιαία σημαίνει ότι κάθε νέος πελάτης ξεκινά βαθιά ζημιωμένος. Η χρέωση κατασκευής καλύπτει την κατασκευή στο κόστος. Η μηνιαία είναι αυτό που το κρατά να λειτουργεί.',
         'Потому что создание сайта, базы данных и работающего ассистента занимает реальные дни, а цена только по подписке означает, что каждый новый клиент начинается с глубокого минуса. Плата за создание покрывает работу по себестоимости. Ежемесячная плата поддерживает работу.'),
    'Is there VAT on top?': ('Υπάρχει ΦΠΑ επιπλέον;', 'НДС добавляется?'),
    'No. Ownerdeck is not registered for VAT, so the prices shown are the prices you pay.':
        ('Όχι. Το Ownerdeck δεν είναι εγγεγραμμένο στο ΦΠΑ, οπότε οι τιμές που βλέπετε είναι οι τιμές που πληρώνετε.',
         'Нет. Ownerdeck не зарегистрирован плательщиком НДС, поэтому указанные цены — это то, что вы платите.'),
    'Can I stop paying?': ('Μπορώ να σταματήσω να πληρώνω;', 'Могу ли я перестать платить?'),
    'Yes, with a month&rsquo;s notice, on any plan. There is no minimum term. If you stop, you keep the site files and an export of your database, and we hand both over free.':
        ('Ναι, με προειδοποίηση ενός μήνα, σε οποιοδήποτε πακέτο. Δεν υπάρχει ελάχιστη διάρκεια. Αν σταματήσετε, κρατάτε τα αρχεία της ιστοσελίδας και εξαγωγή της βάσης δεδομένων σας, και σας τα παραδίδουμε δωρεάν.',
         'Да, с уведомлением за месяц, на любом тарифе. Минимального срока нет. Если вы остановитесь, вы сохраняете файлы сайта и выгрузку базы данных, и мы передаём их бесплатно.'),
    'Do you take a cut of my bookings?': ('Παίρνετε ποσοστό από τις κρατήσεις μου;',
                                          'Вы берёте процент с моих броней?'),
    'No. Deposits and payments run through your own account and your own payment provider. We never handle your customers&rsquo; money.':
        ('Όχι. Οι προκαταβολές και οι πληρωμές περνούν από τον δικό σας λογαριασμό και τον δικό σας πάροχο πληρωμών. Δεν διαχειριζόμαστε ποτέ τα χρήματα των πελατών σας.',
         'Нет. Депозиты и платежи проходят через ваш собственный счёт и вашего платёжного провайдера. Мы никогда не обрабатываем деньги ваших клиентов.'),
    'What if I only want the assistant?': ('Κι αν θέλω μόνο τον βοηθό;',
                                           'А если мне нужен только ассистент?'),
    'That is the Answer plan, and it now comes with a basic website of its own. If you already have a website you are happy with, we will point the assistant at it and price accordingly — just ask.':
        ('Αυτό είναι το πακέτο Answer, και τώρα περιλαμβάνει και μια δική του βασική ιστοσελίδα. Αν έχετε ήδη ιστοσελίδα που σας ικανοποιεί, θα στρέψουμε τον βοηθό σε αυτήν και θα τιμολογήσουμε ανάλογα — απλώς ρωτήστε.',
         'Это тариф Answer, и теперь в него входит собственный базовый сайт. Если у вас уже есть сайт, который вас устраивает, мы направим ассистента на него и пересчитаем цену — просто спросите.'),

    # ---- entry tier: Site (website only, no assistant) ----
    'A proper website, built and run for you. No assistant, no bookings — just somewhere real to send people that never goes out of date.':
        ('Μια σωστή ιστοσελίδα, φτιαγμένη και συντηρημένη για εσάς. Χωρίς βοηθό, χωρίς κρατήσεις — απλώς κάτι πραγματικό όπου να στέλνετε κόσμο, που δεν παλιώνει ποτέ.',
         'Нормальный сайт, созданный и обслуживаемый для вас. Без ассистента и бронирований — просто место, куда можно направлять людей, и которое не устаревает.'),
    'A fast website — your services, prices and contact details':
        ('Μια γρήγορη ιστοσελίδα — υπηρεσίες, τιμές και στοιχεία επικοινωνίας',
         'Быстрый сайт — услуги, цены и контакты'),
    'Works properly on a phone, and on Google':
        ('Λειτουργεί σωστά στο κινητό και στο Google',
         'Корректно работает на телефоне и в Google'),
    'Changes when you need them — you message, we change it':
        ('Αλλαγές όποτε τις χρειάζεστε — στέλνετε μήνυμα, το αλλάζουμε',
         'Изменения по запросу — вы пишете, мы меняем'),
    'Backups and security updates':
        ('Αντίγραφα ασφαλείας και ενημερώσεις ασφαλείας',
         'Резервные копии и обновления безопасности'),
    'AI assistant': ('Βοηθός AI', 'ИИ-ассистент'),
    'Start with Site': ('Ξεκινήστε με το Site', 'Начать с Site'),
    'Everything in Site': ('Όλα του Site', 'Всё из Site'),
    'The AI assistant on WhatsApp, Instagram DMs and website chat':
        ('Ο βοηθός AI σε WhatsApp, Instagram DMs και chat ιστοσελίδας',
         'ИИ-ассистент в WhatsApp, Instagram DM и чате сайта'),
    'The assistant starts at the Deck, because it is only as good as the database behind it. Pointing it at a website with no live prices is how you get an assistant that confidently quotes last year&rsquo;s rates. If you already have a website you are happy with and want the assistant bolted onto it, we will quote for that separately — just ask.':
        ('Ο βοηθός ξεκινά από το Deck, γιατί είναι τόσο καλός όσο η βάση δεδομένων πίσω του. Αν τον στρέψετε σε μια ιστοσελίδα χωρίς ζωντανές τιμές, θα έχετε έναν βοηθό που δίνει με σιγουριά τις περσινές τιμές. Αν έχετε ήδη ιστοσελίδα που σας ικανοποιεί και θέλετε τον βοηθό πάνω της, θα δώσουμε ξεχωριστή προσφορά — απλώς ρωτήστε.',
         'Ассистент начинается с Deck, потому что он хорош ровно настолько, насколько хороша база данных за ним. Если направить его на сайт без актуальных цен, вы получите ассистента, уверенно называющего прошлогодние тарифы. Если у вас уже есть сайт, который вас устраивает, и вы хотите добавить к нему ассистента, мы посчитаем это отдельно — просто спросите.'),
    'That is the point of the deck. Start with Site to get online properly, move to the Deck when you want the messages answered and the bookings taken, add Reach and Return when you want the quiet months filled.':
        ('Αυτό ακριβώς είναι το νόημα της τράπουλας. Ξεκινήστε με το Site για να βγείτε online σωστά, περάστε στο Deck όταν θέλετε να απαντιούνται τα μηνύματα και να κλείνονται οι κρατήσεις, προσθέστε Reach και Return όταν θέλετε να γεμίσουν οι ήσυχοι μήνες.',
         'В этом и смысл колоды. Начните с Site, чтобы нормально выйти в онлайн, перейдите на Deck, когда захотите, чтобы отвечали на сообщения и принимали брони, добавьте Reach и Return, когда захотите заполнить тихие месяцы.'),

    # ---- home page: trades strip, ownership, the person behind it ----
    'Who we build for': ('Για ποιους φτιάχνουμε', 'Для кого мы работаем'),
    'You have answered these questions a thousand times.':
        ('Έχετε απαντήσει σε αυτές τις ερωτήσεις χίλιες φορές.',
         'Вы отвечали на эти вопросы тысячу раз.'),
    'Different trades, the same four questions all day. What does it cost. Is it free on Saturday. Do you deliver. Can I pay a deposit now.':
        ('Διαφορετικά επαγγέλματα, οι ίδιες τέσσερις ερωτήσεις όλη μέρα. Πόσο κοστίζει. Είναι ελεύθερο το Σάββατο. Κάνετε παράδοση. Μπορώ να πληρώσω προκαταβολή τώρα.',
         'Разные сферы, одни и те же четыре вопроса весь день. Сколько стоит. Свободно ли в субботу. Есть ли доставка. Могу ли я внести депозит сейчас.'),
    'Every trade we build for': ('Κάθε επάγγελμα για το οποίο φτιάχνουμε',
                                 'Все сферы, для которых мы работаем'),
    'No lock-in': ('Χωρίς δέσμευση', 'Без привязки'),
    'You own all of it.': ('Όλα ανήκουν σε εσάς.', 'Всё принадлежит вам.'),
    'The usual worry about handing your online side to someone else is that you never get it back. So here is the deal in plain words, and it is the same deal written into the terms.':
        ('Η συνηθισμένη ανησυχία όταν παραδίδετε την ψηφιακή σας πλευρά σε κάποιον άλλον είναι ότι δεν την ξαναπαίρνετε ποτέ. Να λοιπόν η συμφωνία με απλά λόγια, και είναι η ίδια συμφωνία που είναι γραμμένη στους όρους.',
         'Обычный страх при передаче онлайн-части бизнеса другому — что вы её больше не вернёте. Поэтому вот условия простыми словами, и это те же условия, что записаны в договоре.'),
    'Your site, your data, your number': ('Η ιστοσελίδα σας, τα δεδομένα σας, ο αριθμός σας',
                                          'Ваш сайт, ваши данные, ваш номер'),
    'The website, the database and the WhatsApp number stay yours throughout. We never hold them.':
        ('Η ιστοσελίδα, η βάση δεδομένων και ο αριθμός WhatsApp παραμένουν δικά σας από την αρχή ως το τέλος. Δεν τα κρατάμε ποτέ εμείς.',
         'Сайт, база данных и номер WhatsApp всё время остаются вашими. Мы их никогда не удерживаем.'),
    'Leave with thirty days&rsquo; notice': ('Φύγετε με προειδοποίηση τριάντα ημερών',
                                             'Уйти с уведомлением за тридцать дней'),
    'No twelve month tie-in. We hand over the site files and an export of your database, free.':
        ('Χωρίς δωδεκάμηνη δέσμευση. Παραδίδουμε τα αρχεία της ιστοσελίδας και εξαγωγή της βάσης δεδομένων σας, δωρεάν.',
         'Без привязки на двенадцать месяцев. Мы бесплатно передаём файлы сайта и выгрузку вашей базы данных.'),
    'We never touch your money': ('Δεν αγγίζουμε ποτέ τα χρήματά σας',
                                  'Мы никогда не касаемся ваших денег'),
    'Deposits run through your own account and your own payment provider. We take no cut of a booking.':
        ('Οι προκαταβολές περνούν από τον δικό σας λογαριασμό και τον δικό σας πάροχο πληρωμών. Δεν παίρνουμε ποσοστό από καμία κράτηση.',
         'Депозиты проходят через ваш собственный счёт и вашего платёжного провайдера. Мы не берём процент с бронирований.'),
    'The price is the price': ('Η τιμή είναι η τιμή', 'Цена есть цена'),
    'No VAT, no setup surprises. If a job falls outside your plan we quote it before starting.':
        ('Χωρίς ΦΠΑ, χωρίς εκπλήξεις στη ρύθμιση. Αν μια δουλειά πέφτει εκτός του πακέτου σας, δίνουμε προσφορά πριν ξεκινήσουμε.',
         'Без НДС и сюрпризов при запуске. Если работа выходит за рамки вашего тарифа, мы дадим смету до начала.'),
    'Who you are dealing with': ('Με ποιον έχετε να κάνετε', 'С кем вы имеете дело'),
    'One person builds it. The same person answers you.':
        ('Ένα άτομο το φτιάχνει. Το ίδιο άτομο σας απαντά.',
         'Один человек создаёт это. Тот же человек вам отвечает.'),
    'Ownerdeck is not an agency with account managers and a ticket queue. You get the person who wrote the thing, on WhatsApp, usually the same day. That is the whole reason a small operator can get work at this standard at this price.':
        ('Το Ownerdeck δεν είναι πρακτορείο με υπεύθυνους πελατών και ουρά αιτημάτων. Μιλάτε με το άτομο που το έγραψε, στο WhatsApp, συνήθως την ίδια μέρα. Αυτός ακριβώς είναι ο λόγος που μια μικρή επιχείρηση μπορεί να έχει δουλειά αυτού του επιπέδου σε αυτή την τιμή.',
         'Ownerdeck — не агентство с аккаунт-менеджерами и очередью заявок. Вы общаетесь с человеком, который всё это написал, в WhatsApp, обычно в тот же день. Именно поэтому небольшой бизнес может получить работу такого уровня по такой цене.'),
    'Ask me anything': ('Ρωτήστε με ό,τι θέλετε', 'Спросите меня о чём угодно'),
    'Builds it, runs it, and answers the messages.':
        ('Το φτιάχνει, το τρέχει και απαντά στα μηνύματα.',
         'Создаёт, обслуживает и отвечает на сообщения.'),
    'Sole trader, established in Cyprus': ('Ατομική επιχείρηση, με έδρα την Κύπρο',
                                           'Индивидуальный предприниматель, зарегистрирован на Кипре'),
    'Not registered for VAT, so no VAT on any fee':
        ('Μη εγγεγραμμένος στο ΦΠΑ, οπότε καμία χρέωση δεν έχει ΦΠΑ',
         'Не зарегистрирован плательщиком НДС, поэтому НДС ни на что не начисляется'),
    'Works remotely, so where you are does not matter':
        ('Δουλεύει εξ αποστάσεως, οπότε δεν έχει σημασία πού βρίσκεστε',
         'Работает удалённо, поэтому ваше местоположение не имеет значения'),

    # ---- entry tier with website chat, and the custom quote ----
    'A proper website with an AI chat on it. The chat answers on your site — WhatsApp and Instagram start at the Deck.':
        ('Μια σωστή ιστοσελίδα με AI chat πάνω της. Το chat απαντά στη σελίδα σας — το WhatsApp και το Instagram ξεκινούν από το Deck.',
         'Нормальный сайт с ИИ-чатом на нём. Чат отвечает на вашем сайте — WhatsApp и Instagram начинаются с Deck.'),
    'An AI chat on the site, answering from your prices':
        ('Ένα AI chat στη σελίδα, που απαντά από τις τιμές σας',
         'ИИ-чат на сайте, отвечающий по вашим ценам'),
    'The assistant on WhatsApp and Instagram': ('Ο βοηθός σε WhatsApp και Instagram',
                                                'Ассистент в WhatsApp и Instagram'),
    'Custom': ('Κατά παραγγελία', 'Индивидуально'),
    'Need something that is not on this list?': ('Χρειάζεστε κάτι που δεν είναι σε αυτή τη λίστα;',
                                                 'Нужно что-то, чего нет в списке?'),
    'A bigger site, several locations, a system you already use that has to connect to it, or a job that does not fit a card. Tell us what you need and we will send a written quote — a fixed price, no obligation.':
        ('Μια μεγαλύτερη ιστοσελίδα, πολλές τοποθεσίες, ένα σύστημα που ήδη χρησιμοποιείτε και πρέπει να συνδεθεί, ή μια δουλειά που δεν ταιριάζει σε καμία κάρτα. Πείτε μας τι χρειάζεστε και θα στείλουμε γραπτή προσφορά — σταθερή τιμή, χωρίς δέσμευση.',
         'Более крупный сайт, несколько локаций, система, которую вы уже используете и которую нужно подключить, или работа, не подходящая ни под одну карту. Расскажите, что нужно, и мы пришлём письменное предложение — фиксированная цена, без обязательств.'),
    'Ask for a quote': ('Ζητήστε προσφορά', 'Запросить предложение'),

    # ---- the get-started flow ----
    'Get started': ('Ξεκινήστε', 'Начать'),
    'Or message us on WhatsApp': ('Ή στείλτε μας μήνυμα στο WhatsApp',
                                  'Или напишите нам в WhatsApp'),
    'Message me directly': ('Στείλτε μου απευθείας', 'Напишите мне напрямую'),
    'Back': ('Πίσω', 'Назад'),
    'Step one': ('Βήμα ένα', 'Шаг первый'),
    'Step two': ('Βήμα δύο', 'Шаг второй'),
    'Step three': ('Βήμα τρία', 'Шаг третий'),
    'Last step': ('Τελευταίο βήμα', 'Последний шаг'),

    'What kind of business is it?': ('Τι είδους επιχείρηση είναι;', 'Что у вас за бизнес?'),
    'So the quote is about your trade rather than a generic package.':
        ('Ώστε η προσφορά να αφορά το δικό σας επάγγελμα και όχι ένα γενικό πακέτο.',
         'Чтобы предложение было про вашу сферу, а не про общий пакет.'),
    'Something else': ('Κάτι άλλο', 'Что-то другое'),

    'How much of it do you want run for you?':
        ('Πόσο από αυτό θέλετε να το τρέχουμε εμείς;',
         'Сколько из этого вы хотите передать нам?'),
    'Not sure? Pick the middle one — we will tell you honestly if you need less.':
        ('Δεν είστε σίγουροι; Διαλέξτε το μεσαίο — θα σας πούμε ειλικρινά αν χρειάζεστε λιγότερα.',
         'Не уверены? Выберите средний — мы честно скажем, если вам нужно меньше.'),
    'Not sure yet': ('Δεν είμαι σίγουρος ακόμη', 'Пока не уверен'),
    'Talk it through first': ('Ας το συζητήσουμε πρώτα', 'Сначала обсудим'),

    'Anything we should know?': ('Κάτι που πρέπει να ξέρουμε;',
                                 'Что-нибудь, что нам стоит знать?'),
    'Anything we should know': ('Κάτι που πρέπει να ξέρουμε',
                                'Что-нибудь, что нам стоит знать'),
    'Optional. A sentence about what is not working now is usually enough.':
        ('Προαιρετικό. Μια πρόταση για το τι δεν λειτουργεί τώρα συνήθως αρκεί.',
         'Необязательно. Обычно хватает одного предложения о том, что сейчас не работает.'),
    'See what happens next': ('Δείτε τι γίνεται μετά', 'Посмотреть, что дальше'),

    'That is everything we need.': ('Αυτά είναι όλα όσα χρειαζόμαστε.',
                                    'Это всё, что нам нужно.'),
    'Open the chat and it will already say all of this, so you are not repeating yourself. You will get a straight answer, usually the same day.':
        ('Ανοίξτε τη συνομιλία και θα λέει ήδη όλα αυτά, ώστε να μην τα επαναλαμβάνετε. Θα πάρετε ξεκάθαρη απάντηση, συνήθως την ίδια μέρα.',
         'Откройте чат — в нём уже будет всё это, так что повторяться не придётся. Вы получите прямой ответ, обычно в тот же день.'),
    'Open WhatsApp': ('Ανοίξτε το WhatsApp', 'Открыть WhatsApp'),
    'Email instead': ('Ή στείλτε email', 'Или напишите на email'),
    'Your answers are not sent anywhere. They are filled into a message you choose to open. Card details are handled entirely by Stripe and never touch this site.':
        ('Οι απαντήσεις σας δεν στέλνονται πουθενά. Συμπληρώνονται σε ένα μήνυμα που εσείς επιλέγετε να ανοίξετε. Τα στοιχεία της κάρτας τα χειρίζεται εξ ολοκλήρου η Stripe και δεν περνούν ποτέ από αυτόν τον ιστότοπο.',
         'Ваши ответы никуда не отправляются. Они подставляются в сообщение, которое вы сами решаете открыть. Данные карты полностью обрабатывает Stripe — они никогда не попадают на этот сайт.'),

    # ---- the holding deposit ----
    'Want the slot held while we talk?': ('Θέλετε να κρατήσουμε τη θέση όσο μιλάμε;',
                                          'Хотите, чтобы место держалось, пока мы общаемся?'),
    '&euro;75, refundable in full until work starts, and credited against your build fee. It is a way to hold your place in the queue, not a commitment.':
        ('75 €, επιστρέφονται πλήρως μέχρι να ξεκινήσει η δουλειά και πιστώνονται στο κόστος κατασκευής. Είναι τρόπος να κρατήσετε τη σειρά σας, όχι δέσμευση.',
         '75 €, полностью возвращаются до начала работы и засчитываются в стоимость сборки. Это способ занять очередь, а не обязательство.'),
    'Hold my slot &mdash; &euro;75': ('Κρατήστε τη θέση μου — 75 €', 'Забронировать место — 75 €'),
    'Deposit received. Your slot is held — open the chat and we will pick it up from here.':
        ('Η προκαταβολή ελήφθη. Η θέση σας κρατήθηκε — ανοίξτε τη συνομιλία και συνεχίζουμε από εδώ.',
         'Депозит получен. Место за вами — откройте чат, и мы продолжим отсюда.'),

    # ---- plan price lines in the flow ----
    '€600 to build, then €99 a month':
        ('600 € για την κατασκευή, μετά 99 € τον μήνα',
         '600 € за создание, затем 99 € в месяц'),
    '€1,900 to build, then €249 a month':
        ('1.900 € για την κατασκευή, μετά 249 € τον μήνα',
         '1 900 € за создание, затем 249 € в месяц'),
    '€2,400 to build, then €299 a month':
        ('2.400 € για την κατασκευή, μετά 299 € τον μήνα',
         '2 400 € за создание, затем 299 € в месяц'),

    # ---- rental-led hero ----
    'Run the online side of your rental business.':
        ('Τρέξτε την ψηφιακή πλευρά της επιχείρησης ενοικιάσεών σας.',
         'Управляйте онлайн-частью вашего прокатного бизнеса.'),
    'Car, scooter and boat hire, answered at 2am. Ownerdeck runs the website, the enquiries, the bookings and the follow-up after — so the questions that arrive while you are asleep are already dealt with by morning.':
        ('Ενοικιάσεις αυτοκινήτων, σκούτερ και σκαφών, με απαντήσεις στις 2 τα ξημερώματα. Το Ownerdeck τρέχει την ιστοσελίδα, τα ερωτήματα, τις κρατήσεις και την επικοινωνία μετά — ώστε όσα φτάνουν ενώ κοιμάστε να έχουν ήδη τακτοποιηθεί ως το πρωί.',
         'Прокат авто, скутеров и лодок — с ответами в 2 часа ночи. Ownerdeck управляет сайтом, запросами, бронированиями и последующей связью, так что вопросы, приходящие пока вы спите, к утру уже решены.'),
    'enquiries booked between 9pm and 8am last month, for one car rental operator in Limassol':
        ('ερωτήματα έγιναν κρατήσεις μεταξύ 9 μ.μ. και 8 π.μ. τον περασμένο μήνα, για μία εταιρεία ενοικίασης αυτοκινήτων στη Λεμεσό',
         'запросов превратились в брони между 21:00 и 8:00 в прошлом месяце — у одного проката автомобилей в Лимасоле'),
    'No VAT. No long contract on the entry plan. Works the same way for villas, clinics and salons — see who it is for.':
        ('Χωρίς ΦΠΑ. Χωρίς μακροχρόνιο συμβόλαιο στο εισαγωγικό πακέτο. Λειτουργεί το ίδιο για βίλες, κλινικές και κομμωτήρια — δείτε για ποιους είναι.',
         'Без НДС. Без долгосрочного договора на начальном тарифе. Так же работает для вилл, клиник и салонов — посмотрите, для кого это.'),

    # ---- the six trades added with the new imagery ----
    'Restaurants and tavernas': ('Εστιατόρια και ταβέρνες', 'Рестораны и таверны'),
    'Covers, sittings and the same three questions every evening.':
        ('Κουβέρ, βάρδιες και οι ίδιες τρεις ερωτήσεις κάθε βράδυ.',
         'Посадки, смены и одни и те же три вопроса каждый вечер.'),
    'Watersports rental': ('Ενοικίαση θαλάσσιων σπορ', 'Прокат для водного спорта'),
    'Hourly hires, weather calls and kit back before sunset.':
        ('Ωριαίες ενοικιάσεις, αποφάσεις για τον καιρό και επιστροφή εξοπλισμού πριν τη δύση.',
         'Почасовая аренда, решения по погоде и снаряжение обратно до заката.'),
    'Fitness and yoga studios': ('Γυμναστήρια και στούντιο γιόγκα', 'Фитнес- и йога-студии'),
    'Class times, drop-ins and memberships without a spreadsheet.':
        ('Ώρες μαθημάτων, μεμονωμένες επισκέψεις και συνδρομές χωρίς λογιστικό φύλλο.',
         'Расписание занятий, разовые визиты и абонементы без таблиц.'),
    'Photographers and studios': ('Φωτογράφοι και στούντιο', 'Фотографы и студии'),
    'Shoot dates, packages and deposits agreed before the call.':
        ('Ημερομηνίες λήψης, πακέτα και προκαταβολές συμφωνημένα πριν το τηλεφώνημα.',
         'Даты съёмок, пакеты и депозиты — согласованы ещё до звонка.'),
    'Dentists': ('Οδοντίατροι', 'Стоматологи'),
    'Appointments, first-visit questions and reminders that cut no-shows.':
        ('Ραντεβού, ερωτήσεις πρώτης επίσκεψης και υπενθυμίσεις που μειώνουν τις απουσίες.',
         'Записи, вопросы перед первым визитом и напоминания, снижающие неявки.'),
    'Barbers': ('Κουρεία', 'Барбершопы'),
    'Walk-ins, regulars and a diary that fills itself.':
        ('Περαστικοί, τακτικοί πελάτες και ένα ημερολόγιο που γεμίζει μόνο του.',
         'Клиенты с улицы, постоянные посетители и расписание, которое заполняется само.'),

    # ---- the reply-time metric ----
    # "~2 sec" carries a unit, so it is translated rather than left as a
    # numeral like 212 and 14.
    '~2 sec': ('~2 \u03b4\u03b5\u03c5\u03c4.', '~2 \u0441\u0435\u043a'),
    'assistant reply time': ('\u03c7\u03c1\u03cc\u03bd\u03bf\u03c2 \u03b1\u03c0\u03ac\u03bd\u03c4\u03b7\u03c3\u03b7\u03c2 \u03b2\u03bf\u03b7\u03b8\u03bf\u03cd',
                             '\u0432\u0440\u0435\u043c\u044f \u043e\u0442\u0432\u0435\u0442\u0430 \u0430\u0441\u0441\u0438\u0441\u0442\u0435\u043d\u0442\u0430'),

    # ---- the scroll-expand hero ----
    'While you were asleep.': ('Ενώ κοιμόσασταν.',
                               'Пока вы спали.'),
    'Scroll': ('Κύλιση', 'Прокрутите'),
    'The website answered. You found out later.':
        ('Ο ιστότοπος απάντησε. Το μάθατε αργότερα.',
         'Сайт ответил. Вы узнали позже.'),
    'It quoted from your real prices, checked what was free, and held the car — while the person who owns it was asleep.':
        ('Έδωσε τιμή από τον πραγματικό σας τιμοκατάλογο, έλεγξε τι ήταν ελεύθερο και κράτησε το αυτοκίνητο — ενώ ο ιδιοκτήτης κοιμόταν.',
         'Он назвал цену по вашему реальному прайсу, проверил, что свободно, и закрепил машину — пока владелец спал.'),

    # ---- corrected: the live client's plan, and the notice term ----
    # These two sentences outlived the repricing. The first told a prospect
    # the live client pays 150 a month, on the home page, before they reach
    # the pricing page and read 1,900. The second scoped a month's notice —
    # which applies to every plan — down to the cheapest one.
    'A car rental operator in Limassol, running on Deck. The after-hours coverage booked those 14 enquiries automatically \u2014 ones the owner would otherwise have picked up the next morning, if they were still waiting.':
        ('Ένα γραφείο ενοικίασης αυτοκινήτων στη Λεμεσό, στο Deck. \u0397 \u03ba\u03ac\u03bb\u03c5\u03c8\u03b7 \u03b5\u03ba\u03c4\u03cc\u03c2 \u03c9\u03c1\u03b1\u03c1\u03af\u03bf\u03c5 \u03ad\u03ba\u03bb\u03b5\u03b9\u03c3\u03b5 \u03b1\u03c5\u03c4\u03cc\u03bc\u03b1\u03c4\u03b1 \u03b1\u03c5\u03c4\u03ac \u03c4\u03b1 14 \u03b5\u03c1\u03c9\u03c4\u03ae\u03bc\u03b1\u03c4\u03b1 \u2014 \u03b1\u03c5\u03c4\u03ac \u03c0\u03bf\u03c5 \u03b1\u03bb\u03bb\u03b9\u03ce\u03c2 \u03b8\u03b1 \u03ad\u03c0\u03b9\u03b1\u03bd\u03b5 \u03bf \u03b9\u03b4\u03b9\u03bf\u03ba\u03c4\u03ae\u03c4\u03b7\u03c2 \u03c4\u03bf \u03b5\u03c0\u03cc\u03bc\u03b5\u03bd\u03bf \u03c0\u03c1\u03c9\u03af, \u03b1\u03bd \u03c0\u03b5\u03c1\u03af\u03bc\u03b5\u03bd\u03b1\u03bd \u03b1\u03ba\u03cc\u03bc\u03b1.',
         'Прокат автомобилей в Лимассоле, на тарифе Deck. \u041d\u043e\u0447\u043d\u043e\u0435 \u043f\u043e\u043a\u0440\u044b\u0442\u0438\u0435 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0437\u0430\u043a\u0440\u044b\u043b\u043e \u044d\u0442\u0438 14 \u0437\u0430\u043f\u0440\u043e\u0441\u043e\u0432 \u2014 \u0442\u0435, \u0447\u0442\u043e \u0438\u043d\u0430\u0447\u0435 \u0432\u043b\u0430\u0434\u0435\u043b\u0435\u0446 \u0432\u0437\u044f\u043b \u0431\u044b \u0443\u0442\u0440\u043e\u043c, \u0435\u0441\u043b\u0438 \u0431\u044b \u043e\u043d\u0438 \u0435\u0449\u0451 \u0436\u0434\u0430\u043b\u0438.'),
    'A car rental operator in Limassol, running on Deck. Those 14 were booked while the owner was asleep.':
        ('Ένα γραφείο ενοικίασης αυτοκινήτων στη Λεμεσό, στο Deck. \u0391\u03c5\u03c4\u03ad\u03c2 \u03bf\u03b9 14 \u03ba\u03bb\u03b5\u03af\u03c3\u03c4\u03b7\u03ba\u03b1\u03bd \u03b5\u03bd\u03ce \u03bf \u03b9\u03b4\u03b9\u03bf\u03ba\u03c4\u03ae\u03c4\u03b7\u03c2 \u03ba\u03bf\u03b9\u03bc\u03cc\u03c4\u03b1\u03bd.',
         'Прокат автомобилей в Лимассоле, на тарифе Deck. \u042d\u0442\u0438 14 \u0437\u0430\u0431\u0440\u043e\u043d\u0438\u0440\u043e\u0432\u0430\u043b\u0438\u0441\u044c, \u043f\u043e\u043a\u0430 \u0432\u043b\u0430\u0434\u0435\u043b\u0435\u0446 \u0441\u043f\u0430\u043b.'),
    'No VAT. Stop any plan with a month\u2019s notice.':
        ('\u03a7\u03c9\u03c1\u03af\u03c2 \u03a6\u03a0\u0391. \u0394\u03b9\u03b1\u03ba\u03cc\u03c8\u03c4\u03b5 \u03bf\u03c0\u03bf\u03b9\u03bf\u03b4\u03ae\u03c0\u03bf\u03c4\u03b5 \u03c0\u03b1\u03ba\u03ad\u03c4\u03bf \u03bc\u03b5 \u03c0\u03c1\u03bf\u03b5\u03b9\u03b4\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7 \u03b5\u03bd\u03cc\u03c2 \u03bc\u03ae\u03bd\u03b1.',
         '\u0411\u0435\u0437 \u041d\u0414\u0421. \u041e\u0442\u043a\u0430\u0437\u0430\u0442\u044c\u0441\u044f \u043e\u0442 \u043b\u044e\u0431\u043e\u0433\u043e \u0442\u0430\u0440\u0438\u0444\u0430 \u043c\u043e\u0436\u043d\u043e, \u043f\u0440\u0435\u0434\u0443\u043f\u0440\u0435\u0434\u0438\u0432 \u0437\u0430 \u043c\u0435\u0441\u044f\u0446.'),
    'No VAT. Stop any plan with a month\u2019s notice. Works the same way for villas, clinics and salons \u2014 see who it is for.':
        ('\u03a7\u03c9\u03c1\u03af\u03c2 \u03a6\u03a0\u0391. \u0394\u03b9\u03b1\u03ba\u03cc\u03c8\u03c4\u03b5 \u03bf\u03c0\u03bf\u03b9\u03bf\u03b4\u03ae\u03c0\u03bf\u03c4\u03b5 \u03c0\u03b1\u03ba\u03ad\u03c4\u03bf \u03bc\u03b5 \u03c0\u03c1\u03bf\u03b5\u03b9\u03b4\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7 \u03b5\u03bd\u03cc\u03c2 \u03bc\u03ae\u03bd\u03b1. \u039b\u03b5\u03b9\u03c4\u03bf\u03c5\u03c1\u03b3\u03b5\u03af \u03b1\u03ba\u03c1\u03b9\u03b2\u03ce\u03c2 \u03ad\u03c4\u03c3\u03b9 \u03ba\u03b1\u03b9 \u03b3\u03b9\u03b1 \u03b2\u03af\u03bb\u03b5\u03c2, \u03ba\u03bb\u03b9\u03bd\u03b9\u03ba\u03ad\u03c2 \u03ba\u03b1\u03b9 \u03ba\u03bf\u03bc\u03bc\u03c9\u03c4\u03ae\u03c1\u03b9\u03b1 \u2014 \u03b4\u03b5\u03af\u03c4\u03b5 \u03b3\u03b9\u03b1 \u03c0\u03bf\u03b9\u03bf\u03cd\u03c2 \u03b5\u03af\u03bd\u03b1\u03b9.',
         '\u0411\u0435\u0437 \u041d\u0414\u0421. \u041e\u0442\u043a\u0430\u0437\u0430\u0442\u044c\u0441\u044f \u043e\u0442 \u043b\u044e\u0431\u043e\u0433\u043e \u0442\u0430\u0440\u0438\u0444\u0430 \u043c\u043e\u0436\u043d\u043e, \u043f\u0440\u0435\u0434\u0443\u043f\u0440\u0435\u0434\u0438\u0432 \u0437\u0430 \u043c\u0435\u0441\u044f\u0446. \u0422\u0430\u043a \u0436\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u0434\u043b\u044f \u0432\u0438\u043b\u043b, \u043a\u043b\u0438\u043d\u0438\u043a \u0438 \u0441\u0430\u043b\u043e\u043d\u043e\u0432 \u2014 \u0441\u043c\u043e\u0442\u0440\u0438\u0442\u0435, \u0434\u043b\u044f \u043a\u043e\u0433\u043e \u044d\u0442\u043e.'),

    # ---- the funnel's sectors ----
    'Vehicle and equipment rental':
        ('Ενοικιάσεις οχημάτων και εξοπλισμού',
         'Аренда транспорта и оборудования'),
    'Boats and watersports':
        ('Σκάφη και θαλάσσια σπορ',
         'Лодки и водный спорт'),
    'Tours and activities':
        ('Εκδρομές και δραστηριότητες',
         'Экскурсии и активности'),
    'Places to stay':
        ('Καταλύματα',
         'Жильё для гостей'),
    'Property and lettings':
        ('Ακίνητα και ενοικιάσεις',
         'Недвижимость и аренда'),
    'Clinics and health':
        ('Κλινικές και υγεία',
         'Клиники и здоровье'),
    'Salons and grooming':
        ('Κομμωτήρια και περιποίηση',
         'Салоны и уход'),
    'Fitness and wellbeing':
        ('Γυμναστήρια και ευεξία',
         'Фитнес и здоровый образ жизни'),
    'Food and drink':
        ('Φαγητό και ποτό',
         'Еда и напитки'),
    'Trades and home services':
        ('Τεχνίτες και υπηρεσίες σπιτιού',
         'Мастера и услуги для дома'),
    'Professional services':
        ('Επαγγελματικές υπηρεσίες',
         'Профессиональные услуги'),
    'So the quote is about your work rather than a generic package. If none of these is quite it, pick the closest and tell us at the end.':
        ('Ώστε η προσφορά να αφορά τη δουλειά σας και όχι ένα γενικό πακέτο. Αν κανένα δεν ταιριάζει ακριβώς, διαλέξτε το πιο κοντινό και πείτε μας στο τέλος.',
         'Чтобы расчёт был про вашу работу, а не про типовой пакет. Если ничто не подходит точно, выберите ближайшее и скажите нам в конце.'),

    # ---- the reworked hero and funnel copy ----
    'Answered at 2am, booked by morning.':
        ('\u0391\u03c0\u03ac\u03bd\u03c4\u03b7\u03c3\u03b7 \u03c3\u03c4\u03b9\u03c2 2 \u03c4\u03b1 \u03be\u03b7\u03bc\u03b5\u03c1\u03ce\u03bc\u03b1\u03c4\u03b1, \u03ba\u03c1\u03ac\u03c4\u03b7\u03c3\u03b7 \u03bc\u03ad\u03c7\u03c1\u03b9 \u03c4\u03bf \u03c0\u03c1\u03c9\u03af.',
         '\u041e\u0442\u0432\u0435\u0442 \u0432 \u0434\u0432\u0430 \u043d\u043e\u0447\u0438, \u0431\u0440\u043e\u043d\u044c \u043a \u0443\u0442\u0440\u0443.'),
    'Car, scooter and boat hire. Ownerdeck runs the online side of your rental business \u2014 the website, the enquiries, the bookings and the follow-up after \u2014 so the questions that arrive while you are asleep are already dealt with.':
        ('\u0395\u03bd\u03bf\u03b9\u03ba\u03b9\u03ac\u03c3\u03b5\u03b9\u03c2 \u03b1\u03c5\u03c4\u03bf\u03ba\u03b9\u03bd\u03ae\u03c4\u03c9\u03bd, \u03bc\u03b7\u03c7\u03b1\u03bd\u03ce\u03bd \u03ba\u03b1\u03b9 \u03c3\u03ba\u03b1\u03c6\u03ce\u03bd. \u03a4\u03bf Ownerdeck \u03c4\u03c1\u03ad\u03c7\u03b5\u03b9 \u03c4\u03b7\u03bd \u03bf\u03bd\u03bb\u03ac\u03b9\u03bd \u03c0\u03bb\u03b5\u03c5\u03c1\u03ac \u03c4\u03b7\u03c2 \u03b5\u03c0\u03b9\u03c7\u03b5\u03af\u03c1\u03b7\u03c3\u03ae\u03c2 \u03c3\u03b1\u03c2 \u2014 \u03c4\u03bf\u03bd \u03b9\u03c3\u03c4\u03cc\u03c4\u03bf\u03c0\u03bf, \u03c4\u03b1 \u03bc\u03b7\u03bd\u03cd\u03bc\u03b1\u03c4\u03b1, \u03c4\u03b9\u03c2 \u03ba\u03c1\u03b1\u03c4\u03ae\u03c3\u03b5\u03b9\u03c2 \u03ba\u03b1\u03b9 \u03c4\u03b7 \u03c3\u03c5\u03bd\u03ad\u03c7\u03b5\u03b9\u03b1 \u2014 \u03ce\u03c3\u03c4\u03b5 \u03cc\u03c3\u03b1 \u03ad\u03c1\u03c7\u03bf\u03bd\u03c4\u03b1\u03b9 \u03b5\u03bd\u03ce \u03ba\u03bf\u03b9\u03bc\u03ac\u03c3\u03c4\u03b5 \u03bd\u03b1 \u03ad\u03c7\u03bf\u03c5\u03bd \u03ae\u03b4\u03b7 \u03bb\u03c5\u03b8\u03b5\u03af.',
         '\u0410\u0440\u0435\u043d\u0434\u0430 \u0430\u0432\u0442\u043e, \u0441\u043a\u0443\u0442\u0435\u0440\u043e\u0432 \u0438 \u043b\u043e\u0434\u043e\u043a. Ownerdeck \u0432\u0435\u0434\u0451\u0442 \u043e\u043d\u043b\u0430\u0439\u043d-\u0447\u0430\u0441\u0442\u044c \u0432\u0430\u0448\u0435\u0433\u043e \u0431\u0438\u0437\u043d\u0435\u0441\u0430 \u2014 \u0441\u0430\u0439\u0442, \u0437\u0430\u043f\u0440\u043e\u0441\u044b, \u0431\u0440\u043e\u043d\u0438 \u0438 \u0432\u0441\u0451, \u0447\u0442\u043e \u0438\u0434\u0451\u0442 \u043f\u043e\u0441\u043b\u0435, \u2014 \u0447\u0442\u043e\u0431\u044b \u0432\u043e\u043f\u0440\u043e\u0441\u044b, \u043f\u0440\u0438\u0448\u0435\u0434\u0448\u0438\u0435 \u043d\u043e\u0447\u044c\u044e, \u0431\u044b\u043b\u0438 \u0443\u0436\u0435 \u0440\u0435\u0448\u0435\u043d\u044b.'),
    'Watch it take a booking': ('\u0394\u03b5\u03af\u03c4\u03b5 \u03c4\u03bf \u03bd\u03b1 \u03ba\u03bb\u03b5\u03af\u03bd\u03b5\u03b9 \u03ba\u03c1\u03ac\u03c4\u03b7\u03c3\u03b7',
                               '\u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c, \u043a\u0430\u043a \u043e\u043d \u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0435\u0442 \u0431\u0440\u043e\u043d\u044c'),
    'Now live': ('\u03a3\u03b5 \u03bb\u03b5\u03b9\u03c4\u03bf\u03c5\u03c1\u03b3\u03af\u03b1', '\u0421\u0435\u0439\u0447\u0430\u0441 \u0432 \u0440\u0430\u0431\u043e\u0442\u0435'),
    'Not sure? Pick the middle one \u2014 we will tell you honestly if you need less. Nothing is charged here; at the end you can hold your slot with a \u20ac75 deposit if you want to, refundable until work starts.':
        ('\u0394\u03b5\u03bd \u03b5\u03af\u03c3\u03c4\u03b5 \u03c3\u03af\u03b3\u03bf\u03c5\u03c1\u03bf\u03b9; \u0394\u03b9\u03b1\u03bb\u03ad\u03be\u03c4\u03b5 \u03c4\u03bf \u03bc\u03b5\u03c3\u03b1\u03af\u03bf \u2014 \u03b8\u03b1 \u03c3\u03b1\u03c2 \u03c0\u03bf\u03cd\u03bc\u03b5 \u03b5\u03b9\u03bb\u03b9\u03ba\u03c1\u03b9\u03bd\u03ac \u03b1\u03bd \u03c7\u03c1\u03b5\u03b9\u03ac\u03b6\u03b5\u03c3\u03c4\u03b5 \u03bb\u03b9\u03b3\u03cc\u03c4\u03b5\u03c1\u03b1. \u0395\u03b4\u03ce \u03b4\u03b5\u03bd \u03c7\u03c1\u03b5\u03ce\u03bd\u03b5\u03c4\u03b1\u03b9 \u03c4\u03af\u03c0\u03bf\u03c4\u03b1\u00b7 \u03c3\u03c4\u03bf \u03c4\u03ad\u03bb\u03bf\u03c2 \u03bc\u03c0\u03bf\u03c1\u03b5\u03af\u03c4\u03b5 \u03bd\u03b1 \u03ba\u03c1\u03b1\u03c4\u03ae\u03c3\u03b5\u03c4\u03b5 \u03c4\u03b7 \u03b8\u03ad\u03c3\u03b7 \u03c3\u03b1\u03c2 \u03bc\u03b5 \u03c0\u03c1\u03bf\u03ba\u03b1\u03c4\u03b1\u03b2\u03bf\u03bb\u03ae \u20ac75, \u03b5\u03c0\u03b9\u03c3\u03c4\u03c1\u03b5\u03c0\u03c4\u03ad\u03b1 \u03bc\u03ad\u03c7\u03c1\u03b9 \u03bd\u03b1 \u03be\u03b5\u03ba\u03b9\u03bd\u03ae\u03c3\u03b5\u03b9 \u03b7 \u03b4\u03bf\u03c5\u03bb\u03b5\u03b9\u03ac.',
         '\u041d\u0435 \u0443\u0432\u0435\u0440\u0435\u043d\u044b? \u0412\u043e\u0437\u044c\u043c\u0438\u0442\u0435 \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u2014 \u043c\u044b \u0447\u0435\u0441\u0442\u043d\u043e \u0441\u043a\u0430\u0436\u0435\u043c, \u0435\u0441\u043b\u0438 \u0432\u0430\u043c \u043d\u0443\u0436\u043d\u043e \u043c\u0435\u043d\u044c\u0448\u0435. \u0417\u0434\u0435\u0441\u044c \u043d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u0441\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u0442\u0441\u044f; \u0432 \u043a\u043e\u043d\u0446\u0435 \u043c\u043e\u0436\u043d\u043e \u0437\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u044c \u043c\u0435\u0441\u0442\u043e \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u043c \u20ac75 \u2014 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u043d\u044b\u043c, \u043f\u043e\u043a\u0430 \u0440\u0430\u0431\u043e\u0442\u0430 \u043d\u0435 \u043d\u0430\u0447\u0430\u043b\u0430\u0441\u044c.'),

    # ---- the live operator card ----
    'Live &middot; Limassol': ('Ζωντανά &middot; Λεμεσός',
                              'Онлайн &middot; Лимассол'),
    'Last 30 days': ('Τελευταίες 30 μέρες',
                     'Последние 30 дней'),
    'Operators live': ('Ενεργοί πελάτες',
                       'Активных клиентов'),
    'Channel': ('Κανάλι', 'Канал'),
    'Status': ('Κατάσταση', 'Статус'),
    'Running': ('Ενεργό', 'Работает'),

    # ---- the hero proof strip ----
    # These were written straight into lang/*.json, which _translate.py
    # regenerates, so they vanished on the next run. Kept here instead.
    'enquiries answered': ('ερωτήματα απαντήθηκαν',
                           'запросов обработано'),
    'after-hours bookings': ('κρατήσεις εκτός ωραρίου',
                             'броней после рабочего времени'),
    'average reply time': ('μέσος χρόνος απάντησης',
                           'среднее время ответа'),
    'Last 30 days &middot; one live car rental operator in Limassol':
        ('Τελευταίες 30 μέρες &middot; μία εν λειτουργία εταιρεία ενοικίασης αυτοκινήτων στη Λεμεσό',
         'Последние 30 дней &middot; один действующий прокат автомобилей в Лимассоле'),

    # ---- the chat mock, now on what-we-build ----
    'Answer, in practice': ('Η απάντηση, στην πράξη',
                            'Ответ на практике'),
    'Two in the morning, a question about a jeep, and a held booking by the time you wake up. No template and no menu of options — it read the question and answered from your prices.':
        ('Δύο τα ξημερώματα, μια ερώτηση για ένα τζιπ και μια κρατημένη κράτηση μέχρι να ξυπνήσετε. Χωρίς έτοιμο κείμενο και χωρίς μενού επιλογών — διάβασε την ερώτηση και απάντησε από τις δικές σας τιμές.',
         'Два часа ночи, вопрос про джип — и готовая бронь к вашему пробуждению. Никаких шаблонов и никакого меню — он прочёл вопрос и ответил по вашим ценам.'),

    # ---- the payback calculator ----
    'The only number that matters': ('Ο μόνος αριθμός που μετράει',
                                     'Единственное число, которое имеет значение'),
    'How many bookings pay for it?': ('Πόσες κρατήσεις το πληρώνουν;',
                                      'Сколько бронирований его окупают?'),
    'Not what it costs. What it has to earn back. Drag your average booking and see.':
        ('Όχι πόσο κοστίζει. Πόσα πρέπει να επιστρέψει. Σύρετε τη μέση κράτησή σας και δείτε.',
         'Не сколько это стоит, а сколько должно вернуть. Подвиньте среднюю бронь и посмотрите.'),
    'Your average booking': ('Η μέση κράτησή σας', 'Ваша средняя бронь'),
    'Plan': ('Πακέτο', 'Тариф'),
    'bookings a month covers it.': ('κρατήσεις τον μήνα το καλύπτουν.',
                                    'бронирования в месяц покрывают это.'),
    'Your own average, your own plan. It does not count the enquiries you were already going to answer yourself &mdash; only the ones that would otherwise have waited until morning.':
        ('Ο δικός σας μέσος όρος, το δικό σας πακέτο. Δεν μετρά τα ερωτήματα που θα απαντούσατε ούτως ή άλλως μόνοι σας — μόνο εκείνα που αλλιώς θα περίμεναν ως το πρωί.',
         'Ваш собственный средний чек и ваш тариф. Здесь не учтены запросы, на которые вы и так ответили бы сами, — только те, что иначе ждали бы до утра.'),

    # ---- the objection everyone thinks and nobody answers ----
    'Why not just use ChatGPT?': ('Γιατί όχι απλώς ChatGPT;', 'Почему не просто ChatGPT?'),
    'Because ChatGPT does not know whether the Jimny is free on Saturday. It writes a convincing sentence about your prices without having seen them. Ownerdeck answers from your database — the actual fleet, the actual rates, the actual calendar — and when it does not know, it says so and passes the conversation to you. The writing is the easy part. Being right is the product.':
        ('Επειδή το ChatGPT δεν ξέρει αν το Jimny είναι ελεύθερο το Σάββατο. Γράφει μια πειστική πρόταση για τις τιμές σας χωρίς να τις έχει δει ποτέ. Το Ownerdeck απαντά από τη βάση δεδομένων σας — τον πραγματικό στόλο, τις πραγματικές τιμές, το πραγματικό ημερολόγιο — και όταν δεν ξέρει, το λέει και σας παραδίδει τη συνομιλία. Το γράψιμο είναι το εύκολο μέρος. Το προϊόν είναι να έχει δίκιο.',
         'Потому что ChatGPT не знает, свободен ли Jimny в субботу. Он напишет убедительное предложение о ваших ценах, ни разу их не увидев. Ownerdeck отвечает из вашей базы данных — реальный автопарк, реальные тарифы, реальный календарь, — а когда не знает, говорит об этом и передаёт разговор вам. Написать текст — простая часть. Продукт в том, чтобы быть правым.'),
    'See it work': ('Δείτε το να δουλεύει', 'Посмотреть в работе'),

    # ---- who it's for ----
    'Built for businesses that run on bookings.':
        ('Φτιαγμένο για επιχειρήσεις που ζουν από κρατήσεις.',
         'Создано для бизнесов, которые живут за счёт броней.'),
    'If your customers ask what it costs, whether it is free, and can they have it tomorrow — this is built for you. The trade changes, the questions do not.':
        ('Αν οι πελάτες σας ρωτούν πόσο κοστίζει, αν είναι ελεύθερο και αν μπορούν να το έχουν αύριο — αυτό είναι φτιαγμένο για εσάς. Το επάγγελμα αλλάζει, οι ερωτήσεις όχι.',
         'Если ваши клиенты спрашивают, сколько это стоит, свободно ли это и можно ли завтра — это создано для вас. Отрасль меняется, вопросы — нет.'),
    'Car and 4x4 rental': ('Ενοικίαση αυτοκινήτων και 4x4', 'Аренда автомобилей и внедорожников'),
    'Fleet, day rates, insurance and delivery, all answered from one price list.':
        ('Στόλος, ημερήσιες τιμές, ασφάλεια και παράδοση, όλα απαντημένα από έναν τιμοκατάλογο.',
         'Автопарк, дневные тарифы, страховка и доставка — всё из одного прайс-листа.'),
    'Scooter and bike hire': ('Ενοικίαση σκούτερ και ποδηλάτων', 'Прокат скутеров и велосипедов'),
    'Walk-ups and day hires without the phone ringing all afternoon.':
        ('Περαστικοί και ημερήσιες ενοικιάσεις χωρίς να χτυπά το τηλέφωνο όλο το απόγευμα.',
         'Клиенты с улицы и дневная аренда — без звонков весь день.'),
    'Boat and jetski charter': ('Ναύλωση σκαφών και jetski', 'Аренда лодок и гидроциклов'),
    'Half-day and full-day slots, weather holds, deposits taken up front.':
        ('Μισής και ολόκληρης ημέρας θέσεις, αναβολές λόγω καιρού, προκαταβολές εκ των προτέρων.',
         'Слоты на полдня и день, отмены из-за погоды, депозиты вперёд.'),
    'Tours, excursions and diving': ('Εκδρομές, ξεναγήσεις και καταδύσεις',
                                     'Туры, экскурсии и дайвинг'),
    'Group sizes, pick-up points and departure times that stay in step.':
        ('Μεγέθη ομάδων, σημεία παραλαβής και ώρες αναχώρησης που μένουν συγχρονισμένα.',
         'Размеры групп, точки сбора и время отправления — всегда согласованы.'),
    'Villas and short-term rentals': ('Βίλες και βραχυχρόνιες μισθώσεις',
                                      'Виллы и краткосрочная аренда'),
    'Nightly rates by season, minimum stays and availability that is actually true.':
        ('Τιμές ανά διανυκτέρευση κατά σεζόν, ελάχιστες διαμονές και διαθεσιμότητα που ισχύει πραγματικά.',
         'Цены за ночь по сезонам, минимальный срок и доступность, которая действительно верна.'),
    'Guesthouses and small hotels': ('Ξενώνες και μικρά ξενοδοχεία',
                                     'Гостевые дома и небольшие отели'),
    'Room types, breakfast, late check-out — asked and answered at 2am.':
        ('Τύποι δωματίων, πρωινό, αργό check-out — ερωτήσεις και απαντήσεις στις 2 τα ξημερώματα.',
         'Типы номеров, завтрак, поздний выезд — спрошено и отвечено в 2 часа ночи.'),
    'Estate agencies': ('Κτηματομεσιτικά γραφεία', 'Агентства недвижимости'),
    'Listings that stay current and viewings booked without the back and forth.':
        ('Αγγελίες που μένουν ενημερωμένες και ραντεβού που κλείνονται χωρίς πέρα δώθε.',
         'Объявления остаются актуальными, а просмотры бронируются без долгой переписки.'),
    'Private clinics': ('Ιδιωτικές κλινικές', 'Частные клиники'),
    'Appointment slots, first-visit questions and reminders that cut no-shows.':
        ('Ραντεβού, ερωτήσεις πρώτης επίσκεψης και υπενθυμίσεις που μειώνουν τις απουσίες.',
         'Слоты приёма, вопросы перед первым визитом и напоминания, снижающие неявки.'),
    'Salons and spas': ('Κομμωτήρια και σπα', 'Салоны и спа'),
    'Treatments, durations and prices, with the diary kept full.':
        ('Θεραπείες, διάρκειες και τιμές, με το ημερολόγιο πάντα γεμάτο.',
         'Процедуры, длительность и цены, с постоянно заполненным расписанием.'),
    'Not on the list? If your business takes bookings or answers the same questions all day, it will fit. Ask us.':
        ('Δεν είστε στη λίστα; Αν η επιχείρησή σας δέχεται κρατήσεις ή απαντά τις ίδιες ερωτήσεις όλη μέρα, ταιριάζει. Ρωτήστε μας.',
         'Вас нет в списке? Если ваш бизнес принимает брони или весь день отвечает на одни и те же вопросы — подойдёт. Спросите нас.'),

    # ---- questions ----
    'Everything owners ask.': ('Όλα όσα ρωτούν οι ιδιοκτήτες.', 'Всё, о чём спрашивают владельцы.'),
    'If yours is not here, message us — it probably belongs on this page.':
        ('Αν η δική σας δεν είναι εδώ, στείλτε μας μήνυμα — μάλλον ανήκει σε αυτή τη σελίδα.',
         'Если вашего вопроса тут нет, напишите нам — вероятно, ему здесь самое место.'),
    'I already have a website. Do I have to replace it?':
        ('Έχω ήδη ιστοσελίδα. Πρέπει να την αντικαταστήσω;',
         'У меня уже есть сайт. Обязательно ли его менять?'),
    'No. If you are happy with it, we can point the assistant at it and leave it alone. But if it is out of date and nobody can edit it, replacing it is usually cheaper than maintaining it.':
        ('Όχι. Αν σας ικανοποιεί, μπορούμε να στρέψουμε τον βοηθό σε αυτήν και να την αφήσουμε ως έχει. Αλλά αν είναι ξεπερασμένη και κανείς δεν μπορεί να την επεξεργαστεί, η αντικατάσταση συνήθως κοστίζει λιγότερο από τη συντήρηση.',
         'Нет. Если он вас устраивает, мы направим на него ассистента и не будем его трогать. Но если он устарел и никто не может его редактировать, заменить обычно дешевле, чем поддерживать.'),
    'Do I need a new phone number?': ('Χρειάζομαι νέο αριθμό τηλεφώνου;',
                                      'Нужен ли新 новый номер телефона?'),
    'No. The assistant runs on your existing WhatsApp Business number. Your customers keep messaging the number they already have.':
        ('Όχι. Ο βοηθός τρέχει στον υπάρχοντα αριθμό σας WhatsApp Business. Οι πελάτες σας συνεχίζουν να γράφουν στον αριθμό που ήδη έχουν.',
         'Нет. Ассистент работает на вашем существующем номере WhatsApp Business. Клиенты продолжают писать на тот же номер.'),
    'What happens when it does not know the answer?':
        ('Τι γίνεται όταν δεν ξέρει την απάντηση;', 'Что происходит, если он не знает ответа?'),
    'It says so and hands the conversation to you, with everything the customer already said. It never guesses at a price or an availability.':
        ('Το λέει και σας παραδίδει τη συνομιλία, μαζί με όλα όσα έχει ήδη πει ο πελάτης. Ποτέ δεν μαντεύει τιμή ή διαθεσιμότητα.',
         'Он так и говорит и передаёт вам разговор вместе со всем, что уже сказал клиент. Он никогда не угадывает цену или доступность.'),
    'Can I take over a conversation?': ('Μπορώ να αναλάβω μια συνομιλία;',
                                        'Могу ли я взять разговор на себя?'),
    'At any time. You reply from your own phone and the assistant steps back for that conversation.':
        ('Οποιαδήποτε στιγμή. Απαντάτε από το δικό σας κινητό και ο βοηθός αποσύρεται για εκείνη τη συνομιλία.',
         'В любой момент. Вы отвечаете со своего телефона, и ассистент отступает в этом разговоре.'),
    'What languages does it answer in?': ('Σε ποιες γλώσσες απαντά;',
                                          'На каких языках он отвечает?'),
    'Whatever the customer writes in. It reads the message, answers in the same language, and your prices stay the same in all of them.':
        ('Σε όποια γράφει ο πελάτης. Διαβάζει το μήνυμα, απαντά στην ίδια γλώσσα, και οι τιμές σας μένουν ίδιες σε όλες.',
         'На том, на котором пишет клиент. Он читает сообщение, отвечает на том же языке, а ваши цены везде одинаковы.'),
    'Who owns the website and the data?': ('Ποιος έχει την ιστοσελίδα και τα δεδομένα;',
                                           'Кому принадлежат сайт и данные?'),
    'You do. The site, the database and the phone number are yours. If you leave, we hand over the site files and an export of your data.':
        ('Εσείς. Η ιστοσελίδα, η βάση δεδομένων και ο αριθμός τηλεφώνου είναι δικά σας. Αν φύγετε, παραδίδουμε τα αρχεία της ιστοσελίδας και εξαγωγή των δεδομένων σας.',
         'Вам. Сайт, база данных и номер телефона — ваши. Если вы уходите, мы передаём файлы сайта и выгрузку ваших данных.'),
    'How long does it take to go live?': ('Πόσο χρόνο παίρνει για να βγει ζωντανά;',
                                          'Сколько времени до запуска?'),
    'About a week for the Deck, less for Answer. The slow part is usually waiting on photos and a decision about prices.':
        ('Περίπου μία εβδομάδα για το Deck, λιγότερο για το Answer. Το αργό κομμάτι είναι συνήθως η αναμονή για φωτογραφίες και μια απόφαση για τις τιμές.',
         'Около недели для Deck, меньше для Answer. Дольше всего обычно ждём фотографии и решение по ценам.'),
    'I am not technical. Is that a problem?': ('Δεν είμαι τεχνικός. Είναι πρόβλημα;',
                                               'Я не технарь. Это проблема?'),
    'No. Everything you need to change day to day is a form with words on it, and if you would rather not, you message us and we change it.':
        ('Όχι. Ό,τι χρειάζεται να αλλάζετε καθημερινά είναι μια φόρμα με λέξεις, και αν προτιμάτε, μας στέλνετε μήνυμα και το αλλάζουμε εμείς.',
         'Нет. Всё, что нужно менять изо дня в день, — это форма со словами, а если не хотите, напишите нам, и мы изменим сами.'),
    'Do you work outside Cyprus?': ('Δουλεύετε εκτός Κύπρου;', 'Вы работаете за пределами Кипра?'),
    'Yes. Everything is remote and the assistant does not care where it runs. Most clients are in Cyprus because that is where we are.':
        ('Ναι. Όλα γίνονται εξ αποστάσεως και στον βοηθό δεν έχει σημασία πού τρέχει. Οι περισσότεροι πελάτες είναι στην Κύπρο επειδή εκεί είμαστε κι εμείς.',
         'Да. Всё удалённо, и ассистенту всё равно, где он работает. Большинство клиентов на Кипре просто потому, что мы здесь.'),
    'What if the assistant gets something wrong?': ('Κι αν ο βοηθός κάνει λάθος;',
                                                    'А если ассистент ошибётся?'),
    'Tell us and we fix the facts it read from, so it cannot get the same thing wrong twice. It answers from your database, so a wrong answer is almost always a wrong entry.':
        ('Πείτε μας και διορθώνουμε τα δεδομένα από τα οποία διάβασε, ώστε να μην ξανακάνει το ίδιο λάθος. Απαντά από τη βάση δεδομένων σας, οπότε μια λάθος απάντηση είναι σχεδόν πάντα μια λάθος καταχώριση.',
         'Скажите нам, и мы исправим данные, из которых он читал, чтобы та же ошибка не повторилась. Он отвечает из вашей базы, поэтому неверный ответ почти всегда означает неверную запись.'),
    'Is my customers&rsquo; data safe?': ('Είναι ασφαλή τα δεδομένα των πελατών μου;',
                                          'В безопасности ли данные моих клиентов?'),
    'Conversations are processed to answer them and stored so you can read your own history. We do not sell data or use it to advertise. The privacy notice sets out exactly who processes what.':
        ('Οι συνομιλίες επεξεργάζονται για να απαντηθούν και αποθηκεύονται ώστε να διαβάζετε το ιστορικό σας. Δεν πουλάμε δεδομένα ούτε τα χρησιμοποιούμε για διαφήμιση. Η δήλωση απορρήτου ορίζει ακριβώς ποιος επεξεργάζεται τι.',
         'Разговоры обрабатываются, чтобы на них ответить, и сохраняются, чтобы вы могли читать свою историю. Мы не продаём данные и не используем их для рекламы. В политике конфиденциальности указано, кто именно что обрабатывает.'),
    'Can I start small and add later?': ('Μπορώ να ξεκινήσω μικρά και να προσθέσω αργότερα;',
                                         'Могу ли я начать с малого и добавить позже?'),
    'That is the point of the deck. Start with Answer, add Book when the bookings get heavy, add Reach and Return when you want the quiet months filled.':
        ('Αυτό ακριβώς είναι το νόημα της τράπουλας. Ξεκινήστε με το Answer, προσθέστε το Book όταν οι κρατήσεις πυκνώσουν, προσθέστε Reach και Return όταν θέλετε να γεμίσουν οι ήσυχοι μήνες.',
         'В этом и смысл колоды. Начните с Answer, добавьте Book, когда броней станет много, добавьте Reach и Return, когда захотите заполнить тихие месяцы.'),

    # ---- call to action ----
    'Set it once. Let it run.': ('Ρυθμίστε το μία φορά. Αφήστε το να τρέχει.',
                                 'Настройте один раз. Пусть работает.'),
    'Tell us about your business and we will show you exactly how Ownerdeck would handle your website, your messages and your bookings.':
        ('Πείτε μας για την επιχείρησή σας και θα σας δείξουμε ακριβώς πώς θα χειριζόταν το Ownerdeck την ιστοσελίδα, τα μηνύματα και τις κρατήσεις σας.',
         'Расскажите о своём бизнесе, и мы покажем, как именно Ownerdeck справится с вашим сайтом, сообщениями и бронированиями.'),
}


# demo.js and chat-widget.js build their own DOM after the page has loaded and
# ask for translations by key directly. Those keys never appear in the markup,
# so _en_source.json does not know about them and a naive regenerate deletes
# them. Scan the scripts and carry their keys across untouched.
SCRIPTED = ['demo.js', 'chat-widget.js']


def scripted_keys():
    keys = set()
    for name in SCRIPTED:
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            with io.open(path, encoding='utf-8') as f:
                # No word boundaries needed: the key format is distinctive.
                keys |= set(re.findall('k[0-9a-f]{8}', f.read()))
    return keys


def key_for(text):
    return 'k' + hashlib.md5(' '.join(text.split()).encode('utf-8')).hexdigest()[:8]


def main():
    with io.open(os.path.join(HERE, '_en_source.json'), encoding='utf-8') as f:
        source = json.load(f)

    # Index the table by hash so a mismatch is visible rather than silent.
    by_key = {}
    unknown = []
    for en, vals in T.items():
        k = key_for(en)
        if k not in source:
            unknown.append(en)
        by_key[k] = vals

    keep = scripted_keys()
    packs = {}
    for code in LANGS:
        path = os.path.join(HERE, 'lang', code + '.json')
        existing = {}
        if os.path.exists(path):
            with io.open(path, encoding='utf-8') as f:
                existing = json.load(f)
        packs[code] = {k: v for k, v in existing.items() if k in keep}
    missing = []
    for k, en in source.items():
        if k in by_key:
            for i, code in enumerate(LANGS):
                packs[code][k] = decode(by_key[k][i])
        else:
            missing.append(en)

    for code in LANGS:
        path = os.path.join(HERE, 'lang', code + '.json')
        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(packs[code], f, ensure_ascii=False, indent=1, sort_keys=True)
        carried = len([k for k in packs[code] if k in keep])
        print('  lang/%s.json  %d / %d page strings, %d scripted keys carried'
              % (code, len([k for k in packs[code] if k in source]), len(source), carried))

    if unknown:
        print('\n  In the table but no longer on the site (%d) — safe to delete:' % len(unknown))
        for s in unknown[:10]:
            print('    %s' % s[:78])
    if missing:
        print('\n  On the site but not translated (%d):' % len(missing))
        for s in missing[:40]:
            print('    %s' % s[:78])


if __name__ == '__main__':
    main()
