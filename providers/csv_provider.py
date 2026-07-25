"""Instrument data provider backed by the CSV files in Data/."""

import pandas as pd


def load_prices(path: str = "Data/prices-split-adjusted.csv") -> pd.DataFrame:
    """Tidy (date, symbol, price) frame from a split-adjusted close prices CSV."""
    prices = pd.read_csv(path)
    prices["date"] = pd.to_datetime(prices["date"])
    return (
        prices[["date", "symbol", "close"]]
        .rename(columns={"close": "price"})
        .sort_values(["date", "symbol"])
        .reset_index(drop=True)
    )


def load_market_cap(prices: pd.DataFrame, fundamentals_path: str = "Data/fundamentals.csv") -> pd.DataFrame:
    """Tidy (date, symbol, market_cap) frame: prices["price"] x shares outstanding as most recently filed.

    prices: a (date, symbol, price) frame, e.g. from load_prices().
    Uses each symbol's most recently filed shares figure as of each price date (no look-ahead);
    symbols with no filing yet on a given date are dropped.
    """
    fundamentals = pd.read_csv(fundamentals_path)
    shares_outstanding = (
        fundamentals[["Ticker Symbol", "Period Ending", "Estimated Shares Outstanding"]]
        .dropna()
        .rename(columns={
            "Ticker Symbol": "symbol",
            "Period Ending": "date",
            "Estimated Shares Outstanding": "shares",
        })
        .assign(date=lambda df: pd.to_datetime(df["date"]))
        .sort_values("date")
    )
    merged = pd.merge_asof(
        prices.sort_values("date"),
        shares_outstanding,
        on="date",
        by="symbol",
        direction="backward",
    )
    return (
        merged.assign(market_cap=merged["price"] * merged["shares"])[["date", "symbol", "market_cap"]]
        .dropna()
        .sort_values(["date", "symbol"])
        .reset_index(drop=True)
    )
