## June 7, 2026
Had a play with PuLP versus SciPi and I'm ready to try something a litle more adventurous.
Ideally I'd like to have a go at something that I'm likely to see at work:
1. Maximise projected return across a portfolio of > 100 securities
2. Keep turnover below X%
3. Limit a specific sector to Y%
4. Weights must some to 100%
5. Cannot have negative weights

So I installed a nice dataset (NYSE) from Kaggle. I'll have a play with that. Now in Data folder.
I've changed the github setting so that the data doesn't end up in github.

## July 19, 2026
Started noodling around in portfolio_optimization.ipynb, just exploring the Kaggle data before trying anything genuine.
- Read in securities.csv - 505 securities listed.
- Read in prices-split-adjusted.csv - only 501 unique symbols show up in the price history, so 4 of the securities don't have price data.
- Checked the earliest date per symbol to see if the price history is aligned across all securities. It isn't - 467 of the 501 start on 2010-01-04, but the rest start later (a handful of dates scattered up to 2016). Will need to bear this in mind (e.g. truncating to a common start date, or handling the shorter histories) once I get to the actual optimisation.
- Added pandas to requirements.txt since I'm using it to load the CSVs.

## July 25, 2026
Pivoted from just exploring the Kaggle data to actually building out a basic index backtesting engine, ahead of the real optimisation work. Structured it as a set of small swappable pieces rather than one big script:
- `instrument_data.py` - the data contract. Providers hand back a tidy (date, symbol,
  field) frame; `combine()` stitches multiple providers together so `index_levels()`
  sees one frame with everything it needs.
- `providers/csv_provider.py` - first provider, reads the Kaggle split-adjusted prices
  CSV into that tidy shape.
- `selection.py` / `weighting.py` / `rebalance_date.py` - catalogs of interchangeable
  schemes (e.g. `top_n` selection, `equal_weights` weighting, `month_end` rebalancing)
  that all plug into `index_levels()` via a common shape.
- `index_calculation.py` - the actual engine, producing an `IndexResult` (levels +
  daily weights matrix).
- `index_utils.py` - post-processing helpers: `rebase()` to reset an index to a base
  value/date, `turnover()` to compute two-way turnover at each rebalance date.
- `plot.py` - shared plotting helpers for the notebook.

Still using naive schemes throughout (equal weighting, top-N by a single field) - next big step is swapping the weighting side out for the actual optimised weight logic (the LP-based one from the June 7 goals: max return subject to turnover/sector/sum-to-100/no-shorting constraints). Everything above is really just scaffolding so that once the optimiser exists, I can backtest it properly.