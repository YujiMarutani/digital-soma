"""
Digital Soma
Experiment 02b — Sensitivity Analysis
========================================

Simulation Layer: 1.0.0
Experiment: 02b

Purpose
-------
Determine whether Agency Compression and the Homeostatic Trap
are mathematically reachable within the Friction Regulation
model, and identify the parameter regimes in which they emerge.

This experiment follows:

    01 — Single-Agent Friction Regulation
    02 — F_target Parameter Sweep

Primary research question
-------------------------
Under what parameter conditions does the system transition
from agency-preserving regulation to Agency Compression and
eventually to a Homeostatic Trap?

Methodological principle
------------------------
This is an existence search, NOT a confirmation experiment.

Parameters are systematically swept across predefined ranges.
The model is not tuned to manufacture a desired outcome.

Primary parameters
-------------------
lambda
    Agency compression rate

r_H
    Human agency regeneration rate

mu
    Transformative-agency gain

gamma
    AI intervention effectiveness

k_p
    AI controller gain

F_target
    Target friction

Regime definitions
------------------
Adaptive Zone
    mean C >= 0.85 * C_max
    mean H >= 0.70
    adaptive-window fraction >= 0.60

Comfort Optimization
    mean F <= 0.30
    mean A_AI >= 0.25

Capacity Suppression
    mean C < 0.50 * C_max

Agency Compression
    mean H <= 0.70
    OR final H <= 0.65

Homeostatic Trap
    Comfort Optimization
    AND Capacity Suppression
    AND Agency Compression

Scores
------
Adaptive Score:
    S_adapt = (mean C + mean H) / 2

Agency Compression Score:
    S_compress = 1 - mean H

Important
---------
This is a conceptual dynamical model.

It is NOT an empirical model of human psychology,
genetics, or civilization.
"""

from dataclasses import replace
import csv
import importlib.util
from pathlib import Path


# ============================================================
# Load Canonical Single-Agent Model
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent

MODEL_FILE = (
    CURRENT_DIR
    / "01-single-agent-friction-regulation.py"
)

SPEC = importlib.util.spec_from_file_location(
    "friction_regulation",
    MODEL_FILE
)

MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)

Parameters = MODEL.Parameters
run_simulation = MODEL.run_simulation
summarize = MODEL.summarize


# ============================================================
# Parameter Search Space
# ============================================================

LAMBDA_VALUES = [
    0.005,
    0.015,
    0.045,
    0.090,
    0.150
]

R_H_VALUES = [
    0.005,
    0.020,
    0.050
]

MU_VALUES = [
    0.005,
    0.025,
    0.060
]

GAMMA_VALUES = [
    0.40,
    0.80,
    1.20
]

K_P_VALUES = [
    0.04,
    0.08,
    0.16
]

F_TARGET_VALUES = [
    0.15,
    0.35,
    0.55,
    0.75
]


# ============================================================
# Regime Thresholds
# ============================================================

ADAPTIVE_CAPACITY_THRESHOLD = 0.85
ADAPTIVE_AGENCY_THRESHOLD = 0.70
ADAPTIVE_WINDOW_THRESHOLD = 0.60

COMFORT_FRICTION_THRESHOLD = 0.30
COMFORT_AI_THRESHOLD = 0.25

CAPACITY_SUPPRESSION_THRESHOLD = 0.50

AGENCY_COMPRESSION_THRESHOLD = 0.70
FINAL_AGENCY_COMPRESSION_THRESHOLD = 0.65


# ============================================================
# Output
# ============================================================

OUTPUT_FILE = (
    CURRENT_DIR
    / "02b-sensitivity-results.csv"
)


# ============================================================
# Regime Classification
# ============================================================

def classify_regime(summary):
    """
    Classify a simulation according to fixed operational
    definitions.

    Priority order:

        Homeostatic Trap
        Agency Compression
        Capacity Suppression
        Comfort Optimization
        Adaptive Zone
        Intermediate
    """

    mean_f = (
        summary["mean_friction"]
    )

    mean_c = (
        summary[
            "mean_transformative_capacity"
        ]
    )

    mean_h = (
        summary[
            "mean_human_agency"
        ]
    )

    mean_a = (
        summary[
            "mean_ai_intervention"
        ]
    )

    final_h = (
        summary[
            "final_human_agency"
        ]
    )

    adaptive_fraction = (
        summary[
            "adaptive_window_fraction"
        ]
    )

    comfort_optimization = (
        mean_f <= COMFORT_FRICTION_THRESHOLD
        and
        mean_a >= COMFORT_AI_THRESHOLD
    )

    capacity_suppression = (
        mean_c < CAPACITY_SUPPRESSION_THRESHOLD
    )

    agency_compression = (
        mean_h <= AGENCY_COMPRESSION_THRESHOLD
        or
        final_h <= FINAL_AGENCY_COMPRESSION_THRESHOLD
    )

    adaptive_zone = (
        mean_c >= ADAPTIVE_CAPACITY_THRESHOLD
        and
        mean_h >= ADAPTIVE_AGENCY_THRESHOLD
        and
        adaptive_fraction >= ADAPTIVE_WINDOW_THRESHOLD
    )

    homeostatic_trap = (
        comfort_optimization
        and
        capacity_suppression
        and
        agency_compression
    )

    if homeostatic_trap:
        return "Homeostatic Trap"

    if agency_compression:
        return "Agency Compression"

    if capacity_suppression:
        return "Capacity Suppression"

    if comfort_optimization:
        return "Comfort Optimization"

    if adaptive_zone:
        return "Adaptive Zone"

    return "Intermediate"


# ============================================================
# Run One Parameter Combination
# ============================================================

def run_single_condition(
    lambda_value,
    r_h,
    mu,
    gamma,
    k_p,
    f_target
):
    """
    Run the canonical model under one parameter combination.
    """

    base = Parameters()

    parameters = replace(
        base,

        agency_compression_rate=(
            lambda_value
        ),

        agency_regeneration=(
            r_h
        ),

        agency_transformative_gain=(
            mu
        ),

        gamma=(
            gamma
        ),

        k_p=(
            k_p
        ),

        f_target=(
            f_target
        )
    )

    history = run_simulation(
        parameters
    )

    summary = summarize(
        history,
        parameters
    )

    mean_c = (
        summary[
            "mean_transformative_capacity"
        ]
    )

    mean_h = (
        summary[
            "mean_human_agency"
        ]
    )

    mean_f = (
        summary[
            "mean_friction"
        ]
    )

    mean_a = (
        summary[
            "mean_ai_intervention"
        ]
    )

    adaptive_score = (
        mean_c + mean_h
    ) / 2.0

    agency_compression_score = (
        1.0 - mean_h
    )

    regime = classify_regime(
        summary
    )

    return {
        "lambda": lambda_value,
        "r_H": r_h,
        "mu": mu,
        "gamma": gamma,
        "k_p": k_p,
        "f_target": f_target,

        "mean_friction": mean_f,

        "mean_transformative_capacity":
            mean_c,

        "mean_human_agency":
            mean_h,

        "mean_ai_intervention":
            mean_a,

        "adaptive_window_fraction":
            summary[
                "adaptive_window_fraction"
            ],

        "final_friction":
            summary[
                "final_friction"
            ],

        "final_transformative_capacity":
            summary[
                "final_transformative_capacity"
            ],

        "final_human_agency":
            summary[
                "final_human_agency"
            ],

        "final_ai_intervention":
            summary[
                "final_ai_intervention"
            ],

        "adaptive_score":
            adaptive_score,

        "agency_compression_score":
            agency_compression_score,

        "regime":
            regime
    }


# ============================================================
# Full Factorial Sweep
# ============================================================

def run_sensitivity_analysis():
    """
    Execute the complete factorial parameter sweep.

    Number of runs:

        5 lambda
        × 3 r_H
        × 3 mu
        × 3 gamma
        × 3 k_p
        × 4 F_target

        = 1620 runs
    """

    results = []

    total_runs = (
        len(LAMBDA_VALUES)
        * len(R_H_VALUES)
        * len(MU_VALUES)
        * len(GAMMA_VALUES)
        * len(K_P_VALUES)
        * len(F_TARGET_VALUES)
    )

    run_number = 0

    print()
    print(
        "=================================================="
    )
    print(
        " Digital Soma — Experiment 02b"
    )
    print(
        " Sensitivity Analysis"
    )
    print(
        "=================================================="
    )
    print()

    print(
        f"Total runs: {total_runs}"
    )

    print()

    for lambda_value in LAMBDA_VALUES:

        for r_h in R_H_VALUES:

            for mu in MU_VALUES:

                for gamma in GAMMA_VALUES:

                    for k_p in K_P_VALUES:

                        for f_target in F_TARGET_VALUES:

                            run_number += 1

                            result = (
                                run_single_condition(
                                    lambda_value=(
                                        lambda_value
                                    ),
                                    r_h=r_h,
                                    mu=mu,
                                    gamma=gamma,
                                    k_p=k_p,
                                    f_target=f_target
                                )
                            )

                            results.append(
                                result
                            )

                            if (
                                run_number == 1
                                or
                                run_number % 100 == 0
                                or
                                run_number == total_runs
                            ):

                                print(
                                    f"[{run_number:04d}/"
                                    f"{total_runs:04d}] "
                                    f"lambda="
                                    f"{lambda_value:.3f} "
                                    f"r_H="
                                    f"{r_h:.3f} "
                                    f"mu="
                                    f"{mu:.3f} "
                                    f"gamma="
                                    f"{gamma:.2f} "
                                    f"k_p="
                                    f"{k_p:.2f} "
                                    f"F_target="
                                    f"{f_target:.2f} "
                                    f"→ "
                                    f"H="
                                    f"{result['mean_human_agency']:.3f} "
                                    f"C="
                                    f"{result['mean_transformative_capacity']:.3f} "
                                    f"{result['regime']}"
                                )

    return results


# ============================================================
# Save CSV
# ============================================================

def save_results(results):
    """
    Save all parameter combinations and outputs.
    """

    if not results:
        return

    fieldnames = list(
        results[0].keys()
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            results
        )


# ============================================================
# Regime Statistics
# ============================================================

def calculate_regime_statistics(results):
    """
    Calculate occupancy of each regime.
    """

    counts = {}

    for result in results:

        regime = result["regime"]

        counts[regime] = (
            counts.get(regime, 0)
            + 1
        )

    total = len(results)

    statistics = []

    for regime, count in sorted(
        counts.items()
    ):

        percentage = (
            100.0
            * count
            / total
        )

        statistics.append(
            (
                regime,
                count,
                percentage
            )
        )

    return statistics


# ============================================================
# Find Minimum Agency by Lambda
# ============================================================

def calculate_lambda_agency_summary(
    results
):
    """
    Calculate minimum and mean agency for each
    lambda value.
    """

    summary = {}

    for result in results:

        lambda_value = result["lambda"]

        if lambda_value not in summary:

            summary[lambda_value] = []

        summary[lambda_value].append(
            result[
                "mean_human_agency"
            ]
        )

    output = []

    for lambda_value in sorted(
        summary.keys()
    ):

        values = summary[
            lambda_value
        ]

        output.append(
            {
                "lambda":
                    lambda_value,

                "minimum_mean_H":
                    min(values),

                "mean_H":
                    sum(values)
                    / len(values)
            }
        )

    return output


# ============================================================
# Find Homeostatic Trap Conditions
# ============================================================

def find_homeostatic_traps(results):
    """
    Extract all Homeostatic Trap conditions.

    No ranking or cherry-picking is performed.
    """

    return [
        result
        for result in results
        if result["regime"]
        == "Homeostatic Trap"
    ]


# ============================================================
# Print Analysis
# ============================================================

def print_analysis(results):
    """
    Print a concise summary of the experiment.
    """

    total = len(results)

    regime_statistics = (
        calculate_regime_statistics(
            results
        )
    )

    lambda_summary = (
        calculate_lambda_agency_summary(
            results
        )
    )

    traps = (
        find_homeostatic_traps(
            results
        )
    )

    print()
    print(
        "=================================================="
    )
    print(
        " Experiment 02b Results"
    )
    print(
        "=================================================="
    )
    print()

    print(
        f"Total simulations: {total}"
    )

    print()

    print(
        "Regime occupancy:"
    )

    print(
        "----------------------------------------------"
    )

    for (
        regime,
        count,
        percentage
    ) in regime_statistics:

        print(
            f"{regime:<25}"
            f"{count:>6}  "
            f"{percentage:>6.2f}%"
        )

    print()

    print(
        "Agency by lambda:"
    )

    print(
        "----------------------------------------------"
    )

    print(
        "lambda | min(mean H) | mean(mean H)"
    )

    for item in lambda_summary:

        print(
            f"{item['lambda']:.3f}   | "
            f"{item['minimum_mean_H']:.3f}       | "
            f"{item['mean_H']:.3f}"
        )

    print()

    print(
        f"Homeostatic Trap runs: "
        f"{len(traps)}"
    )

    if traps:

        print()

        print(
            "Strongest observed agency compression:"
        )

        strongest = min(
            traps,
            key=lambda x:
            x["mean_human_agency"]
        )

        print(
            f"lambda = "
            f"{strongest['lambda']}"
        )

        print(
            f"r_H = "
            f"{strongest['r_H']}"
        )

        print(
            f"mu = "
            f"{strongest['mu']}"
        )

        print(
            f"gamma = "
            f"{strongest['gamma']}"
        )

        print(
            f"k_p = "
            f"{strongest['k_p']}"
        )

        print(
            f"F_target = "
            f"{strongest['f_target']}"
        )

        print(
            f"Mean F = "
            f"{strongest['mean_friction']:.4f}"
        )

        print(
            f"Mean C = "
            f"{strongest['mean_transformative_capacity']:.4f}"
        )

        print(
            f"Mean H = "
            f"{strongest['mean_human_agency']:.4f}"
        )

        print(
            f"Mean A_AI = "
            f"{strongest['mean_ai_intervention']:.4f}"
        )

    print()

    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )


# ============================================================
# Main
# ============================================================

def main():

    results = (
        run_sensitivity_analysis()
    )

    save_results(
        results
    )

    print_analysis(
        results
    )


if __name__ == "__main__":
    main()
