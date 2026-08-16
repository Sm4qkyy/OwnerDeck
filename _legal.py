# The legal pages: notice, privacy, cookies, terms.
#
# Deliberately NOT marked with data-t. These are kept in English and the terms
# say English governs, because a machine translation of a liability clause that
# disagrees with the English one creates exactly the ambiguity the clause is
# there to prevent. The header, footer and navigation around them still
# translate.
#
# Every field the owner has to supply is wrapped in <span class="todo">, which
# renders as a visible dashed box. A registration number that has been invented
# is worse than a gap, so these are meant to be impossible to miss.
#
# This is a careful draft by a non-lawyer. Have it reviewed before relying on
# it commercially.
import re

UPDATED = '15 August 2026'

# A role address, not a personal one. This has to still be read in two years,
# and it appears on a legal notice that outlives any one inbox.
PRIVACY_EMAIL = 'privacy@ownerdeck.com'


def todo(what):
    return '<span class="todo">%s</span>' % what


def no_obfuscate(html):
    """Fence every mailto link against Cloudflare's email obfuscation.

    Cloudflare rewrites mailto links at the edge into a JavaScript-decoded
    placeholder. On a marketing page that is a fair anti-spam trade. On these
    pages it is not: the e-Commerce Directive requires the provider's email
    address to be directly and permanently accessible, and with scripting off
    the rewritten version reads "[email protected]". The email_off comment
    pair is Cloudflare's documented opt-out and is inert everywhere else.
    """
    return re.sub(r'(<a href="mailto:[^"]+">.*?</a>)',
                  r'<!--email_off-->\1<!--email_on-->', html, flags=re.S)


def wrap(slug, nav, title, desc, h1, body):
    body = no_obfuscate(body)
    return dict(
        slug=slug, in_flow=False, legal=True, no_cta=True, no_widget=True, nav=nav,
        title=title, desc=desc,
        head='<meta name="robots" content="index,follow">\n',
        body='''  <div class="wrap measure legal">
    <a class="back" href="/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg> Back to home</a>
    <h1>%s</h1>
    <p class="legal__meta">Last updated %s</p>
%s
  </div>

''' % (h1, UPDATED, body))


IDENTITY = '''    <dl>
      <dt>Service</dt><dd>Ownerdeck</dd>
      <dt>Operated by</dt><dd>%s</dd>
      <dt>Legal form</dt><dd>%s</dd>
      <dt>Registered address</dt><dd>%s</dd>
      <dt>Country</dt><dd>Republic of Cyprus</dd>
      <dt>Email</dt><dd><a href="mailto:%%(email)s">%%(email)s</a></dd>
      <dt>Privacy contact</dt><dd><a href="mailto:%%(privacy)s">%%(privacy)s</a></dd>
      <dt>WhatsApp</dt><dd><a href="%%(wa)s" rel="noopener">Message us</a></dd>
      <dt>VAT</dt><dd>Not registered for VAT. No VAT is charged on any fee.</dd>
    </dl>''' % ('Mark Saade',
                'Sole trader',
                'Livadia, Larnaca, Cyprus')


def pages(EMAIL, WA):
    sub = dict(email=EMAIL, wa=WA, privacy=PRIVACY_EMAIL)
    P = []

    # ------------------------------------------------------- legal notice
    P.append(wrap(
        'legal', 'Legal notice',
        'Legal notice — Ownerdeck',
        'Who operates Ownerdeck, where we are established, and how to reach us.',
        'Legal notice',
        '''    <p>This page is published under the information requirements of Directive 2000/31/EC on electronic commerce, as transposed in the Republic of Cyprus by the Law on Certain Legal Aspects of Information Society Services, in particular Electronic Commerce, of 2004 (156(I)/2004).</p>

    <h2>Who we are</h2>
''' + IDENTITY % sub + '''

    <p class="note">Ownerdeck is listed here as a sole trader, so there is no HE company number.</p>

    <h2>What we do</h2>
    <p>Ownerdeck designs, builds and operates websites, databases, AI chat assistants, booking systems and related online services for small owner-operated businesses. We sell to businesses, not to consumers.</p>

    <h2>Regulated activity</h2>
    <p>None of our services are subject to a licensing or authorisation scheme, and we are not a member of a regulated profession. We do not provide legal, tax, accounting, medical or investment advice, and nothing on this site should be read as any of those.</p>

    <h2>Payments</h2>
    <p>We do not hold or process your customers&rsquo; money. Deposits and payments taken through a system we build run through your own merchant account with your own payment provider.</p>

    <h2>Complaints</h2>
    <p>Write to <a href="mailto:%(email)s">%(email)s</a> and we will reply within five working days. If a dispute cannot be resolved between us, it is subject to the courts of the Republic of Cyprus as set out in our <a href="/terms">terms</a>.</p>
    <p>The European Commission&rsquo;s online dispute resolution platform closed on 20 July 2025 and is no longer available. In any case, it covered consumer contracts, and Ownerdeck contracts with businesses.</p>

    <h2>Responsibility for content</h2>
    <p>We take care that everything on this site is accurate, but prices and descriptions may change. Nothing here is a binding offer until it is confirmed in writing between us. Links to other sites are provided for convenience; we are not responsible for their content.</p>

    <h2>Accessibility</h2>
    <p>This site is built to meet WCAG 2.2 Level AA. It works without JavaScript, without colour alone carrying meaning, and with a keyboard alone. If you hit something you cannot use, email <a href="mailto:%(email)s">%(email)s</a> and we will fix it.</p>
''' % sub))

    # ------------------------------------------------------------ privacy
    P.append(wrap(
        'privacy', 'Privacy',
        'Privacy notice — Ownerdeck',
        'What personal data Ownerdeck handles, why, who processes it, how long '
        'it is kept, and the rights you have under the GDPR.',
        'Privacy notice',
        '''    <p>This notice explains what we do with personal data. It is written to meet Articles 13 and 14 of Regulation (EU) 2016/679 (the GDPR) and the Cyprus Law providing for the Protection of Natural Persons with regard to the Processing of Personal Data of 2018 (125(I)/2018).</p>

    <h2>Two different roles</h2>
    <p>Read this first, because the rest of the notice depends on it.</p>
    <ul>
      <li><b>We are the controller</b> for people who visit this website, message us about our own services, or become our clients. That is the data described below.</li>
      <li><b>We are a processor</b> for the personal data inside a system we run for a client — the enquiries and bookings made by <i>that client&rsquo;s</i> customers. The client is the controller of it, decides what happens to it, and publishes their own privacy notice about it. We only act on their instructions, under a written data processing agreement. If you messaged a business that uses Ownerdeck, ask that business, and we will assist them in answering you.</li>
    </ul>

    <h2>Controller and contact</h2>
''' + IDENTITY % sub + '''
    <p>We are not required to appoint a Data Protection Officer and have not appointed one. Privacy questions go to the address above.</p>

    <h2>What we collect, why, and on what basis</h2>
    <h3>When you message us</h3>
    <p>Your name, phone number or email address, and the contents of your message. We use it to answer you and, if you become a client, to run the service. <b>Legal basis:</b> Article 6(1)(b), steps taken at your request before entering a contract, and performance of the contract afterwards.</p>

    <h3>When you use this website</h3>
    <p>Our hosting and security providers record your IP address, the pages requested, timestamps, and your browser and device type in their server logs. We use this to keep the site available and to defend it against abuse. <b>Legal basis:</b> Article 6(1)(f), our legitimate interest in a working, secure website. We do not run analytics, advertising or tracking of any kind on this site.</p>

    <h3>Your theme and language choice</h3>
    <p>Stored in your own browser, never sent to us. See the <a href="/cookies">cookies and storage notice</a>.</p>

    <h3>When you are a client</h3>
    <p>Business contact details, the facts about your business that the system runs on, billing records and our correspondence. <b>Legal basis:</b> Article 6(1)(b) for the contract, and Article 6(1)(c) for keeping accounting records as Cyprus tax law requires.</p>

    <h2>Who else processes it</h2>
    <p>We keep this list short on purpose. Each of these is a processor acting under contract, or an independent controller where noted.</p>
    <ul>
      <li><b>Vercel Inc.</b> — hosting and delivery of this website. Server logs.</li>
      <li><b>Cloudflare, Inc.</b> — DNS, caching and protection against attacks. Traffic metadata.</li>
      <li><b>Anthropic PBC</b> — the AI model that generates assistant replies. Message content is sent for processing and is not used to train models.</li>
      <li><b>Meta Platforms Ireland Ltd.</b> — WhatsApp Business and Instagram messaging, where a client uses those channels. Meta is an independent controller for the messaging platform itself under its own terms.</li>
      <li><b>Google Ireland Ltd.</b> — Google Business Profile, for clients on the Reach card, and the fonts this site loads. Independent controller.</li>
      <li><b>Web3Forms</b> — delivery of any contact form submission.</li>
      <li>Our accountant and, where legally compelled, public authorities.</li>
    </ul>
    <p>We do not sell personal data, and we do not share it for anyone else&rsquo;s marketing.</p>

    <h3>Data processing agreements</h3>
    <p>Because we handle conversations belonging to our clients&rsquo; customers, every client engagement is covered by a written data processing agreement under Article 28 of the GDPR before the service goes live. It records what we process, for how long, on whose instructions, which sub-processors are approved, and what happens to the data when the contract ends. Clients also need their own privacy notice covering what their customers&rsquo; messages are used for — we will tell you what our part of it says, but publishing yours is your obligation, not ours.</p>

    <h2>Transfers outside the EEA</h2>
    <p>Some of the providers above are established in, or process data in, the United States. Those transfers rely on the European Commission&rsquo;s Standard Contractual Clauses, on the EU&ndash;US Data Privacy Framework where the provider is certified, and on the supplementary measures set out in each provider&rsquo;s data processing terms. You can ask us for a copy of the relevant safeguards.</p>

    <h2>How long we keep it</h2>
    <ul>
      <li>Enquiries that do not become clients: 12 months.</li>
      <li>Client records and correspondence: for the length of the contract and 6 years after, which is the period Cyprus tax law requires for accounting records.</li>
      <li>Server and security logs: as retained by the providers above, typically under 30 days.</li>
      <li>Data inside a client&rsquo;s own system: for as long as that client instructs, and deleted or exported on request when their service ends.</li>
    </ul>

    <h2>Automated decisions</h2>
    <p>The assistant composes replies automatically, which is automated processing. It does not make decisions that produce a legal effect for you or similarly significantly affect you within the meaning of Article 22 — it answers questions and offers to hold a booking, and a person can take over at any moment.</p>

    <h2>Your rights</h2>
    <p>Under the GDPR you can ask us to:</p>
    <ul>
      <li>confirm what we hold and give you a copy of it (Article 15);</li>
      <li>correct anything inaccurate (Article 16);</li>
      <li>delete it, where we have no overriding reason to keep it (Article 17);</li>
      <li>restrict what we do with it while a question is resolved (Article 18);</li>
      <li>hand it over in a portable format (Article 20);</li>
      <li>stop processing based on legitimate interests, including any direct marketing, which we will stop on request without exception (Article 21).</li>
    </ul>
    <p>Where we rely on consent, you can withdraw it at any time without affecting anything done before you withdrew it. Email <a href="mailto:%(privacy)s">%(privacy)s</a>. We answer within one month and we do not charge for it.</p>

    <h2>Complaining</h2>
    <p>If you think we have handled your data badly, tell us first — it is usually a misunderstanding we can fix the same day. You also have the right to complain to the supervisory authority:</p>
    <p><b>Office of the Commissioner for Personal Data Protection</b>, Republic of Cyprus &mdash; <a href="https://www.dataprotection.gov.cy" rel="noopener">www.dataprotection.gov.cy</a>. If you live in another EU country, you may complain to your own national authority instead.</p>

    <h2>Changes</h2>
    <p>If we change this notice we update the date at the top, and we tell clients directly if the change matters to them.</p>
''' % sub))

    # ------------------------------------------------------------ cookies
    P.append(wrap(
        'cookies', 'Cookies',
        'Cookies and storage — Ownerdeck',
        'This site sets no tracking cookies. Here is exactly what it does store '
        'in your browser and why no consent banner is needed.',
        'Cookies and storage',
        '''    <p>This notice covers Article 5(3) of Directive 2002/58/EC, as transposed in Cyprus by the Regulation of Electronic Communications and Postal Services Law of 2004 (112(I)/2004).</p>

    <h2>The short version</h2>
    <p>This site sets <b>no advertising cookies, no analytics cookies and no tracking of any kind</b>. That is why you are not being asked to accept anything. There is no banner because there is nothing to consent to.</p>

    <h2>What is actually stored</h2>
    <p>Two values, in your browser&rsquo;s local storage, created only when you choose something. They never leave your device and are never sent to us.</p>
    <dl>
      <dt><code>od_theme</code></dt><dd>Remembers whether you picked the light or the dark theme. Written only when you use the theme button. Kept until you clear your browser data.</dd>
      <dt><code>od_lang</code></dt><dd>Remembers which language you picked. Written only when you use the language switcher. Kept until you clear your browser data.</dd>
    </dl>
    <p>Both are strictly necessary to provide the preference you explicitly asked for, which is the exemption in Article 5(3). If you never touch either control, nothing is stored at all.</p>

    <h2>Your network provider</h2>
    <p>Cloudflare, which protects this site from attack, may set a strictly necessary security cookie to tell real visitors from automated traffic. It carries no advertising identifier and is exempt on the same basis.</p>

    <h2>Fonts</h2>
    <p>The typefaces are served by Google Fonts. Loading them discloses your IP address to Google as a technical necessity of fetching the file. Google states it sets no cookies for the Fonts service. If you would rather that request never happened, a content blocker will stop it and the site will fall back to your system typeface with no loss of function.</p>

    <h2>Clearing it</h2>
    <p>Clearing site data for this domain in your browser settings removes both values immediately. The site keeps working; it simply forgets your theme and language.</p>

    <h2>Systems we build for clients</h2>
    <p>A website we build for a client may need more than this — a session cookie to keep a booking together, for example. Each of those sites carries its own cookie notice, and where non-essential cookies are involved, its own consent banner.</p>
''' % sub))

    # -------------------------------------------------------------- terms
    P.append(wrap(
        'terms', 'Terms',
        'Terms of service — Ownerdeck',
        'The terms covering an Ownerdeck build and the monthly service that '
        'runs it. Business to business, governed by Cyprus law.',
        'Terms of service',
        '''    <p>These terms govern the build we do for you and the monthly service that keeps it running. They form a contract between you and Ownerdeck as identified in our <a href="/legal">legal notice</a>. They apply from the day you accept a quote, in writing or over WhatsApp.</p>

    <h2>1. Who these terms are for</h2>
    <p>Ownerdeck contracts with businesses and with people acting for purposes related to their trade or profession. We do not contract with consumers. Because of that, the fourteen day right of withdrawal for distance contracts under Directive 2011/83/EU and Cyprus Law 133(I)/2013 does not apply. If you are buying as a consumer, tell us before you accept a quote, because these terms are not written for you.</p>

    <h2>2. What you are buying</h2>
    <p>A <b>build fee</b>, paid once, covers designing and building what you ordered. A <b>monthly fee</b> covers running it. The plan, the fee and what is included are the ones shown on the <a href="/pricing">pricing page</a>, or in your written quote where that differs.</p>
    <p>The monthly fee covers hosting, the domain, the database, the assistant running, backups, security updates and reasonable changes — prices, services, text, photos. It does not cover rebuilding the site, adding a card you did not order, or work outside the online side of your business. We quote for those before starting.</p>

    <h2>3. What we need from you</h2>
    <p>The build depends on you giving us accurate facts about your business and the access we need — your domain, your WhatsApp Business number, your Google listing. You are responsible for the accuracy and legality of what you give us, for holding the rights to any photo or text you supply, and for your own obligations to your customers, including your own privacy notice and consumer law duties. Delays in getting us what we need move the delivery date.</p>

    <h2>4. Ownership</h2>
    <p>Your website, your content, your data and your phone number are yours. On delivery of the build, we assign to you the rights in the site design and content made specifically for you.</p>
    <p>We keep ownership of the underlying tools, templates, code libraries and know-how we reuse across clients, and grant you a perpetual, non-exclusive licence to use them as part of your site for as long as you use it. If you leave, we hand over the site files and an export of your database in a common format, at no charge.</p>

    <h2>5. The assistant, and its limits</h2>
    <p>The AI assistant answers from the facts in your database. It is instructed not to invent prices or availability, and to hand a conversation to you when it is unsure.</p>
    <p>It is still software built on a language model, and it can make mistakes. You are responsible for what your business commits to. You can read every conversation and take over any of them at any time. We ask that you check its answers during the first weeks and tell us anything wrong so we can correct the underlying facts. We do not warrant that it will never make an error.</p>

    <h2>6. Data protection</h2>
    <p>Where we handle personal data belonging to <i>your</i> customers, you are the controller and we are your processor under Article 28 of the GDPR. We will process it only on your documented instructions, keep it confidential, apply appropriate security, use only the sub-processors listed in our <a href="/privacy">privacy notice</a>, help you answer data subject requests and security incidents, and delete or return it when the service ends. Our own handling of data is set out in that same notice. On request we will sign a separate data processing agreement.</p>

    <h2>7. Money</h2>
    <p>The build fee is invoiced on acceptance and payable before the service goes live, unless we have agreed otherwise in writing. The monthly fee is invoiced monthly in advance. Prices are in euro. <b>Ownerdeck is not registered for VAT, so no VAT is added.</b></p>
    <p>We do not hold your customers&rsquo; money at any point. Deposits and payments run through your own merchant account with your own payment provider, and their fees are theirs, not ours.</p>
    <p>If an invoice is more than 14 days late we may suspend the service after giving you notice. We will not delete anything for non-payment without telling you first and giving you a chance to export it.</p>

    <h2>8. Changing the price</h2>
    <p>We may change the monthly fee once in any twelve month period, with at least 30 days&rsquo; written notice. If you do not want the new price, you may end the service before it takes effect and owe nothing further.</p>

    <h2>9. Ending it</h2>
    <p>You may end the monthly service at any time with 30 days&rsquo; written notice. There is no minimum term on any plan. Work quoted separately outside a plan is governed by whatever that written quote says.</p>
    <p>The build fee is not refundable once the build has been delivered. If we have started but not delivered, we refund the part not yet worked.</p>
    <p>Either of us may end the contract immediately if the other commits a serious breach and does not fix it within 14 days of being told, or becomes insolvent. On termination we hand over your files and a data export, and your licence to the underlying tools ends.</p>

    <h2>10. What we promise, and what we do not</h2>
    <p>We will carry out the work with reasonable care and skill, and we will keep the service available as far as we reasonably can. We do not promise that it will be uninterrupted or error free, and we do not promise any particular commercial result — more bookings, better rankings, a higher review score.</p>
    <p>We are not responsible for failures at third parties outside our control, including WhatsApp, Instagram, Google, the hosting platform, your payment provider or your internet connection.</p>

    <h2>11. Liability</h2>
    <p>Nothing in these terms limits liability for death or personal injury caused by negligence, for fraud, or for anything else that cannot lawfully be limited.</p>
    <p>Subject to that, neither of us is liable to the other for loss of profit, loss of business, loss of goodwill or any indirect or consequential loss. Our total liability arising in any twelve month period is limited to the total fees you paid us in that period.</p>

    <h2>12. Confidentiality</h2>
    <p>Each of us will keep the other&rsquo;s non-public business information confidential and use it only to perform this contract. We would like to name you as a client and describe the work in general terms; tell us if you would rather we did not, and we will not.</p>

    <h2>13. Force majeure</h2>
    <p>Neither of us is in breach for a delay or failure caused by something genuinely outside our reasonable control. If it lasts more than 60 days, either of us may end the contract without further liability.</p>

    <h2>14. Changes to these terms</h2>
    <p>We may update these terms and will give clients at least 30 days&rsquo; notice of anything that materially affects them. Continuing to use the service after that counts as acceptance. The version that applies to a dispute is the one in force when it arose.</p>

    <h2>15. General</h2>
    <p>These terms are the whole agreement between us on this subject. If a court finds any part unenforceable, the rest stands. Failing to enforce something once does not waive it. Neither of us may transfer this contract without the other&rsquo;s consent, except to a buyer of substantially the whole business. Nobody other than you and us can enforce these terms.</p>
    <p>These terms are written in English. Any translation is provided for convenience, and the English version governs.</p>

    <h2>16. Law and courts</h2>
    <p>These terms and any dispute arising out of them, including non-contractual ones, are governed by the law of the Republic of Cyprus. The courts of the Republic of Cyprus have exclusive jurisdiction.</p>

    <h2>17. Getting in touch</h2>
    <p>Questions about these terms go to <a href="mailto:%(email)s">%(email)s</a> or over <a href="%(wa)s" rel="noopener">WhatsApp</a>.</p>
''' % sub))

    return P
