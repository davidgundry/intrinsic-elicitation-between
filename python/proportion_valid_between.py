#
# A script to analyse how the proportion of valid data changed between experiment 1 and 2. 
#
# Different changes were made to game and control conditions so we want to examine each separately.
# Experiments lasted different durations. First only acepted 20 inputs, in the second most had many
# more than that. So we control by only considering the first 20 inputs (and excluding participants
# without that many).
# 

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import ttest_1samp
from scipy.stats import mannwhitneyu
from statsmodels.graphics.gofplots import qqplot
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt

import seaborn as sns
sns.set(style="ticks", font_scale=1.5)
import ptitprince as pt

minimum_moves=20
dataset = 'combined'
print("Analysing dataset", dataset, "\n")
df = pd.read_csv("data/"+dataset+".csv")
df = df[df['total_moves']>=minimum_moves]
df = df[df['bug'] != "bug"]



def hypothesis_valid_proporition(exp1, exp2):
    print("""Hypothesis: Proportion of valid data (first 20, idealised) will be lower in experiment 2
    than experiment 1. A two-tailed Mann-Whitney U test will be used to test
    whether the distribution differs significantly between the two experiments
     α = 0.05""")
    c0 = exp1['proportion_of_valid_data_first20_idealised']
    c1 = exp2['proportion_of_valid_data_first20_idealised']
    alpha = 0.05
    mwu = mannwhitneyu(c0, c1, alternative='two-sided')
    n0 = len(c0)
    n1 = len(c1)
    cond0 = (n0 - 1) * (stdev(c0) ** 2)
    cond1 = (n1 - 1) * (stdev(c1) ** 2)
    pooledSD = sqrt((cond0 + cond1) / (n0 + n1 - 2))
    cohens_d = (mean(c0) - mean(c1)) / pooledSD
    print("Exp1 mean" ,mean(c0), "sd" ,stdev(c0))
    print("Exp2 mean" ,mean(c1), "sd", stdev(c1))
    print("Mann-Whitney U test: p =", mwu.pvalue, "; U =",mwu.statistic, "; significant =",(mwu.pvalue < alpha), "; d =",cohens_d, "\n\n")


def valid_proportion_idealised_raincloud(df, condition):
    dy="proportion_of_valid_data_first20_idealised"; dx="exp"; ort="v"; pal = sns.color_palette(n_colors=2)
    f, ax = plt.subplots(figsize=(7, 5))
    ax=pt.half_violinplot( x = dx, y = dy, data = df, palette = pal, bw = .2, cut = 0.,
                        scale = "area", width = .6, inner = None, orient = ort)
    ax=sns.stripplot( x = dx, y = dy, data = df, palette = pal, edgecolor = "white",
                    size = 3, jitter = 1, zorder = 0, orient = ort)
    ax=sns.boxplot( x = dx, y = dy, data = df, color = "black", width = .15, zorder = 10,\
                showcaps = True, boxprops = {'facecolor':'none', "zorder":10},\
                showfliers=True, whiskerprops = {'linewidth':2, "zorder":10},\
                saturation = 1, orient = ort)
    plt.xticks(plt.xticks()[0], ["Experiment 1","Experiment 2"])
    ax.set_xlabel("")
    ax.set_ylabel("Proportion of Valid Data")
    plt.savefig('out/prop_valid_data_first20_'+condition+'_idealised_per_experiment_raincloud+'+dataset+'.pdf', bbox_inches='tight')

print("Comparing all data (both conditions combined)")
exp1 = df[df['exp']==1]
exp2 = df[df['exp']==2]
valid_proportion_idealised_raincloud(df,"both")
hypothesis_valid_proporition(exp1, exp2)

print("Comparing game conditions")
gamedf = df[df['version'] == "game"]
game_exp1 = gamedf[gamedf['exp']==1]
game_exp2 = gamedf[gamedf['exp']==2]
valid_proportion_idealised_raincloud(gamedf,"game")
hypothesis_valid_proporition(game_exp1, game_exp2)

print("Comparing control conditions")
controldf = df[df['version'] == "control"]
control_exp1 = controldf[controldf['exp']==1]
control_exp2 = controldf[controldf['exp']==2]
valid_proportion_idealised_raincloud(controldf,"control")
hypothesis_valid_proporition(control_exp1, control_exp2)