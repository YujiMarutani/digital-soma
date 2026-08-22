# Digital Soma — Simulation Layer

Reproducible computational experiments for the Digital Soma Friction Regulation Model.

---

## 1. Overview

This directory contains the computational simulation layer of the Digital Soma project.

It implements and evaluates a minimal dynamical system designed to explore:

- friction regulation
- transformative capacity
- human agency
- AI intervention
- homeostatic regulation
- agency compression
- emergent civilizational regimes

The simulation layer is **not intended to reproduce human psychology**.

It is a boundary-condition model designed to test whether Digital Soma-like regimes are mathematically reachable under explicit parameter conditions.

The central methodological question is:

> **Under what dynamical conditions can AI-mediated friction regulation produce sustained reductions in transformative capacity and human agency?**

---

## 2. Simulation Stack

The Digital Soma simulation pipeline consists of progressively deeper experiments.

```text
DIGITAL SOMA SIMULATION STACK

01 — Single-Agent Friction Regulation
     Core dynamical system
     Friction → Capacity → Agency → Environment
          ↓
02 — F_target Parameter Sweep
     Policy-space exploration
     F_target = 0.05 → 0.95
          ↓
02b — Sensitivity / Existence Search
     1,620-run factorial exploration
     λ, r_H, μ, γ, k_p, F_target
          ↓
03 — Lambda Continuation
     High-resolution agency-compression trajectory
     λ = 0.005 → 0.200
          ↓
03b — Critical Boundary Analysis
     Operational regime boundaries
     λ_trap ≈ 0.05675
     λ_agency ≈ 0.09725
          ↓
03c — Temporal Dynamics
     Planned
     Path dependence / hysteresis / temporal ordering
```

The experiments are not designed to confirm the Digital Soma hypothesis.

They are designed to determine **which regimes are reachable, under which parameter conditions, and whether those regimes are dynamically stable or merely threshold-defined.**

---

## 3. Canonical Model

The simulation layer implements the Friction Regulation Model.

### Friction

$begin:math:display$
F\(t\)\=\\alpha G\+\\beta E\(t\)\-\\gamma A\(t\)
$end:math:display$

where:

- $begin:math:text$F\(t\)$end:math:text$ = experienced friction
- $begin:math:text$G$end:math:text$ = biological / behavioral propensity
- $begin:math:text$E\(t\)$end:math:text$ = environmental stress
- $begin:math:text$A\(t\)$end:math:text$ = AI intervention
- $begin:math:text$\\alpha\,\\beta\,\\gamma$end:math:text$ = model parameters

### Transformative Capacity

$begin:math:display$
C\(F\)\=C\_\{\\max\}
\\exp\\left\[
\-\\frac\{\(F\-F\^\*\)\^2\}\{2\\sigma\_F\^2\}
\\right\]
$end:math:display$

where:

- $begin:math:text$C\(F\)$end:math:text$ = transformative capacity
- $begin:math:text$F\^\*$end:math:text$ = modeled optimal friction
- $begin:math:text$\\sigma\_F$end:math:text$ = width of the adaptive region

### AI Intervention

$begin:math:display$
\\dot A\=k\_p\(F\-F\_\{\\text\{target\}\}\)
$end:math:display$

AI intervention therefore operates as a feedback controller attempting to regulate experienced friction toward a target.

### Human Agency

$begin:math:display$
\\dot H\=r\_H\-\\lambda A H\+\\mu C
$end:math:display$

where:

- $begin:math:text$H$end:math:text$ = human agency
- $begin:math:text$r\_H$end:math:text$ = agency regeneration
- $begin:math:text$\\lambda$end:math:text$ = agency compression rate
- $begin:math:text$A$end:math:text$ = AI intervention
- $begin:math:text$\\mu$end:math:text$ = transformative contribution

Full model specification:

```text
../model/01-friction-regulation-model.md
```

---

## 4. Experiments

### 01 — Single-Agent Friction Regulation

Establishes the baseline dynamical system.

Primary objectives:

- establish model behavior
- evaluate friction regulation
- observe transformative-capacity dynamics
- establish the controller response
- examine human-agency dynamics

---

### 02 — F_target Parameter Sweep

Explores:

```text
F_target = 0.05 → 0.95
step = 0.05
```

Primary observables:

- mean friction
- transformative capacity
- human agency
- AI intervention
- adaptive-window occupancy
- final state variables

Main finding:

> Lower friction targets increase AI intervention and can suppress transformative capacity, while human agency remains near saturation under the original parameterization.

---

### 02b — Sensitivity / Existence Search

A full factorial exploration of:

```text
λ
r_H
μ
γ
k_p
F_target
```

Total:

```text
1,620 runs
```

The purpose was not parameter fitting.

It was an **existence search**:

> Can Agency Compression and Homeostatic Trap occur anywhere within a systematically defined parameter space?

Result:

```text
Adaptive Zone          810 / 1620  = 50.0%
Intermediate            402 / 1620  = 24.8%
Capacity Suppression    351 / 1620  = 21.7%
Homeostatic Trap         54 / 1620  =  3.3%
Agency Compression        3 / 1620  =  0.2%
```

Conclusion:

> Agency Compression and Homeostatic Trap are mathematically reachable but occupy a restricted region of parameter space.

---

### 03 — Lambda Continuation

The parameter configuration associated with strong compression is fixed while $begin:math:text$\\lambda$end:math:text$ is swept continuously.

```text
λ = 0.005 → 0.200
```

The purpose is to determine how human agency changes as the strength of the AI→agency compression channel increases.

The resulting trajectory shows continuous agency degradation.

---

### 03b — Critical Boundary Analysis

A high-resolution continuation analysis was performed around the transition region.

The main operational boundaries were:

```text
Homeostatic Trap

λ ≈ 0.05675
```

and:

```text
Mean Agency Compression

λ ≈ 0.09725
```

The state variables remained continuous across the sampled boundary regions.

Therefore:

> **No genuine dynamical bifurcation has been demonstrated in the current model.**

The observed boundaries are operational threshold crossings along a continuous agency-degradation trajectory.

This distinction is methodologically important.

---

### 03c — Temporal Dynamics

Planned experiment.

Objectives:

- examine $begin:math:text$F\(t\)$end:math:text$
- examine $begin:math:text$C\(t\)$end:math:text$
- examine $begin:math:text$H\(t\)$end:math:text$
- examine $begin:math:text$A\(t\)$end:math:text$
- identify temporal ordering
- test path dependence
- test hysteresis
- distinguish transient compression from sustained compression

---

## 5. Operational Regimes

The simulation layer uses fixed regime definitions.

| Regime | Operational Condition |
|---|---|
| Adaptive Zone | High transformative capacity + preserved agency + sufficient adaptive-window occupancy |
| Comfort Optimization | Low mean friction + sustained AI intervention |
| Capacity Suppression | $begin:math:text$C \< 0\.50C\_\{\\max\}$end:math:text$ |
| Agency Compression | $begin:math:text$\\bar H \\leq 0\.70$end:math:text$ or $begin:math:text$H\_\{final\}\\leq0\.65$end:math:text$ |
| Homeostatic Trap | Comfort Optimization + Capacity Suppression + Agency Compression |

These definitions remain fixed across experiments.

Thresholds are not modified to produce a desired narrative.

---

## 6. Key Findings

### Transformative Capacity

Transformative capacity follows an inverted-U relationship with friction.

However, this relationship is **structurally imposed by the model function**.

It should therefore not be interpreted as an emergent empirical discovery.

---

### AI Intervention

AI intervention increases when the controller attempts to maintain friction below the system's natural equilibrium.

This behavior emerges from the feedback mechanism.

---

### Agency Compression

Under the original parameterization:

```text
H ≈ 1
```

Agency Compression therefore does not emerge naturally from the initial model.

Sensitivity analysis demonstrates that compression becomes reachable when the compression term becomes sufficiently strong relative to agency regeneration and transformative gain.

---

### Homeostatic Trap

The sensitivity experiment identified:

```text
54 / 1620 runs
≈ 3.3%
```

as Homeostatic Trap.

Therefore:

> **Homeostatic Trap is possible but not generic within the explored parameter space.**

---

### Transition Structure

High-resolution lambda continuation found no discontinuous state transition.

The current evidence supports:

```text
Continuous Agency Degradation
        ↓
Operational Threshold Crossing
        ↓
Regime Classification
```

rather than:

```text
Bifurcation
    ↓
Sudden State Transition
```

---

## 7. Current Regime Interpretation

The current computational model supports the following hierarchy:

```text
AI Intervention
       ↓
Friction Regulation
       ↓
Experienced Friction
       ↓
Transformative Capacity
       ↓
Human Agency
       ↓
Potential Homeostatic Trap
```

The model does not establish that this sequence necessarily occurs in real civilization.

It establishes that the corresponding state relationships can be represented and explored computationally.

---

## 8. Results

Current simulation outputs are stored in the repository's results layer.

```text
results/
├── 01-parameter-sweep-results.csv
├── 02b-sensitivity-results.csv
├── 03-bifurcation-results.csv
└── 03b-critical-boundary-results.csv
```

Each result file should be interpreted together with the corresponding simulation script and model version.

---

## 9. Reproducibility

### Requirements

- Python 3.10+
- NumPy
- Pandas

Matplotlib may be required for optional visualization workflows.

### Run Experiments

From the `simulation/` directory:

```bash
python 01-single-agent-friction-regulation.py
python 02-parameter-sweep.py
python 02b-sensitivity-analysis.py
python 03-bifurcation-analysis.py
python 03b-critical-boundary-analysis.py
```

Experimental outputs should be written to the designated results directory.

---

## 10. Research Principles

The simulation layer follows several methodological principles.

### No Narrative-Driven Parameter Tuning

Parameters should not be adjusted merely to generate a desired outcome.

### Existence Before Interpretation

A regime must first be demonstrated computationally before it is interpreted theoretically.

### Threshold ≠ Bifurcation

Operational classification boundaries must not automatically be interpreted as dynamical phase transitions.

### Model ≠ Reality

The simulation is a theoretical boundary-condition model, not a validated model of human psychology or civilization.

### Emergence vs. Construction

Every observed phenomenon must be classified as either:

- structurally imposed
- controller-induced
- dynamically emergent
- operationally defined

where possible.

---

## 11. Roadmap

```text
03c — Temporal Dynamics
        ↓
04 — λ × γ Regime Mapping
        ↓
05 — Slow G / Behavioral Feedback
        ↓
06 — Stochastic Robustness
        ↓
07 — Multi-Agent Population Model
        ↓
08 — Civilizational Homeostasis
```

The long-term objective is to determine whether Digital Soma-like dynamics persist when the model is extended from a single agent to interacting populations and adaptive environments.

---

## 12. Research Question

The simulation layer ultimately asks:

> **Under what conditions can successful emotional optimization become a self-reinforcing reduction in transformative capacity and human agency?**

And more specifically:

> **Can a civilization remain capable of transformation when the systems governing its environment become increasingly capable of removing the friction that generates questioning, dissent, adaptation, and change?**

---

## 13. Maintainer

**Y. Marutani**

O'VALLEY Knowledge Lab

---

## 14. License

To be determined.
