from dataclasses import dataclass
from datetime import date
from typing import Callable, Dict, Sequence

import pandas as pd

from instrument_data import InstrumentValues, to_wide, values_on


@dataclass(frozen=True)
class IndexResult:
    levels: pd.Series
    weights: pd.DataFrame


def index_levels(
    instrument_data: pd.DataFrame,
    base_date: pd.Timestamp,
    rebalance_dates: Sequence[date],
    selection_algo: Callable[[Sequence[InstrumentValues]], Sequence[InstrumentValues]],
    weighting_algo: Callable[[Sequence[InstrumentValues]], Dict[str, float]],
    base_value: float = 1000.0,
) -> IndexResult:
    """Compute a rebalanced index's level series and its daily holding-weight matrix.

    instrument_data: tidy (date, symbol, field...) frame from a provider (see instrument_data.py),
        must include a "price" field; other fields (e.g. "market_cap") are whatever
        selection_algo/weighting_algo need.
    selection_algo: picks the instruments to hold from each rebalance date's instrument values.
    weighting_algo: maps the selected instrument values to their weight (fraction of 1.0) for that period.

    Returns an IndexResult: .levels is the index level time series; .weights is a date x symbol
    matrix of each holding's weight, drifting with prices between rebalances and reset to
    weighting_algo's target on each rebalance date (0 for symbols not held that period). Feed
    .weights and the same rebalance_dates to index_utils.turnover() to measure turnover.
    """
    close_prices = to_wide(instrument_data, "price")
    close_filled = close_prices.ffill()  # covers occasional single-day gaps in an otherwise-listed stock's history
    trading_days = close_prices.loc[base_date:].index

    index_values = pd.Series(index=trading_days, dtype=float, name="index_value")
    weights_by_period = []
    current_base_value = base_value

    for i, reb_date in enumerate(rebalance_dates):
        period_end = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else None
        if period_end is not None:
            period_days = trading_days[(trading_days >= reb_date) & (trading_days < period_end)]
        else:
            period_days = trading_days[trading_days >= reb_date]

        instrument_values = values_on(instrument_data, reb_date)
        selected = selection_algo(instrument_values)
        selected_symbols = [iv.symbol for iv in selected]

        target_weights = pd.Series(weighting_algo(selected))
        start_prices = close_filled.loc[reb_date, selected_symbols]
        shares = (current_base_value * target_weights) / start_prices

        period_prices = close_filled.loc[period_days, selected_symbols]
        period_holding_values = period_prices.mul(shares, axis=1)
        period_index_values = period_holding_values.sum(axis=1)

        index_values.loc[period_days] = period_index_values
        weights_by_period.append(period_holding_values.div(period_index_values, axis=0))
        current_base_value = period_index_values.iloc[-1]

    weights = pd.concat(weights_by_period).fillna(0.0)
    return IndexResult(levels=index_values, weights=weights)
