"""Catalog of rebalance date schedules.

Each scheme maps a sequence of trading days and a base date to the list of rebalance
dates. This is the shape index_levels()'s rebalance_dates argument expects,
so any scheme here can be swapped in interchangeably. Signatures use core Python types
(date, not pd.Timestamp/DatetimeIndex) so this module has no pandas dependency;
pd.Timestamp objects satisfy them fine, since Timestamp is a subclass of date.
"""

from datetime import date
from itertools import groupby
from typing import List, Sequence


def month_end(trading_days: Sequence[date], base_date: date) -> List[date]:
    """Rebalance dates: base_date itself, then the last trading day of every month after it."""
    after_base = sorted(d for d in trading_days if d >= base_date)
    month_ends = [max(days) for _, days in groupby(after_base, key=lambda d: (d.year, d.month))]
    return [base_date] + [d for d in month_ends if d > base_date]
