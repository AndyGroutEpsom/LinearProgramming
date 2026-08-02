from datetime import date
from typing import Sequence

import pandas as pd


def rebase(index_values: pd.Series, base_date: pd.Timestamp, base_value: float = 1000.0) -> pd.Series:
    """Rescale index_values so it equals base_value on base_date, dropping any dates before it."""
    series_from_base = index_values.loc[base_date:]
    return series_from_base / series_from_base.loc[base_date] * base_value


def turnover(weights: pd.DataFrame, rebalance_dates: Sequence[date]) -> pd.Series:
    """Classic two-way turnover at each rebalance date.

    weights: date x symbol matrix of daily portfolio weights (drifting with prices between
        rebalances, reset to target weights on rebalance dates) - e.g. shares * price / portfolio
        value, one column per symbol, missing/unheld positions treated as 0.
    rebalance_dates: the dates on which weights was rebalanced; must be a subset of weights.index.
        The first rebalance date has no prior weights to compare against and is excluded from
        the result.

    Turnover on a rebalance date is half the sum of absolute weight changes between the drifted
    weights on the trading day immediately before it and the new weights on the day itself - the
    /2 avoids double-counting a trade as both a sell in one name and a buy in another.
    """
    turnovers = {}
    for reb_date in rebalance_dates[1:]:
        prior_days = weights.index[weights.index < reb_date]
        before = weights.loc[prior_days[-1]].fillna(0)
        after = weights.loc[reb_date].fillna(0)
        turnovers[reb_date] = before.subtract(after, fill_value=0).abs().sum() / 2
    return pd.Series(turnovers, name="turnover")


def sector_weights(weights: pd.DataFrame, sector_by_symbol: pd.Series) -> pd.DataFrame:
    """Roll a date x symbol weight matrix up to a date x sector matrix.

    sector_by_symbol: symbol -> GICS Sector lookup, e.g.
        instrument_data.drop_duplicates("symbol").set_index("symbol")["sector"].
    """
    return weights.T.groupby(sector_by_symbol).sum().T


def effective_sector_count(weights: pd.DataFrame, sector_by_symbol: pd.Series) -> pd.Series:
    """Effective number of sectors held, from the inverse Herfindahl-Hirschman Index of sector weights.

    A single number capturing diversification across the whole sector mix, not just the largest
    sector: 1.0 means the portfolio is concentrated in one sector; it equals the plain count of
    sectors held when they're equally weighted; a skewed mix scores lower than its raw sector count.
    Higher is more diversified - compare against the number of GICS sectors available (11) for scale.
    """
    hhi = sector_weights(weights, sector_by_symbol).pow(2).sum(axis=1)
    return (1 / hhi).rename("effective_sector_count")


def largest_sector_weight(weights: pd.DataFrame, sector_by_symbol: pd.Series) -> pd.Series:
    """Weight of the single largest sector, per date."""
    return sector_weights(weights, sector_by_symbol).max(axis=1).rename("largest_sector_weight")


