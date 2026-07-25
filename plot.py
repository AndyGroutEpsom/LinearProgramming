"""Plotting helpers for portfolio_optimization.ipynb."""

from typing import Mapping, Union

import matplotlib.pyplot as plt
import pandas as pd

_CATEGORICAL_COLORS = [
    "#2a78d6",  # blue
    "#eb6834",  # orange
    "#1baf7a",  # aqua
    "#eda100",  # yellow
    "#e87ba4",  # magenta
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
]


def plot_index_levels(
    index_values: Union[pd.Series, Mapping[str, pd.Series]],
    title: str = "Index Level",
    ylabel: str = "Index value",
):
    """Plot one or more index level series on the same axes.

    index_values: a single pd.Series, or a {label: pd.Series} mapping for multiple series.
    """
    if isinstance(index_values, pd.Series):
        series_by_label = {index_values.name or "Index": index_values}
    else:
        series_by_label = dict(index_values)

    fig, ax = plt.subplots(figsize=(10, 4))
    for (label, series), color in zip(series_by_label.items(), _CATEGORICAL_COLORS):
        ax.plot(series.index, series.values, color=color, linewidth=1, label=label)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, color="#e1e0d9", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if len(series_by_label) > 1:
        ax.legend(frameon=False)

    fig.tight_layout()
    return fig, ax


def plot_turnover(
    turnover: pd.Series,
    title: str = "Turnover",
    ylabel: str = "Turnover",
):
    """Plot a turnover time series (e.g. from index_utils.turnover()) as one bar per rebalance date."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(turnover.index, turnover.values, width=20, color=_CATEGORICAL_COLORS[0])

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.grid(True, axis="y", color="#e1e0d9", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig, ax
