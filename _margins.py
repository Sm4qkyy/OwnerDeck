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
    'Data':     10,   # schema, admin views, import of what they already have
    'Answer':   12,   # prompt, business config, availability wiring, testing
    'Book':      8,   # calendar, confirmations, deposits
    'Reach':     3,   # Google listing, review flow
}
SUPPORT_HRS_MONTH = 1.5            # ASSUMED - per client, per month, ongoing
TARGET_HOURLY     = 45             # ASSUMED - EUR/hour Mark wants to clear

# Monthly cash costs, per client
HOSTING   = 2.00                   # ASSUMED - EUR, share of Vercel/Hetzner
DATABASE  = 3.00                   # ASSUMED - EUR, share of managed Postgres
DOMAIN    = 1.20                   # ASSUMED - EUR, ~15/yr
STRIPE_PCT, STRIPE_FIX = 0.015, 0.25

CONVOS   = int(sys.argv[1]) if len(sys.argv) > 1 else 250   # ASSUMED
MSGS     = 8                       # ASSUMED - messages per conversation
IN_TOK, OUT_TOK = 5000, 300        # ASSUMED - per message, system prompt resent
CACHING  = True                    # prompt caching on the system prefix
STABLE   = 0.70                    # ASSUMED - share of input that is stable
BOOK_RATE = 0.25                   # ASSUMED - conversations that become bookings
TPL_UTIL, TPL_MKT = 0.03, 0.06     # ASSUMED - EUR per WhatsApp template message

TIERS = {
    'Answer':    (['Answer'],                                  150),
    'Deck':      (['Answer', 'Site', 'Book'],                   249),
    'Full Deck': (['Answer', 'Site', 'Book', 'Reach', 'Data'],  299),
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


def monthly_cash(cards, convos):
    c = HOSTING + DOMAIN + claude_eur(convos) + templates_eur(convos, cards)
    if 'Data' in cards: c += DATABASE
    if 'Site' not in cards: c -= HOSTING * 0.5     # no site to host
    return c


def report(convos):
    print('=' * 78)
    print('  %d conversations/client/month · target %d EUR/hour · %.1f h/mo support'
          % (convos, TARGET_HOURLY, SUPPORT_HRS_MONTH))
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
        contrib = price - cash - stripe - (SUPPORT_HRS_MONTH * TARGET_HOURLY)
        months  = (build / contrib) if contrib > 0 else None
        # Effective hourly across year one: what the work actually paid.
        yr1_hours = hours + SUPPORT_HRS_MONTH * 12
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
        yr1_hours = hours + SUPPORT_HRS_MONTH * 12
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
                 ('support hours/client/month', SUPPORT_HRS_MONTH),
                 ('target hourly (EUR)', TARGET_HOURLY),
                 ('conversations/client/month', CONVOS),
                 ('managed Postgres share (EUR/mo)', DATABASE),
                 ('hosting share (EUR/mo)', HOSTING)]:
        print('  %-32s %s' % (k, v))
