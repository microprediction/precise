# precise skills

Self-contained skills for using the [`precise`](https://github.com/microprediction/precise)
package — online (incremental) covariance and correlation estimation. Each is written so an
agent can act on it without further context: trigger, install, copy-pasteable code, expected
output, guardrails.

| Skill | Use it when… |
|---|---|
| [estimate-online-covariance](estimate-online-covariance/SKILL.md) | you need a covariance/correlation/precision matrix updated per observation (or a `partial_fit` drop-in for `sklearn.covariance`) |
| [choose-covariance-estimator](choose-covariance-estimator/SKILL.md) | you are unsure *which* estimator fits the data's dimension, conditioning, or tails |
| [score-covariance-estimate](score-covariance-estimate/SKILL.md) | you need to judge or rank covariance estimates out-of-sample (especially in high dimensions) |
| [keyed-dynamic-universe](keyed-dynamic-universe/SKILL.md) | observations are dicts keyed by name and the set of names changes over time |
| [assess-covariance-method](assess-covariance-method/SKILL.md) | you are evaluating a **new/proposed** estimator or scoring rule and want a rigorous, honest verdict |

Install for all of these: `pip install precise` (numpy-only core; add `[pandas]`, `[research]`,
or `[dev]` for extras). Docs: <https://precise.microprediction.org>.
