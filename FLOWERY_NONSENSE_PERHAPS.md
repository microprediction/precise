# Using Markowitz-Style Optimization for Bouquet Design

## Can We Apply Markowitz Directly?

> **Short answer:** Yes, you *can* cast bouquet design as a mean–variance problem, but it takes extra effort because beauty is not a simple, linear “return,” and aesthetic “risk” is tricky to define.

---

## 1 Mapping Markowitz Terms to Floral Design

| Markowitz term                     | Floral analogue                                             | How you might measure it |
|-----------------------------------|-------------------------------------------------------------|--------------------------|
| **Asset weight $w_i$**            | Proportion or count of stems of flower _i_                  | Decision variables (often integers) |
| **Expected return $\mu_i$**       | Average beauty contribution of one stem of flower _i_       | Crowd-sourced ratings, expert scores, ML predictions |
| **Covariance $\Sigma_{ij}$**      | Disharmony/clash between flowers _i_ and _j_               | Pairwise harmony scores, colour-wheel distance, shape-clash metrics |
| **Portfolio return $w^\top\mu$**  | Total predicted beauty                                      | Linear sum of contributions |
| **Portfolio risk $w^\top\Sigma w$** | Aggregate discordance risk (lack of unity)                 | Quadratic clash penalty |

**Continuous formulation**

$$
\begin{aligned}
\max_{w}\;& w^\top\mu \;-\;\lambda\,w^\top\Sigma w \\[4pt]
\text{s.t. }& \mathbf 1^\top w = 1,\quad w \ge 0
\end{aligned}
$$

---

## 2 Why Most Florists Don’t Stop Here

| Issue | Why it matters for bouquets |
|-------|-----------------------------|
| **Non-additive beauty** | Synergies and clashes are often *non-linear*. |
| **Risk ≠ variance** | A symmetric variance treats all deviations equally; humans don’t. |
| **Tiny integer portfolios** | 12–24 stems → an integer quadratic program, not the smooth QP Markowitz likes. |
| **Data burden** | Need an $N \times N$ clash matrix; expensive to collect. |
| **Beauty is multi-objective** | People like *unity **and** variety* simultaneously (an inverted-U curve). |

---

## 3 Making Markowitz Useful Anyway

1. **Rate single stems** → get $\mu_i$.  
2. **Rate pairs of stems** → build clash matrix $\Sigma$.  
3. **Add florist constraints**  
   * Integer counts  
   * Budget and stem limits  
   * Colour quotas, minimum greens, etc.  
4. **Solve the integer QP** (branch-and-bound or meta-heuristic).  
5. **Designer tweak pass** to fine-tune beyond the model.

---

## 4 Alternatives & Hybrids

* **Multi-objective genetic / flower-pollination algorithms** — naturally handle unity *and* variety.  
* **Black–Litterman-style priors** — blend expert views with crowd data.  
* **Robust or CVaR risk measures** — penalise ugly clashes more than mild disharmony.

---

### Bottom Line

Markowitz gives a **useful first-pass screener** of candidate bouquets, especially if you have rating data.  
For full realism, designers often switch to more flexible multi-objective heuristics that better capture the **unity-in-variety** principle people consistently find most beautiful.
