
library("pwr")

# These calulations come after observing that valid data is much lower in the game condition in experiment 2,
# Even if we control for only taking the first 20 inputs in each case. There are not that many big differences
# between the game conditions of the two experiments. So I think this might be because of the switch from random
# placement to column placement of buttons.

observedEffectSizePropValidDataGameBetweenExps <- 0.5101550187824632

# PropValidData (Observed)
alt <- "two.sided" # We could find either is the case. If so we might be able to make an explanation based on
                    # Intrinsic Elicitaiton. While we have a direction we expect, it going the other way is
                    # still a potentially interesting result
pwr.t.test(d = observedEffectSizePropValidDataGameBetweenExps, sig.level = 0.05, power = 0.8, alternative = alt)

# PropValidData (Minimum effect size of interest)
alt <- "two.sided"
effectSizeOfInterest <- cohen.ES(test = "t", size = "small")$effect.size
                 # We would be interested in relatively small differences in valid data. 
pwr.t.test(d = effectSizeOfInterest, sig.level = 0.05, power = 0.8, alternative = alt)

# Sample size required, based on observed data is 61.29 per group. We will round this to 62 making an
# overall required sample size of 124. If we try and get any potentially interesting effect we'd need
# ~800 people which would be far too expensive to run.
