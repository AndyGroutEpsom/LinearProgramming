"""The data contract that instrument data providers produce.

A provider returns a tidy DataFrame: one row per (date, symbol), plus one column per
field it supplies (e.g. "price", "market_cap"). Different providers can supply
different fields; combine() stitches their outputs together on (date, symbol) so
index_levels() sees one frame with everything it needs for a given run.
"""

from dataclasses import dataclass
from datetime import date
from typing import Dict, List

import pandas as pd


@dataclass(frozen=True)
class InstrumentValues:
    symbol: str
    market_values: Dict[str, float]

    def __getitem__(self, field: str) -> float:
        return self.market_values[field]


def combine(*frames: pd.DataFrame) -> pd.DataFrame:
    """Outer-merge tidy (date, symbol, field...) frames from one or more providers on (date, symbol)."""
    result = frames[0]
    for frame in frames[1:]:
        result = result.merge(frame, on=["date", "symbol"], how="outer")
    return result.sort_values(["date", "symbol"]).reset_index(drop=True)


def values_on(data: pd.DataFrame, as_of_date: date) -> List[InstrumentValues]:
    """InstrumentValues for every symbol with a complete row (no missing fields) on as_of_date."""
    day = data[data["date"] == as_of_date].dropna()
    fields = day.columns.drop(["date", "symbol"])
    return [InstrumentValues(row["symbol"], row[fields].to_dict()) for _, row in day.iterrows()]


def to_wide(data: pd.DataFrame, field: str) -> pd.DataFrame:
    """Pivot one field to a date x symbol matrix, one price per cell."""
    return data.pivot(index="date", columns="symbol", values=field).sort_index()
