# Bird contest simulation

Simulates pairwise competitive contests between individuals with genetic load
L ~ Exponential(1), linking Morton et al.'s lethal-equivalents framework to a
logistic/binomial model of contest outcomes.

## Model
- Fitness: w = exp(-L)
- Single-trial win probability: P(A wins) = 1 / (1 + exp(-ΔL)), ΔL = L_B - L_A
- Each "contest" is a best-of-m majority vote over m independent trials (m must be odd, to avoid ties)
- `error` adds independent per-trial noise (representing match-day conditions —
  injury, fatigue, weather) to each bird's effective load before that trial

## Key functions
- `Contest()` — runs one m-trial contest, either between a random pair from the
  population, or a synthetic pair with a specified ΔL
- `Plot_prob_against_Ldiff` / `Plot_prob_against_wdiff` — P(A wins) vs load/fitness difference
- `Plot_prob_against_m` — P(A wins) vs number of trials per contest, for a fixed ΔL
- `Plot_prob_against_error` — P(A wins) vs noise level, for a fixed ΔL and m
- `Binomial_curve` — exact theoretical prediction (binomial CDF), for comparison against simulation

## Usage
See `Experiments.ipynb` for example calls to each plotting function.
