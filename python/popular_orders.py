from get_moves import moves_by_user
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import numpy as np
import pandas as pd
from scipy.stats import chisquare, chi2_contingency, fisher_exact
from statsmodels.sandbox.stats.multicomp import multipletests
import math

pio.templates.default = "simple_white"

def best_grammar_most_matched(game, tool, name):
    print("\n==================================")
    print("Analysing Experiment ", name)
    print("==================================")

    bins_all_inputable = ["sfc", "sfn", "scf", "scn", "snf", "snc", "fsc", "fsn", "fcs", "fcn", "fns", "fnc", "csf", "csn", "cfs", "cfn", "cns", "cnf", "nsf", "nsc", "nfs", "nfc", "ncs", "ncf"]
    orders_all_inputable = [[0,1,2], [0,1,3], [0,2,1], [0,2,3], [0,3,1], [0,3,2], [1,0,2], [1,0,3], [1,2,0], [1,2,3], [1,3,0], [1,3,2], [2,0,1], [2,0,3], [2,1,0], [2,1,3], [2,3,0], [2,3,1], [3,0,1], [3,0,2], [3,1,0], [3,1,2], [3,2,0], [3,2,1]]
    bins_correctform = ["sfn", "scn", "snf", "snc", "fsn", "fcn", "fns", "fnc", "csn", "cfn", "cns", "cnf", "nsf", "nsc", "nfs", "nfc", "ncs", "ncf"]
    orders_correctform = [[0,1,3], [0,2,3], [0,3,1], [0,3,2], [1,0,3], [1,2,3], [1,3,0], [1,3,2], [2,0,3], [2,1,3], [2,3,0], [2,3,1], [3,0,1], [3,0,2], [3,1,0], [3,1,2], [3,2,0], [3,2,1]]

    countsTool = moves_with_order(tool, orders_correctform)
    countsGame = moves_with_order(game, orders_correctform)

    order = np.argsort(countsTool)
    orderedBins = [bins_correctform[i] for (i) in order[::-1]]
    orderedCountsTool = [countsTool[i] for (i) in order[::-1]]
    orderedCountsGame = [countsGame[i] for (i) in order[::-1]]

    bin = pd.Series(orderedBins + orderedBins, name="Word Order")
    cnt = pd.Series(orderedCountsGame + orderedCountsTool, name="Count")
    cnd = pd.Series(["game" for (i) in range(len(orderedCountsTool))] + ["tool" for (i) in range(len(orderedCountsTool))], name="condition")
    df = pd.concat([bin, cnt, cnd], axis=1)

    fig = px.bar(df, x = "Word Order", y="Count", color="condition", barmode='group')
    fig.write_image(dir+"out/barchart_order_counts_"+ name +".png")

    counts = orderedCountsGame
    print("\nOne-way Chi-Square test to assess goodness of fit of distribution of detected"+
            "\ngrammar against null hypothesis that word orders are equally likely."+
            "\nHypothesis: word orders are not equally likely")
    c, p = chisquare(counts)
    print("ChiSquared =", c, "p =", p, "df =", len(counts)-1)
    print("Number of inputs in game used = ", sum(orderedCountsGame))

    print("\nPost-hoc Chi-Square test, comparing grammatical orders against every other order." +
    "\nBut we're not interested in comparing between pairs of grammatical orders, or between pairs" +
    "\nof non-grammatical orders. If running this on new data, double check from the graph that the first three"
    "\norders are the grammatical ones.")
    combinations_0 = [[0, i] for (i) in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]]
    combinations_1 = [[1, i] for (i) in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]]
    combinations_2 = [[2, i] for (i) in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]]
    all_combinations = combinations_0 + combinations_1 + combinations_2

    p_vals, chisq_vals = [], []
    for comb in all_combinations:
        c, p = chisquare([counts[comb[0]], counts[comb[1]]])
        chisq_vals.append(c)
        p_vals.append(p)

    # Correcting using Holm–Bonferroni correction method
    reject_list, corrected_p_vals = multipletests(p_vals, method='holm')[:2]
    print("A\B\tChiSq\cor. p-value\tsig.")
    for comb, x_val, p_val, corr_p_val in zip(all_combinations, chisq_vals, p_vals, corrected_p_vals):
        print(orderedBins[comb[0]],"\t", orderedBins[comb[1]], "\t", round(x_val,2), "\t", round(corr_p_val,3), "\t", asterisks(corr_p_val))


def moves_with_order(moves, orders):
    bincats = [0] * len(orders)
    for u in moves:
        for move in u:
            for oi, o in enumerate(orders):
                falsified = False
                for i in range(3):
                    if o[i] != move[i].value:
                        falsified = True
                if not falsified:
                    bincats[oi] += 1
                    break
    return bincats

def asterisks(p_val):
    if math.isnan(p_val):
        return ""
    if p_val > 0.05:
        return "n.s."
    elif p_val < 1e-4:  
        return '****'
    elif p_val < 1e-3:
        return '***'
    elif p_val < 1e-2:
        return '**'
    else:
        return '*'


dir = "" #"intrinsic-elicitation-between/"
moves_exp1_game_user = moves_by_user(dir+"data/data_exp1.json", "Normal", correct_form=True, coded=True)
moves_exp2_game_user = moves_by_user(dir+"data/data_exp2.json", "normal", correct_form=True, coded=True)
moves_exp1_tool_user = moves_by_user(dir+"data/data_exp1.json", "Tool", correct_form=True, coded=True)
moves_exp2_tool_user = moves_by_user(dir+"data/data_exp2.json", "tool", correct_form=True, coded=True)
best_grammar_most_matched(moves_exp1_game_user, moves_exp1_tool_user,  "exp1")
best_grammar_most_matched(moves_exp2_game_user, moves_exp2_tool_user, "exp2")

