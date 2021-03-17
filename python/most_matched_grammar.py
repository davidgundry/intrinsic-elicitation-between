# This script tries to statistically show which grammar is most commonly used by participants
# We work out the most likely grammar for a participant by seeing which grammar the plurality of
# their inputs match with. Then see if one grammar stands out as being the one most participants
# most commonly match with.
#
# It has a problem that multiple grammars can have the same score, so we don't know to which
# category to assign that player. To resolve this we assign a participant in multiple categories
# proportionally to each category. Eg. if they are in 3, they count 1/3 toward each.
#
# To check which grammar is most commonly used, could we do multiple testing and correct using 
# Fasle Discovery Rate, Benjamini/Hochberg. But this would mean controlling the error rate. So
# some proportion of our rejected nulls would be incorrect. We'd have more Type I errors and fewer
# type II. If we control for the family-wise error rate then we can have more confidence in our
# rejected nulls, as there is only a small % chance that we have _any_ Type I errors. As we want to give
# confidence that the standard grammar is preferred over _everything_ else, we want to be confident
# that it is unlikely for _any_ test to be wrong. Rather than thinking: "standard grammar is popular,
# but it's possible that we're _not_ better than % of the other grammars."

# We're using the Holm–Bonferroni. This ranks our p values in order, then divides our alpha between
# them on the basis of this ranking (unlike Bonferroni where the division is equal). It controls
# family-wise error rate at our alpha of 0.05.

# TODO: can I do post-hoc chi-square for individual users to decide which
# grammar is the best?

# If you add them up, it looks like about 40% of the time, one of the top 2
# grammars are chosen. So a plausible correct grammar is elicited 40% of
# the time. #TODO: Script this?

from get_moves import moves_by_user
from grammar_decider import MostMatched
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import numpy as np
from scipy.stats import chisquare
from itertools import combinations
from statsmodels.sandbox.stats.multicomp import multipletests

pio.templates.default = "simple_white"

def best_grammar_most_matched(moves, name, use20):
    print("\n==================================")
    print("Analysing Experiment ", name)
    print("==================================")
    matches_per_grammar_per_user, user_grammars = get_matches(moves)
    bins = ["fcns",  "cfns",  "nfcs",  "fncs",  "cnfs",  "ncfs",  "ncsf",  "cnsf",  "sncf",  "nscf",  "csnf",  "scnf",  "sfnc",  "fsnc",  "nsfc",  "snfc",  "fnsc",  "nfsc",  "cfsn",  "fcsn",  "scfn",  "csfn",  "fscn", "sfcn"]
    prop_analysis(name, bins, matches_per_grammar_per_user)
    best_grammar_analysis(name, bins, user_grammars, use20)

def get_matches(moves):
    matches_per_grammar_per_user, user_grammars = [], []
    more_than_one_best, participants = 0, 0
    for u in moves:
        participants += 1
        ro = MostMatched().create(u)
        if len(ro.grammars) > 1:
            more_than_one_best += 1
        user_grammars.append(ro.grammars)
        matches_per_grammar_per_user.append(ro.matches)
    print(participants, "participants")
    print(more_than_one_best, "participants had no single best grammar")
    return matches_per_grammar_per_user, user_grammars

def prop_analysis(name, bins, matches_per_grammar_per_user):
    print("\nAnalysing Proportions")
    print("----------------------------------")
    print("""Compare proportional usage of grammars within individuals. Rather than choosing
one per user and dividing when equal best, each user contributes proportionally to all
grammars they used, to the amount they used them. This answers the question 'What grammar
is most commonly collected by the game if we control for number of user inputs?', or 'What
grammar would be likely to decide on given a single input?' This is going to increase noise,
as many grammars are rarely if ever most commonly used, but are used occasionally. These small
proportions will add up having the effect of flattening the distirbution. This is exacerbated
because moves (3 words long) will match multiple possible grammars (4 words long), so groups
of grammars are going to be correlated. Even if one grammar was 'intended' it will pull
up closely related grammars as well.""")
    
    proportional_match_scores = []
    for u in matches_per_grammar_per_user:
        pu = []
        total_matches = sum(u)
        for i in u:
            pu.append(i/total_matches)
        proportional_match_scores.append(pu)

    prop_counts = [0] * 24
    for u in proportional_match_scores:
        for i, p in enumerate(u):
            prop_counts[i] += p
    print("Proportional counts:", prop_counts)

    # Create heatmap to help us understand our data more
    fig = go.Figure(data=go.Heatmap(
                        z=proportional_match_scores,
                        hoverongaps = False))
    fig.write_image(dir+"out/heatmap_prop_matching_"+ name +".png")

    print("\nOne-way Chi-Square test to assess goodness of fit of distribution of detected"+
            "\ngrammar against null hypothesis that grammars equally likely."+
            "\nHypothesis: grammars are not equally likely")
    c, p = chisquare(prop_counts)
    print("ChiSquared =", c, "p =", p, "df =", len(prop_counts)-1)

    fig = px.bar(x = bins, y=prop_counts, labels={'x':'grammar', 'y':'count'})
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.write_image(dir+"out/barchart_prop_matching_"+ name +".png")


def best_grammar_analysis(name, bins, user_grammars, use20):
    print("\nAnalysing Best-Grammar Data")
    print("------------------------------")
    print("""Where we've made a decision as to what each's user's grammar is,
see how our judgements are distirbuted. Do we mostly decide users use x grammar?
This way, the question is 'What grammars would we decide upon if we were to use the
game as a measurement tool and how often would that decision match what we expect?'
This way we can detect if one grammar is always/usually a little bit more common.
If there is no such grammar, we would expect our 'best' grammar judement to be noisy
and not reveal one clear winner. This makes sense if one 'intended' grammar can pull
up other similar grammars because they are also compatable with the same (3-word) input.
We expect the intended grammar to be always highest, but for correlated grammars to always
be close behind.\n""")
    best_counts = [0]*24
    for u in user_grammars:
        for g in u:
            best_counts[g.value] += 1/len(u)
    print("Grammar counts:", best_counts)

    print("\nOne-way Chi-Square test to assess goodness of fit of distribution of detected"+
            "\ngrammar against null hypothesis that grammars equally likely."+
            "\nHypothesis: grammars are not equally likely")
    c, p = chisquare(best_counts)
    print("ChiSquared =", c, "p =", p, "df =", len(best_counts)-1)

    print("\nPost-hoc Chi-Square test")
    #all_combinations = list(combinations([i for (i) in range(24)], 2)) # If we wanted to compare every possible combination
                                                    # of grammars, this is how we would do it. But
                                                    # most of these are not of interest to us at all.
    if (use20):
        combinations_20 = [[20, i] for (i) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23]] # 20: scfn
        combinations_23 = [[23, i] for (i) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22]] # 23: sfcn
        all_combinations = combinations_23 + combinations_20
    else:
        combinations_23 = [[23, i] for (i) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 21,22]] # 23: sfcn
        all_combinations = combinations_23

    p_vals, chisq_vals = [], []
    for comb in all_combinations:
        c, p = chisquare([best_counts[comb[0]], best_counts[comb[1]]])
        chisq_vals.append(c)
        p_vals.append(p)

    # Correcting using Holm–Bonferroni correction method
    reject_list, corrected_p_vals = multipletests(p_vals, method='holm')[:2]
    print("grammarA\tgrammarB\tbinB\tChiSq\tcorrected p-value\tsig.")
    for comb, x_val, p_val, corr_p_val in zip(all_combinations, chisq_vals, p_vals, corrected_p_vals):
        print(comb[0],"\t", comb[1], "\t", bins[comb[1]], "\t", round(x_val,2), "\t", round(corr_p_val,3), "\t", asterisks(corr_p_val))

    
    fig = px.bar(x = bins, y=best_counts, labels={'x':'grammar', 'y':'count'}) #text=list(map(asterisks, corrected_p_vals)))
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.write_image(dir+"out/barchart_best_matching_"+ name +".png")


def asterisks(p_val):
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
best_grammar_most_matched(moves_exp1_game_user, "exp1_game", False)
best_grammar_most_matched(moves_exp2_game_user, "exp2_game", True)

moves_exp1_tool_user = moves_by_user(dir+"data/data_exp1.json", "Tool", correct_form=True, coded=True)
moves_exp2_tool_user = moves_by_user(dir+"data/data_exp2.json", "tool", correct_form=True, coded=True)
best_grammar_most_matched(moves_exp1_tool_user, "exp1_tool", False)
best_grammar_most_matched(moves_exp2_tool_user, "exp2_tool", True)