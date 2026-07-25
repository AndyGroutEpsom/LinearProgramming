"""Catalog of selection schemes.

Each scheme maps a sequence of InstrumentValues to the subset to hold. This is the
shape index_levels()'s selection_algo parameter expects, so any scheme here
can be swapped in interchangeably.
"""

from typing import Sequence

from instrument_data import InstrumentValues


def top_n(instrument_values: Sequence[InstrumentValues], n: int, field: str) -> Sequence[InstrumentValues]:
    return sorted(instrument_values, key=lambda iv: iv[field], reverse=True)[:n]
