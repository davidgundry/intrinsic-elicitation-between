from get_moves import moves_by_user
from grammar_decider import MostMatched
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import numpy as np
from scipy.stats import chisquare
from itertools import combinations
from statsmodels.sandbox.stats.multicomp import multipletests
import math

pio.templates.default = "simple_white"

def best_grammar_most_matched(moves, name):
    print("\n==================================")
    print("Analysing Experiment ", name)
    print("==================================")

    bins_all_inputable = ["sfc", "sfn", "scf", "scn", "snf", "snc", "fsc", "fsn", "fcs", "fcn", "fns", "fnc", "csf", "csn", "cfs", "cfn", "cns", "cnf", "nsf", "nsc", "nfs", "nfc", "ncs", "ncf"]
    orders_all_inputable = [[0,1,2], [0,1,3], [0,2,1], [0,2,3], [0,3,1], [0,3,2], [1,0,2], [1,0,3], [1,2,0], [1,2,3], [1,3,0], [1,3,2], [2,0,1], [2,0,3], [2,1,0], [2,1,3], [2,3,0], [2,3,1], [3,0,1], [3,0,2], [3,1,0], [3,1,2], [3,2,0], [3,2,1]]
    bins_correctform = ["sfn", "scn", "snf", "snc", "fsn", "fcn", "fns", "fnc", "csn", "cfn", "cns", "cnf", "nsf", "nsc", "nfs", "nfc", "ncs", "ncf"]
    orders_correctform = [[0,1,3], [0,2,3], [0,3,1], [0,3,2], [1,0,3], [1,2,3], [1,3,0], [1,3,2], [2,0,3], [2,1,3], [2,3,0], [2,3,1], [3,0,1], [3,0,2], [3,1,0], [3,1,2], [3,2,0], [3,2,1]]

    counts = moves_with_order(moves, orders_correctform)

    fig = px.bar(x = bins_correctform, y=counts, labels={'x':'order', 'y':'count'})
    fig.write_image(dir+"out/barchart_order_counts_"+ name +".png")


    print("\nOne-way Chi-Square test to assess goodness of fit of distribution of detected"+
            "\ngrammar against null hypothesis that grammars equally likely."+
            "\nHypothesis: grammars are not equally likely")
    c, p = chisquare(counts)
    print("ChiSquared =", c, "p =", p, "df =", len(counts)-1)

    print("\nPost-hoc Chi-Square test")
    all_combinations = list(combinations([i for (i) in range(len(counts))], 2))

    p_vals, chisq_vals = [], []
    for comb in all_combinations:
        c, p = chisquare([counts[comb[0]], counts[comb[1]]])
        chisq_vals.append(c)
        p_vals.append(p)

    # Correcting using Holm–Bonferroni correction method
    reject_list, corrected_p_vals = multipletests(p_vals, method='holm')[:2]
    print("A\B\tChiSq\cor. p-value\tsig.")
    for comb, x_val, p_val, corr_p_val in zip(all_combinations, chisq_vals, p_vals, corrected_p_vals):
        print(comb[0],"\t", comb[1], "\t", round(x_val,2), "\t", round(corr_p_val,3), "\t", asterisks(corr_p_val))


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
best_grammar_most_matched(moves_exp1_game_user, "exp1_game")
best_grammar_most_matched(moves_exp2_game_user, "exp2_game")

moves_exp1_tool_user = moves_by_user(dir+"data/data_exp1.json", "Tool", correct_form=True, coded=True)
moves_exp2_tool_user = moves_by_user(dir+"data/data_exp2.json", "tool", correct_form=True, coded=True)
best_grammar_most_matched(moves_exp1_tool_user, "exp1_tool")
best_grammar_most_matched(moves_exp2_tool_user, "exp2_tool")