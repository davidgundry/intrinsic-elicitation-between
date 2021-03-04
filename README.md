# Intrinsic Elicitation, Between-Experiment Analysis

Following the two experiments, [intrinsic elicitiation 1](https://github.com/davidgundry/intrinsic-elicitation-1) and [intrinsic elicitation 2](https://github.com/davidgundry/intrinsic-elicitation-2), we want to do some further exploratory analysis to compare these datasets. This will be published in the same paper as the above two experiments. There is no further data collection, and the analysis is not preregistered.

We're mainly interested if the changes we made to the game between experiments (positioning buttons in columns, removing explicit instructions in control condition, graphical improvements, different levels, better block creation algorithm, etc.) had an effect on the proportion of valid data.

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


A script to run a power analysis for a possible future experiment can be found in `r/`, which generated `out/power-anaysis.Rout`. You can generate this using the following command:

    R CMD BATCH --quiet r/power-analysis.r out/power-analysis.Rout

