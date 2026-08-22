"""
Digital Soma
Experiment 03 — Agency Compression Bifurcation Analysis
===========================================================

Purpose
-------
Locate the critical transition in agency dynamics as the
agency-compression rate (lambda) increases.

This experiment follows Experiment 02b, which demonstrated
that Agency Compression and Homeostatic Trap states are
mathematically reachable but occupy a restricted region of
parameter space.

Primary research question
-------------------------
At what value of lambda does the system transition from
agency-preserving regulation to sustained Agency Compression?

Secondary questions
-------------------
1. Does Human Agency decline continuously or abruptly?
2. Does Transformative Capacity decline simultaneously?
3. Does AI intervention increase before the transition?
4. Does a critical threshold exist?
5. Is the transition better explained by lambda alone or by
   effective agency pressure:

       R_eff = lambda * mean(A_AI)
               -------------------------
               r_H + mu * mean(C)

This experiment does NOT assume that a bifurcation exists.
It searches for one.

Important methodological constraint
-----------------------------------
Do not tune lambda to manufacture a desired result.

The parameter range is defined independently and the transition
is detected from the resulting dynamics.

This is a conceptual simulation, not an empirical model of
human psychology, genetics, or civilization.
"""

from dataclasses import replace
import csv
import importlib.util
from pathlib import Path


# ============================================================
# Load Canonical Model
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
# Experiment Configuration
# ============================================================

# Fixed conditions selected from the strongest
# Homeostatic Trap region observed in Experiment 02b.

FIXED_F_TARGET = 0.15
FIXED_R_H = 0.005
FIXED_MU = 0.005
FIXED_GAMMA = 0.40
FIXED_K_P = 0.16


# High-resolution lambda sweep.
#
# The range intentionally extends below and above the region
# where compression appeared in Experiment 02b.

LAMBDA_MIN = 0.005
LAMBDA_MAX = 0.200
LAMBDA_STEP = 0.0025


# Operational thresholds.
#
# These are inherited from Experiment 02b and are NOT changed
# to manufacture a transition.

AGENCY_COMPRESSION_THRESHOLD = 0.70
AGENCY_STRONG_COMPRESSION_THRESHOLD = 0.50

CAPACITY_SUPPRESSION_THRESHOLD = 0.50

COMFORT_FRICTION_THRESHOLD = 0.30
COMFORT_AI_THRESHOLD = 0.25


OUTPUT_FILE = (
    CURRENT_DIR
    / "03-bifurcation-results.csv"
)


# ============================================================
# Lambda Sweep Generator
# ============================================================

def generate_lambda_values():
    """
    Generate a high-resolution lambda sweep.
    """

    values = []

    current = LAMBDA_MIN

    while current <= LAMBDA_MAX + 1e-12:

        values.append(
            round(current, 6)
        )

        current += LAMBDA_STEP

    return values


# ============================================================
# Effective Agency Pressure
# ============================================================

def calculate_effective_agency_pressure(
    lambda_value,
    mean_ai_intervention,
    r_h,
    mu,
    mean_capacity
):
    """
    Effective Agency Compression Pressure:

        R_eff =
            lambda * mean(A_AI)
            -------------------------
            r_H + mu * mean(C)

    Interpretation:

        R_eff << 1
            regeneration / transformative protection dominates

        R_eff ≈ 1
            compression and regeneration compete

        R_eff >> 1
            compression pressure dominates

    This is a diagnostic ratio, not a universal law.
    """

    denominator = (
        r_h
        + mu * mean_capacity
    )

    if denominator <= 0:
        return float("inf")

    numerator = (
        lambda_value
        * mean_ai_intervention
    )

    return numerator / denominator


# ============================================================
# Regime Classification
# ============================================================

def classify_regime(summary):
    """
    Classify the final simulation regime.

    Classification priority:

        Homeostatic Trap
        Agency Compression
        Capacity Suppression
        Comfort Optimization
        Adaptive Zone
        Intermediate

    The thresholds are fixed from Experiment 02b.
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
        summary[
            "final_human_agency"
        ] <= 0.65
    )

    adaptive_zone = (
        mean_c >= 0.85
        and
        mean_h >= 0.70
        and
        adaptive_fraction >= 0.60
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
# Run One Lambda Condition
# ============================================================

def run_lambda(lambda_value):
    """
    Run the canonical model at one lambda value.
    """

    base = Parameters()

    parameters = replace(
        base,

        f_target=FIXED_F_TARGET,

        agency_compression_rate=(
            lambda_value
        ),

        agency_regeneration=(
            FIXED_R_H
        ),

        agency_transformative_gain=(
            FIXED_MU
        ),

        gamma=(
            FIXED_GAMMA
        ),

        k_p=(
            FIXED_K_P
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

    mean_a = (
        summary[
            "mean_ai_intervention"
        ]
    )

    r_eff = (
        calculate_effective_agency_pressure(
            lambda_value=lambda_value,
            mean_ai_intervention=mean_a,
            r_h=FIXED_R_H,
            mu=FIXED_MU,
            mean_capacity=mean_c
        )
    )

    regime = classify_regime(
        summary
    )

    return {
        "lambda": lambda_value,

        "f_target": FIXED_F_TARGET,
        "r_H": FIXED_R_H,
        "mu": FIXED_MU,
        "gamma": FIXED_GAMMA,
        "k_p": FIXED_K_P,

        "mean_friction":
            summary[
                "mean_friction"
            ],

        "mean_transformative_capacity":
            mean_c,

        "mean_human_agency":
            summary[
                "mean_human_agency"
            ],

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

        "effective_agency_pressure":
            r_eff,

        "agency_compression_score":
            1.0
            - summary[
                "mean_human_agency"
            ],

        "regime":
            regime
    }


# ============================================================
# Detect Transition
# ============================================================

def detect_transition(results):
    """
    Identify the first lambda value at which sustained
    Agency Compression appears.

    The primary criterion is:

        mean H <= 0.70

    A secondary criterion checks the Homeostatic Trap.
    """

    agency_transition = None
    trap_transition = None

    for result in results:

        if (
            agency_transition is None
            and
            result[
                "mean_human_agency"
            ]
            <= AGENCY_COMPRESSION_THRESHOLD
        ):

            agency_transition = result

        if (
            trap_transition is None
            and
            result["regime"]
            == "Homeostatic Trap"
        ):

            trap_transition = result

    return (
        agency_transition,
        trap_transition
    )


# ============================================================
# Save Results
# ============================================================

def save_results(results):
    """
    Save complete bifurcation sweep.
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
# Print Summary
# ============================================================

def print_summary(
    results,
    agency_transition,
    trap_transition
):
    """

    Print the critical transition information.
    """

    print()
    print(
        "=================================================="
    )
    print(
        " Digital Soma — Experiment 03"
    )
    print(
        " Agency Compression Bifurcation Analysis"
    )
    print(
        "=================================================="
    )
    print()

    print(
        "Fixed parameters:"
    )

    print(
        f"F_target = {FIXED_F_TARGET}"
    )

    print(
        f"r_H      = {FIXED_R_H}"
    )

    print(
        f"mu       = {FIXED_MU}"
    )

    print(
        f"gamma    = {FIXED_GAMMA}"
    )

    print(
        f"k_p      = {FIXED_K_P}"
    )

    print()

    if agency_transition is None:

        print(
            "Agency Compression threshold "
            "was NOT crossed."
        )

    else:

        print(
            "First Agency Compression threshold:"
        )

        print(
            f"lambda = "
            f"{agency_transition['lambda']:.6f}"
        )

        print(
            f"Mean H = "
            f"{agency_transition['mean_human_agency']:.4f}"
        )

        print(
            f"Mean C = "
            f"{agency_transition['mean_transformative_capacity']:.4f}"
        )

        print(
            f"Mean A = "
            f"{agency_transition['mean_ai_intervention']:.4f}"
        )

        print(
            f"R_eff = "
            f"{agency_transition['effective_agency_pressure']:.4f}"
        )

    print()

    if trap_transition is None:

        print(
            "Homeostatic Trap threshold "
            "was NOT crossed."
        )

    else:

        print(
            "First Homeostatic Trap:"
        )

        print(
            f"lambda = "
            f"{trap_transition['lambda']:.6f}"
        )

        print(
            f"Mean H = "
            f"{trap_transition['mean_human_agency']:.4f}"
        )

        print(
            f"Mean C = "
            f"{trap_transition['mean_transformative_capacity']:.4f}"
        )

        print(
            f"Mean F = "
            f"{trap_transition['mean_friction']:.4f}"
        )

        print(
            f"Mean A = "
            f"{trap_transition['mean_ai_intervention']:.4f}"
        )

        print(
            f"R_eff = "
            f"{trap_transition['effective_agency_pressure']:.4f}"
        )

    print()

    print(
        "Selected trajectory points:"
    )

    print(
        "lambda | F | C | H | A_AI | R_eff | regime"
    )

    print(
        "--------------------------------------------------"
    )

    # Print approximately every 10th result.
    stride = max(
        1,
        len(results) // 10
    )

    for result in results[::stride]:

        print(
            f"{result['lambda']:.4f} | "
            f"{result['mean_friction']:.3f} | "
            f"{result['mean_transformative_capacity']:.3f} | "
            f"{result['mean_human_agency']:.3f} | "
            f"{result['mean_ai_intervention']:.3f} | "
            f"{result['effective_agency_pressure']:.3f} | "
            f"{result['regime']}"
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

    lambda_values = (
        generate_lambda_values()
    )

    results = []

    print()
    print(
        "Running Experiment 03..."
    )

    print(
        f"Lambda range: "
        f"{LAMBDA_MIN} → "
        f"{LAMBDA_MAX}"
    )

    print(
        f"Step: "
        f"{LAMBDA_STEP}"
    )

    print(
        f"Runs: "
        f"{len(lambda_values)}"
    )

    print()

    for index, lambda_value in enumerate(
        lambda_values,
        start=1
    ):

        result = run_lambda(
            lambda_value
        )

        results.append(
            result
        )

        if (
            index == 1
            or index == len(lambda_values)
            or index % 10 == 0
        ):

            print(
                f"[{index:03d}/"
                f"{len(lambda_values):03d}] "
                f"lambda={lambda_value:.4f} | "
                f"H={result['mean_human_agency']:.4f} | "
                f"C={result['mean_transformative_capacity']:.4f} | "
                f"A={result['mean_ai_intervention']:.4f}"
            )

    (
        agency_transition,
        trap_transition
    ) = detect_transition(
        results
    )

    save_results(
        results
    )

    print_summary(
        results,
        agency_transition,
        trap_transition
    )


if __name__ == "__main__":
    main()
