# Does the pricing survive the repositioning?
#
# The old version of this file modelled one assistant and deliberately excluded
# Mark's time. That was defensible when the product was a bot that ran itself.
# It is not defensible now: selling a built website and database means the
# dominant cost IS the hours, and a monthly-only price with no build fee means
# every new client starts deeply underwater.
#
# VERIFIED  - repo config, live rates, Anthropic published pricing.
# ASSUMED   - placeholder. All listed at the end. Change and re-run.
import sys

EUR_USD = 0.92                     # ASSUMED

# ---------------------------------------------------------------- VERIFIED
CLAUDE = {'haiku-4.5': (1.00, 5.00), 'sonnet-4.6': (3.00, 15.00)}
BOOKING_MODEL = 'sonnet-4.6'       # Haiku was unreliable at the required JSON

# ---------------------------------------------------------------- ASSUMED
# Build hours, once per client, by service.
HOURS = {
    'Site':     16,   # design, build, copy pass, deploy
    'Site-Lite': 9,   # ASSUMED - brochure site, no live database behind it.
                      # The entry tier now carries a website, so it carries
                      # the hours for one; the saving over Site is the data
                      # wiring and the admin views, not the design work.
    'Data':     10,   # schema, admin views, import of what they already have
    'Chat':      4,   # ASSUMED - website chat widget only. Same prompt work as
                      # Answer minus the WhatsApp and Instagram channel setup,
                      # which is where most of Answer's 12 hours actually go.
    'Answer':   12,   # prompt, business config, availability wiring, testing
    'Book':      8,   # calendar, confirmations, deposits
    'Reach':     3,   # Google listing, review flow
    'Return':    5,   # ASSUMED - campaign templates, segments, scheduling
}
# Support is per tier, not a single global. A brochure site generates a
# handful of "change this price" messages a year; a tier running an assistant
# and taking deposits generates questions every week. Using one number for
# both was what made a website-only tier look unviable.
SUPPORT_HRS = {'Site': 0.75, 'Deck': 1.5, 'Full Deck': 2.0}  # ASSUMED
TARGET_HOURLY     = 45             # ASSUMED - EUR/hour Mark wants to clear

# Monthly cash costs, per client
HOSTING   = 2.00                   # ASSUMED - EUR, share of Vercel/Hetzner
DATABASE  = 3.00                   # ASSUMED - EUR, share of managed Postgres
DOMAIN    = 1.20                   # ASSUMED - EUR, ~15/yr
STRIPE_PCT, STRIPE_FIX = 0.015, 0.25

CONVOS   = int(sys.argv[1]) if len(sys.argv) > 1 else 250   # ASSUMED
# A chat widget on a brochure site sees a fraction of what a WhatsApp number
# sees: the visitor has to be on the site already, and most of them are not.
# Modelling it at the full rate would price the entry tier for traffic it will
# never get.
CONVOS_WEB = 40                    # ASSUMED - website-chat-only volume
MSGS     = 8                       # ASSUMED - messages per conversation
IN_TOK, OUT_TOK = 5000, 300        # ASSUMED - per message, system prompt resent
CACHING  = True                    # prompt caching on the system prefix
STABLE   = 0.70                    # ASSUMED - share of input that is stable
BOOK_RATE = 0.25                   # ASSUMED - conversations that become bookings
TPL_UTIL, TPL_MKT = 0.03, 0.06     # ASSUMED - EUR per WhatsApp template message

# The entry tier is a website with a chat widget on it, and nothing else. The
# assistant's cost is driven by the channels it opens, not by its existence:
# a widget on a brochure site is a fraction of a WhatsApp number's traffic.
# That is what lets this tier sit at 99 rather than 249, and it makes the
# ladder legible — get online, then get answered everywhere, then get found.
TIERS = {
    'Site':      (['Site-Lite', 'Chat'],                                        99),
    'Deck':      (['Answer', 'Site', 'Data', 'Book'],                          249),
    'Full Deck': (['Answer', 'Site', 'Data', 'Book', 'Reach', 'Return'],       299),
}


def claude_eur(convos):
    cin, cout = CLAUDE[BOOKING_MODEL]
    n = convos * MSGS
    eff = IN_TOK * (1 - STABLE) + IN_TOK * STABLE * 0.1 if CACHING else IN_TOK
    return ((n * eff / 1e6) * cin + (n * OUT_TOK / 1e6) * cout) * EUR_USD


def templates_eur(convos, cards):
    b = convos * BOOK_RATE
    n = 0.0
    if 'Book' in cards:  n += b * 2 * TPL_UTIL
    if 'Reach' in cards: n += b * 1 * TPL_UTIL
    return n


def tier_convos(cards, convos):
    """How many conversations this tier's assistant actually handles."""
    if 'Answer' in cards: return convos       # WhatsApp, Instagram and the site
    if 'Chat' in cards:   return CONVOS_WEB   # the site only
    return 0


def monthly_cash(cards, convos):
    c = HOSTING + DOMAIN + templates_eur(convos, cards)
    # The model is the biggest line here, and it scales with the channels the
    # tier actually opens — not with the fact that it has an assistant at all.
    n = tier_convos(cards, convos)
    if n: c += claude_eur(n)
    if 'Data' in cards: c += DATABASE
    return c


def report(convos):
    print('=' * 78)
    print('  %d conversations/client/month · target %d EUR/hour · from %.1f h/mo support'
          % (convos, TARGET_HOURLY, min(SUPPORT_HRS.values())))
    print('=' * 78)
    print('%-11s %6s %7s %8s %9s %10s %9s' %
          ('TIER', 'PRICE', 'CASH/mo', 'BUILD h', 'BUILD @cost', 'BREAK-EVEN', 'YR1 €/h'))

    rows = []
    for tier, (cards, price) in TIERS.items():
        cash   = monthly_cash(cards, convos)
        hours  = sum(HOURS[c] for c in cards)
        build  = hours * TARGET_HOURLY
        stripe = price * STRIPE_PCT + STRIPE_FIX
        # Monthly contribution after cash costs and ongoing support time.
        support = SUPPORT_HRS[tier]
        contrib = price - cash - stripe - (support * TARGET_HOURLY)
        months  = (build / contrib) if contrib > 0 else None
        # Effective hourly across year one: what the work actually paid.
        yr1_hours = hours + support * 12
        yr1_cash  = price * 12 - (cash + stripe) * 12
        yr1_rate  = yr1_cash / yr1_hours
        rows.append((tier, price, cash, hours, build, months, yr1_rate, contrib))
        print('%-11s %6.0f %7.2f %8d %9.0f %10s %9.0f'
              % (tier, price, cash, hours, build,
                 ('%.1f mo' % months) if months else 'never', yr1_rate))
    return rows


def verdict(rows):
    print()
    print('Reading it')
    print('-' * 78)
    for tier, price, cash, hours, build, months, yr1, contrib in rows:
        cash_mult = price / (cash + price * STRIPE_PCT + STRIPE_FIX)
        line = '  %-11s cash margin %.0fx' % (tier, cash_mult)
        if months is None:
            line += ' · never recovers the build'
        elif months > 12:
            line += ' · build not repaid inside a year (%.1f mo)' % months
        elif months > 6:
            line += ' · build repaid in %.1f months' % months
        else:
            line += ' · build repaid in %.1f months' % months
        if yr1 < TARGET_HOURLY:
            line += ' · year one pays %.0f/h, under target' % yr1
        print(line)


def with_build_fee():
    print()
    print('Same tiers, with a one-off build fee at cost')
    print('-' * 78)
    print('%-11s %9s %8s %10s %9s' % ('TIER', 'BUILD FEE', 'MONTHLY', 'YR1 TOTAL', 'YR1 €/h'))
    for tier, (cards, price) in TIERS.items():
        hours = sum(HOURS[c] for c in cards)
        fee   = round(hours * TARGET_HOURLY / 50) * 50          # to the nearest 50
        cash  = monthly_cash(cards, CONVOS)
        stripe = price * STRIPE_PCT + STRIPE_FIX
        yr1_hours = hours + SUPPORT_HRS[tier] * 12
        yr1_cash  = fee + price * 12 - (cash + stripe) * 12
        print('%-11s %9.0f %8.0f %10.0f %9.0f'
              % (tier, fee, price, fee + price * 12, yr1_cash / yr1_hours))


if __name__ == '__main__':
    rows = report(CONVOS)
    verdict(rows)
    with_build_fee()
    print()
    print('ASSUMED inputs — confirm before quoting any of this')
    print('-' * 78)
    for k, v in [('build hours per service', HOURS),
                 ('support hours/client/month', SUPPORT_HRS),
                 ('target hourly (EUR)', TARGET_HOURLY),
                 ('conversations/client/month', CONVOS),
                 ('managed Postgres share (EUR/mo)', DATABASE),
                 ('hosting share (EUR/mo)', HOSTING)]:
        print('  %-32s %s' % (k, v))
