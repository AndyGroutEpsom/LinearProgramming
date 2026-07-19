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