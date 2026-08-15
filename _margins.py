# Does the pricing cover costs at 2x minimum?
#
# Two kinds of number live here, and they are not the same:
#   VERIFIED  - taken from the repo, the live config, or Anthropic's published
#               rates. Safe to reason from.
#   ASSUMED   - a placeholder. Every one of these is marked and listed at the
#               end. Change them and re-run; do not quote the output until the
#               ASSUMED block matches reality.
#
# Run:  python _margins.py            (central case)
#       python _margins.py 400        (400 customer conversations/client/month)
import sys

EUR_PER_USD = 0.92          # ASSUMED - set to the rate your card actually bills

# ---------------------------------------------------------------- VERIFIED
# Anthropic list prices, USD per million tokens (input, output).
CLAUDE = {
    'haiku-4.5':  (1.00,  5.00),
    'sonnet-4.6': (3.00, 15.00),
    'sonnet-5':   (3.00, 15.00),   # intro $2/$10 through 2026-08-31
}

PRICES = {'Answer': 150, 'Deck': 249, 'Full Deck': 299}

# The booking bot runs Sonnet 4.6 (Haiku was unreliable at the required JSON —
# see the Voyage notes). The website chat runs Haiku 4.5 with a 300-token
# output cap and a measured ~$0.0004 per exchange.
BOOKING_MODEL = 'sonnet-4.6'

# ---------------------------------------------------------------- ASSUMED
# Per inbound customer message, the bot resends system prompt + filtered
# history, so input dominates. Sized from the known architecture: BUSINESS
# config + rules + ~15 turns of history, max_tokens 1500.
IN_TOK, OUT_TOK = 5000, 300          # ASSUMED
MSGS_PER_CONVO  = 8                  # ASSUMED
CONVOS_PER_MONTH = int(sys.argv[1]) if len(sys.argv) > 1 else 250   # ASSUMED

BOOKING_RATE = 0.25                  # ASSUMED - conversations that become bookings
HETZNER_TOTAL = 12.00                # ASSUMED - EUR/month for the n8n box, ALL clients
CLIENTS = 10                         # ASSUMED - clients sharing that box
STRIPE_PCT, STRIPE_FIX = 0.015, 0.25 # ASSUMED - EU card rate

# WhatsApp: service replies inside the 24h customer window are free. Business
# INITIATED template messages are charged per message, by category and country.
# This is the single biggest unknown in the model and the only cost that scales
# with the client's booking volume.
TPL_UTILITY   = 0.03                 # ASSUMED - EUR, reminders/confirmations
TPL_MARKETING = 0.06                 # ASSUMED - EUR, off-season offers


# Pass "cache" as the second argument to model prompt caching being switched on
# for the booking bot's system prompt. Cache reads bill at ~0.1x, and the system
# prompt is the stable prefix that gets resent on every single message.
CACHING = len(sys.argv) > 2 and sys.argv[2] == 'cache'
STABLE_PREFIX = 0.70                 # ASSUMED - share of input that never changes


def claude_cost_eur(convos):
    """Booking-bot inference for one client for one month."""
    cin, cout = CLAUDE[BOOKING_MODEL]
    msgs = convos * MSGS_PER_CONVO
    eff_in = (IN_TOK * (1 - STABLE_PREFIX) + IN_TOK * STABLE_PREFIX * 0.1
              if CACHING else IN_TOK)
    usd = (msgs * eff_in / 1e6) * cin + (msgs * OUT_TOK / 1e6) * cout
    return usd * EUR_PER_USD


def template_cost_eur(convos, cards):
    """Only the cards that send business-initiated messages cost per message."""
    bookings = convos * BOOKING_RATE
    n = 0.0
    if 'Book' in cards:
        n += bookings * 2 * TPL_UTILITY          # confirmation + pickup reminder
    if 'Reach' in cards:
        n += bookings * 1 * TPL_UTILITY          # review request after each booking
    if 'Return' in cards:
        n += bookings * 1.5 * TPL_MARKETING      # reminders + off-season offers
    return n


TIERS = {
    'Answer':    ['Answer'],
    'Deck':      ['Answer', 'Site', 'Book'],
    'Full Deck': ['Answer', 'Site', 'Book', 'Reach', 'Return'],
}


def report(convos):
    print('=' * 74)
    print('  %d conversations/client/month, %d msgs each, %s, %d clients on one box'
          % (convos, MSGS_PER_CONVO, BOOKING_MODEL, CLIENTS))
    print('=' * 74)
    print('%-11s %8s %8s %8s %8s %8s %7s %6s' %
          ('TIER', 'PRICE', 'CLAUDE', 'WHATSAPP', 'HOST', 'STRIPE', 'GROSS', 'MULT'))

    host = HETZNER_TOTAL / CLIENTS
    for tier, cards in TIERS.items():
        price  = PRICES[tier]
        claude = claude_cost_eur(convos)
        tpl    = template_cost_eur(convos, cards)
        stripe = price * STRIPE_PCT + STRIPE_FIX
        total  = claude + tpl + host + stripe
        gross  = price - total
        mult   = price / total if total else float('inf')
        flag   = '' if mult >= 2 else '   <-- UNDER 2x'
        print('%-11s %8.0f %8.2f %8.2f %8.2f %8.2f %7.2f %5.1fx%s'
              % (tier, price, claude, tpl, host, stripe, gross, mult, flag))

    print()
    print('  MULT = price / direct cost. Target is 2.0x or better.')
    print('  Excludes your time, which is the real constraint (see notes).')


def breakeven():
    """At what volume does each tier stop returning 2x?"""
    print()
    print('Volume at which each tier drops below 2x')
    print('-' * 74)
    host = HETZNER_TOTAL / CLIENTS
    for tier, cards in TIERS.items():
        price = PRICES[tier]
        stripe = price * STRIPE_PCT + STRIPE_FIX
        limit = None
        for c in range(10, 20001, 10):
            total = claude_cost_eur(c) + template_cost_eur(c, cards) + host + stripe
            if price / total < 2:
                limit = c
                break
        print('  %-11s  %s conversations/month'
              % (tier, ('%d' % limit) if limit else '>20,000 (never, at these rates)'))


def levers():
    print()
    print('Biggest levers, measured')
    print('-' * 74)
    base = claude_cost_eur(CONVOS_PER_MONTH)
    cin, cout = CLAUDE[BOOKING_MODEL]

    # Prompt caching: the system prompt is resent on every message and is the
    # bulk of the input. Cache reads bill at ~0.1x.
    cached_in = IN_TOK * 0.3 + IN_TOK * 0.7 * 0.1     # 70% of input is stable prefix
    msgs = CONVOS_PER_MONTH * MSGS_PER_CONVO
    cached = ((msgs * cached_in / 1e6) * cin +
              (msgs * OUT_TOK / 1e6) * cout) * EUR_PER_USD
    print('  prompt caching on the system prompt   EUR %.2f -> %.2f  (-%.0f%%)'
          % (base, cached, (1 - cached / base) * 100))

    hin, hout = CLAUDE['haiku-4.5']
    haiku = ((msgs * IN_TOK / 1e6) * hin + (msgs * OUT_TOK / 1e6) * hout) * EUR_PER_USD
    print('  Haiku instead of Sonnet               EUR %.2f -> %.2f  (-%.0f%%)  '
          'NOTE: Haiku was unreliable at the JSON this bot needs'
          % (base, haiku, (1 - haiku / base) * 100))


if __name__ == '__main__':
    report(CONVOS_PER_MONTH)
    breakeven()
    levers()
    print()
    print('ASSUMED inputs you must confirm before trusting any of the above:')
    print('-' * 74)
    for k, v in [('conversations/client/month', CONVOS_PER_MONTH),
                 ('messages per conversation', MSGS_PER_CONVO),
                 ('input tokens per message', IN_TOK),
                 ('booking rate', BOOKING_RATE),
                 ('WhatsApp utility template EUR', TPL_UTILITY),
                 ('WhatsApp marketing template EUR', TPL_MARKETING),
                 ('Hetzner EUR/month (all clients)', HETZNER_TOTAL),
                 ('clients sharing the box', CLIENTS),
                 ('USD->EUR', EUR_PER_USD)]:
        print('  %-34s %s' % (k, v))
