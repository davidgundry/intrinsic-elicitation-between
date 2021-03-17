# There are big problems doing it this way. Deciding grammar by relative order is way
# more complicated than the hardcoded method I used, so the results we get here
# are not at all reliable.

from get_moves import moves_by_user, Categories
from grammar_decider import RelativeOrder
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from scipy.stats import chisquare
from itertools import combinations
import numpy as np
from statsmodels.sandbox.stats.multicomp import multipletests

pio.templates.default = "simple_white"
dir = "intrinsic-elicitation-between/"

#moves_exp1 = all_moves("data/data_exp1.json", correct_form=True, coded=True)
#moves_exp2 = all_moves("data/data_exp2.json", correct_form=True, coded=True)
#moves = moves_exp1 + moves_exp2

moves_exp1_user = moves_by_user(dir+"data/data_exp1.json", correct_form=True, coded=True)
moves_exp2_user = moves_by_user(dir+"data/data_exp2.json", correct_form=True, coded=True)
moves_user = moves_exp1_user + moves_exp2_user

def relative_order_analysis(moves, name):
    print("\nAnlysing Experiment ", name)
    grammar_match_scores = []
    no_best = 0
    for u in moves:
        ro = RelativeOrder()
        grammars = ro.grammar(u)
        if len(grammars) != 1:
            no_best+=1
            print(grammars)
        else:
            grammar_match_scores.append(grammars[0].value)
        # TODO: Prob: what if two grammars with equal score?
        p = []
    print(no_best, "excluded because no single best grammar")


    counts, bins = np.histogram(grammar_match_scores, 24)
    bins = [i for (i) in range(24)]
    fig = px.bar(x = bins, y=counts, labels={'x':'grammar', 'y':'count'})
    fig.write_image(dir+"out/barchart_best_grammar_"+ name +".png")
    print("Grammar counts:", counts)

    print("\nOne-way Chi-Square test to assess goodness of fit of distribution of detected"+
            "\ngrammar against null hypothesis that grammars equally likely."+
            "\nHypothesis: grammars are not equally likely")
    c, p = chisquare(counts)
    print("X^2 = ", c, "p =", p)


    print("Post-hoc Chi-Square test")
    #all_combinations = list(combinations(bins, 2)) # If we wanted to compare every possible combination
                                                    # of grammars, this is how we would do it. But
                                                    # most of these are not of interest to us at all.
    combinations_20 = [[20, i] for (i) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23]] # 20: scfn
    combinations_23 = [[23, i] for (i) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22]] # 23: sfcn
    all_combinations = combinations_20 + combinations_23
    p_vals, chisq_vals = [], []
    for comb in all_combinations:
        c, p = chisquare([counts[comb[0]], counts[comb[1]]])
        chisq_vals.append(c)
        p_vals.append(p)

    reject_list, corrected_p_vals = multipletests(p_vals, method='bonferroni')[:2]
    print("\ngrammarA\tgrammarB\tChiSq\toriginal p-value\tcorrected p-value\treject?")
    for comb, x_val, p_val, corr_p_val, reject in zip(all_combinations, chisq_vals, p_vals, corrected_p_vals, reject_list):
        print(comb[0],comb[1], "\t", x_val, "\t", p_val, "\t", corr_p_val, "\t", reject)
    

    _summary_stat_moves(moves)
    #_create_heatmap(ro.pairs_prop)
    
def _create_heatmap(pairs_prop, name):
    z_text = [[str(y) for y in x] for x in pairs_prop]
    fig = go.Figure(data=go.Heatmap(
                    z=pairs_prop,
                    x=["size","colour", "filled", "noun"],
                    y=["size","colour", "filled", "noun"],
                    hoverongaps = False))
    fig.update_xaxes(title_text="After")
    fig.update_yaxes(title_text="Before")
    fig.show()
    fig.write_image(dir+"out/heatmap_relative_order_" + name + ".png")

def _summary_stat_moves(moves):
    count_ordered,noun_initial, noun_final = 0, 0, 0 
    for u in moves:
        for m in u:
            ordered = True
            for i, w in enumerate(m):
                if (i > 0):
                    if m[i].value < m[i-1].value:
                        ordered = False
            if ordered:
                count_ordered += 1
            if m[0] == Categories.Noun:
                noun_initial+=1
            if m[2] == Categories.Noun:
                noun_final+=1

    print("Correct Form (Total):", len(moves), len(moves)/len(moves))
    print("Grammatical:", count_ordered, count_ordered/len(moves))
    print("Noun Initial:", noun_initial, noun_initial/len(moves))
    print("Noun Final:", noun_final, noun_final/len(moves))

relative_order_analysis(moves_exp1_user, "exp1")
relative_order_analysis(moves_exp2_user, "exp2")
relative_order_analysis(moves_user, "expboth")
