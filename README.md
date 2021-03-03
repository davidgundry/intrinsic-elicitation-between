# Intrinsic Elicitation, Between-Experiment Analysis

No data collection, just further analysis comparing the data sets already collected.

We're mainly interested if the changes we made to the game between experiments (positioning buttons in columns, removing explicit instructions in control condition, graphical improvements, different levels, better block creation algorithm, etc.) had an effect on the proportion of valid data.

## Directory Structure

* `data/` - processed/anonymised data
* `out/` - output of analysis scripts including data and graphs. Logs of script console output is saved here too
* `python/` - python scripts
* `r/` - r scripts

## Data Source

`combined.csv` was manually constructed by concatenating the relevant columns from the data from experiments 1 and 2 and making condition names consistent.

## Analysis

In the project directory (for this experiment) run the following commands (on Linux). These create (or overwrite) files in `out/`).

    python python/analysis_between.py > out/analysis_between.txt

## Power analysis for subsequent experiment

A script to run a power analysis for a possible future experiment can be found in `r/`, which generated `out/power-anaysis.Rout`. You can generate this using the following command:

    R CMD BATCH --quiet r/power-analysis.r out/power-analysis.Rout
