# Intrinsic Elicitation, Between-Experiment Analysis

Following the two experiments, [intrinsic elicitiation 1](https://github.com/davidgundry/intrinsic-elicitation-1) [[OSF](https://osf.io/u2nze/)] and [intrinsic elicitation 2](https://github.com/davidgundry/intrinsic-elicitation-2), [[OSF](https://osf.io/4g9fh/)] we want to do some further exploratory analysis to compare these datasets. This will be published in the same paper as the above two experiments. There is no further data collection, and the analysis is not preregistered.

This repository is also hosted on OSF at [https://osf.io/5tgc8/](https://osf.io/5tgc8/).

We're mainly interested if the changes we made to the game between experiments (positioning buttons in columns, removing explicit instructions in control condition, graphical improvements, different levels, better block creation algorithm, etc.) had an effect on the proportion of valid data.

Some of this analysis is to be published in the following conference paper. In the paper we report the proposition of valid data between experiments. There is also more exploratory analysis that has not been published.

> David Gundry and Sebastian Deterding. 2022. Trading Accuracy for Enjoyment? Data Quality and Player Experience in Data Collection Games. In CHI Conference on Human Factors in Computing Systems (CHI ’22), April 29-May 5, 2022, New Orleans, LA, USA. ACM, New York, NY, USA, 14 pages. [https://doi.org/10.1145/3491102.3502025](https://doi.org/10.1145/3491102.3502025)

## Directory Structure

* `data/` - processed/anonymised data
* `out/` - output of analysis scripts including data and graphs. Logs of script console output is saved here too
* `python/` - python scripts
* `r/` - r scripts

## Data Source

Data was taken from the experiments [intrinsic elicitiation 1](https://github.com/davidgundry/intrinsic-elicitation-1) and [intrinsic elicitation 2](https://github.com/davidgundry/intrinsic-elicitation-2). The `out/data.csv` file was used from each experiment as it's easier to work with manually than JSON.

The file `data/combined.csv` was manually constructed by concatenating the relevant columns from the data from experiments 1 and 2 and making condition names consistent. The `row` column was numbered as the records appeared in the CSV. An `exp` column was set to `1` for the first experiment and `2` for the second experiment.

## Analysis

In the project directory (for this experiment) run the following commands (on Linux). These create (or overwrite) files in `out/`).

    python python/proportion_valid_between.py > out/proportion_valid_between.txt

    python python/enjoyment_between.py > out/enjoyment_between.txt

    python python/time_between.py > out/time_between.txt

    python python/most_matched_grammar.py > out/most_matched_grammar.txt

    python python/popular_orders.py > out/popular_orders.txt

A script to run a power analysis for a possible future experiment can be found in `r/`, which generated `out/power-anaysis.Rout`. You can generate this using the following command:

    R CMD BATCH --quiet r/power-analysis.r out/power-analysis.Rout
