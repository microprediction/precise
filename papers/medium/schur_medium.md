<!--
MEDIUM PUBLISHING NOTES (delete before posting)
- Medium has no native math. The three equations are pre-rendered PNGs in ./img/.
  Where you see  [[IMAGE: img/xxx.png]]  drag that file into Medium at that spot.
- White background, hi-res, so they read in both light and dark mode.
- Title/subtitle are the first two lines; set them as Title and Subtitle in Medium.
-->

# Remind me again why we trust the covariance likelihood in high dimensions

### One dial that bridges the full and the block-diagonal likelihood — and tells you where to set it

Suppose I hand you a covariance matrix and ask whether it's any good. The textbook answer, the one you'd be slightly embarrassed to argue against, is to score it by the likelihood it assigns to fresh data. For a Gaussian that's this:

[[IMAGE: img/eq_likelihood.png]]

It's a strictly proper scoring rule. It's the thing maximum likelihood is built to chase. By every classical argument it is simply correct — and in low dimensions it is.

So here's the awkward part. Look at where that expression spends its attention. Both terms are run by the *smallest* eigenvalues of the estimate: the log-determinant marches off to minus infinity as any eigenvalue heads for zero, and the inverse blows up in the same breath. Now put yourself in the regime everyone actually works in, where you have roughly as many variables as data points. The small eigenvalues collapse toward zero and, worse, become impossible to pin down — they're noise wearing a signal's clothes. The likelihood then bets its entire verdict on the part of the matrix it understands least.

You can guess how that goes. In a rigged experiment where I know which of two estimates is genuinely better — I can compute the true divergence, because I built the truth — the held-out likelihood picks the better one about 45% of the time. A coin would do better. Meanwhile the dull, inversion-free judges, plain Frobenius distance and the like, hum along around 85%. The most principled score we have is the one that fails.

If you've ever built a minimum-variance portfolio you've met this ghost before. The weights are proportional to the inverse covariance times a vector of ones, and they famously detonate in high dimensions — "error maximization," people call it. Same inverse. Same small eigenvalues. Same disaster. The fix everyone reaches for is to stop trusting that raw inverse. The interesting question isn't *whether* to stop trusting it; it's whether you can stop trusting it *by degrees*, with a single honest knob, instead of throwing the whole thing out.

You can, and the knob has been hiding in plain sight.

### The likelihood was a sum all along

Here's the one fact everything rests on. Split your variables into blocks and the Gaussian likelihood factors — exactly, no approximation — into a sum of block-conditional pieces. Each block gets scored given the earlier ones, through a quantity called the Schur complement, and the only matrices that ever get inverted are the small conditioning blocks. This is the machinery underneath half of spatial statistics (the Vecchia approximation, Gaussian–Markov random fields) without anyone calling it that.

I've made no approximation yet. I've just rewritten the likelihood in a form with a handle on it. And now I turn the handle. Damp the cross-block coupling by a single number γ between 0 and 1:

[[IMAGE: img/eq_gamma_bridge.png]]

At γ = 1 you have the full likelihood back, fragile and all. At γ = 0 each block is scored on its own, ignoring the others entirely — that's the block-diagonal, or *composite*, likelihood, the robust-but-blind option. Everywhere in between is the new thing, and it's the only setting that's better conditioned than both ends, because damping lifts exactly the small eigenvalues that wrecked the full likelihood. I call it the Schur pseudo-likelihood, and the name earns its keep: for any γ short of 1 it isn't a normalized probability, just a sum of perfectly good block scores that don't agree on a single joint distribution. That's a feature. You score with it; you don't fit with it.

If "interpolate between the full thing and the block-diagonal thing with one parameter" rings a bell, it should. That is precisely how Schur-complementary portfolios bridge the minimum-variance portfolio and hierarchical risk parity. It's the same dial on the same Schur complement — I've just stolen it from allocation and pointed it at evaluation.

### So where do you set it?

This is the part I'm pleased about. The dial controls how much to trust the estimated coupling, and "how much should I trust something I measured noisily" has a real answer. Work it out in the simplest case — predict one block from another, estimate the relationship from n samples — and the optimal γ falls out in closed form:

[[IMAGE: img/eq_gamma_star.png]]

Stare at it for a second and the whole argument is sitting right there. That ρ² is the strength of the coupling; the optimal γ is its *reliability* — the signal-to-total ratio, a Wiener filter, James–Stein shrinkage, whatever name you grew up with. It climbs toward 1 as you get more data or the coupling gets stronger (go ahead, trust it, use the full likelihood). It sinks toward 0 as the coupling dissolves into noise (ignore it, go block-diagonal). And it sits in the interior exactly when the coupling is worth something but not everything — which, in high dimensions, is almost always.

### The honest part

I'd be doing the thing I complained about at the top if I oversold this, so: the closed form above is the optimum for *using* the dial to clean an estimate, the well-behaved case. The high-dimensional question of which γ best *grades* competing estimates is only half-settled — I can write down the variance term that makes the full likelihood explode (it grows like one over the fourth power of the smallest eigenvalue, which you can watch happen), but the other half of that story is genuinely harder and I don't have it in closed form yet. An interior γ wins decisively when the signal lives inside the blocks and the cross-block coupling is shared noise; it doesn't buy you anything when the coupling is either perfectly reliable or pure garbage. That's not a hedge, it's the actual shape of the result, and it's falsifiable: find an interior optimum where the coupling is known to be perfectly reliable and you've sunk it.

The code is a `pip install precise` away, the dial included; the full derivations, the canonical-correlation generalization, and the Godambe-information bookkeeping are in the paper. None of which changes the one line I'd want you to leave with: in high dimensions you are rewarded, over and over, for not trusting the raw inverse — and now there's a number that tells you exactly how much to distrust it.

---

*The paper (with all the math that didn't survive the trip to Medium): [Schur Covariance Evaluation — A Principled Pseudo-Likelihood in High Dimensions](https://github.com/microprediction/precise/blob/main/papers/schur_likelihood_paper.pdf). Code: [microprediction/precise](https://github.com/microprediction/precise). The original Schur theory was developed with the support of Intech Investments.*
