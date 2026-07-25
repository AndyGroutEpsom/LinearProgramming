"""Catalog of weighting schemes.

Each scheme maps a sequence of selected InstrumentValues to a {symbol: weight} dict,
where weights are fractions of 1.0. This is the shape index_levels()'s
weighting_algo parameter expects, so any scheme here can be swapped in interchangeably.
"""

from typing import Dict, Sequence

from instrument_data import InstrumentValues


def equal_weights(instrument_values: Sequence[InstrumentValues]) -> Dict[str, float]:
    weight = 1.0 / len(instrument_values)
    return {iv.symbol: weight for iv in instrument_values}


def market_cap_weights(instrument_values: Sequence[InstrumentValues]) -> Dict[str, float]:
    total_market_cap = sum(iv["market_cap"] for iv in instrument_values)
    return {iv.symbol: iv["market_cap"] / total_market_cap for iv in instrument_values}
