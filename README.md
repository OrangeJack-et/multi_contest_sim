# Repeated-contest simulation

How much does repeating a noisy contest amplify a small edge? This simulates
pairwise contests between individuals of unequal fitness and compares the
outcome with an exact binomial prediction.

**Headline result:** an individual with a 0.55 chance of winning a single
contest is dominant with probability 0.84 over a best-of-99, matching the
closed-form prediction with no fitted parameters.

Summer 2026 research project, University of East Anglia. Manuscript in
preparation.

## Model
- Each individual carries a realised load L ~ Exponential(1) and has fitness w = exp(-L)
- **Contest:** a single Bernoulli trial. P(A wins) = w_A / (w_A + w_B) = 1 / (1 + exp(-ΔL)), with ΔL = L_B - L_A
- **Dominance relation:** m contests between the same pair (m odd); the individual with the most wins is dominant
- **Error:** per-contest noise added to each individual's load before every contest, representing conditions on the day.

## Analytic prediction
With no error, the number of contests A wins is Binomial(m, P_A), so

    P(A dominant) = 1 - F(floor(m/2); m, P_A)

where F is the binomial CDF. Nothing is fitted.

## Results
- Simulation follows the analytic curve for every odd m from 1 to 99 (ΔL = 0.2, 10^4 dominance relations per point)
- At ΔL = 0.2: P = 0.55 for m = 1, rising to 0.841 for m = 99
- Error flattens the curve but repetition still recovers the edge: at m = 99 with error = 1

![Simulation against the analytic prediction](figures/fig2b.png)

## Code
- `Population_Simulation.py`: the model and plotting functions
  - `Contest()` runs one dominance relation of m contests, for a random pair or a synthetic pair with a set ΔL
  - `Plot_prob_against_Ldiff` / `Plot_prob_against_wdiff`: P(A dominant) against load or fitness difference
  - `Plot_prob_against_m`: P(A dominant) against number of contests, at fixed ΔL
  - `Plot_prob_against_error`: P(A dominant) against error level, at fixed ΔL and m
  - `Binomial_curve`: the analytic prediction
- `Experiments.ipynb`: reproduces every figure

## Running it
    pip install -r requirements.txt
    jupyter notebook Experiments.ipynb

## Background
The load model follows Morton et al.'s lethal-equivalents framework.
