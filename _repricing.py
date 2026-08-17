# Does the competitive research's pricing recommendation actually survive?
#
# The research is right that EUR 600-2,400 upfront is the outlier in the market
# and that it kills conversations. It proposes "EUR 0-300 to start with
# EUR 249-349/month on a 6-month minimum" and asserts that this "preserves
# lifetime revenue".
#
# That assertion is not checked anywhere in the research, and it is the whole
# question. A build fee is not a margin — it is a cost recovery. Removing it
# without lengthening the term moves the break-even past the point at which a
# client is free to leave, which means every client who leaves at minimum term
# loses money.
#
# This models each structure against the real build hours from _margins.py.
import sys

sys.path.insert(0, '.')
from _margins import HOURS, SUPPORT_HRS, TARGET_HOURLY, monthly_cash, \
    STRIPE_PCT, STRIPE_FIX, CONVOS   # noqa: E402

DECK = ['Answer', 'Site', 'Data', 'Book']
TIER = 'Deck'

hours = sum(HOURS[c] for c in DECK)
build_cost = hours * TARGET_HOURLY
cash = monthly_cash(DECK, CONVOS)
support = SUPPORT_HRS[TIER]


def model(name, setup, monthly, min_months):
    stripe = monthly * STRIPE_PCT + STRIPE_FIX
    contrib = monthly - cash - stripe - (support * TARGET_HOURLY)
    # What we are actually out of pocket after the minimum term, if they leave
    # the day it ends.
    at_min = setup + contrib * min_months - build_cost
    months_to_break_even = (build_cost - setup) / contrib if contrib > 0 else None
    yr1_hours = hours + support * 12
    yr1 = setup + monthly * 12 - (cash + stripe) * 12
    return dict(name=name, setup=setup, monthly=monthly, min_months=min_months,
                contrib=contrib, at_min=at_min, be=months_to_break_even,
                yr1_rate=yr1 / yr1_hours)


print('=' * 84)
print('  Deck tier · %d build hours · %.0f EUR of work at the %d EUR/h target'
      % (hours, build_cost, TARGET_HOURLY))
print('  %.2f EUR/mo cash cost · %.2f h/mo support' % (cash, support))
print('=' * 84)
print('%-34s %7s %8s %7s %11s %9s' %
      ('STRUCTURE', 'SETUP', 'MONTHLY', 'MIN', 'AT MIN TERM', 'YR1 EUR/h'))

rows = [
    model('Today',                          1900, 249, 1),
    model('Research proposal (low end)',       0, 249, 6),
    model('Research proposal (high end)',    300, 349, 6),
    model('Research, but 12 month term',       0, 299, 12),
    model('Small setup, 12 month term',      300, 299, 12),
    model('Half the build fee, 12 months',   950, 279, 12),
]
for r in rows:
    flag = '' if r['at_min'] >= 0 else '   <-- LOSS'
    print('%-34s %7.0f %8.0f %7d %11.0f %9.0f%s'
          % (r['name'], r['setup'], r['monthly'], r['min_months'],
             r['at_min'], r['yr1_rate'], flag))

print()
print('  AT MIN TERM = what is left after recovering the build, if the client')
print('  leaves the day the minimum term ends. Negative means the work was')
print('  done at a loss.')
print()
for r in rows:
    if r['be']:
        print('  %-34s break-even at %4.1f months' % (r['name'], r['be']))
