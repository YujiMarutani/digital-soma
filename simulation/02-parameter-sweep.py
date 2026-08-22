"""
Digital Soma
Parameter Sweep: Friction Regulation
======================================

Simulation Layer: 1.0.0
Experiment: 02

Purpose
-------
Sweep the AI target friction (F_target) and determine whether
an adaptive Friction Window emerges.

Primary research question
-------------------------
What happens to transformative capacity and human agency when
the AI controller is instructed to maintain different target
friction levels?

Primary parameter
-----------------
F_target

Measured outputs
----------------
- Mean friction
- Mean transformative capacity
- Mean human agency
- Mean AI intervention
- Adaptive-window occupancy
- Final friction
- Final transformative capacity
- Final human agency

This script reuses the canonical single-agent model:

simulation/01-single-agent-friction-regulation.py

This is a conceptual simulation, not an empirical model of
human psychology, genetics, or civilization.
"""

from dataclasses import replace
import csv
import importlib.util
from pathlib import Path


# ============================================================
# Load canonical simulation model
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

F_TARGET_MIN = 0.05
F_TARGET_MAX = 0.95
F_TARGET_STEP = 0.05

OUTPUT_FILE = (
    CURRENT_DIR
    / "parameter-sweep-results.csv"
)


# ============================================================
# Generate Sweep Values
# ============================================================

def generate_target_values():
    """
    Generate F_target values for the parameter sweep.

    Example:
        0.05
        0.10
        ...
        0.95
    """

    values = []

    current = F_TARGET_MIN

    while current <= F_TARGET_MAX + 1e-9:
        values.append(round(current, 4))
        current += F_TARGET_STEP

    return values


# ============================================================
# Run Single Experiment
# ============================================================

def run_single_target(f_target):
    """
    Run the canonical simulation for one target friction value.
    """

    base_parameters = Parameters()

    parameters = replace(
        base_parameters,
        f_target=f_target
    )

    history = run_simulation(parameters)

    summary = summarize(
        history,
        parameters
    )

    return summary


# ============================================================
# Run Parameter Sweep
# ============================================================

def run_parameter_sweep():
    """
    Run the complete F_target sweep.
    """

    results = []

    target_values = generate_target_values()

    print()
    print("==============================================")
    print(" Digital Soma — Friction Target Sweep")
    print("==============================================")
    print()

    print(
        f"Targets: "
        f"{F_TARGET_MIN:.2f} → "
        f"{F_TARGET_MAX:.2f}"
    )

    print(
        f"Step: "
        f"{F_TARGET_STEP:.2f}"
    )

    print()

    for index, f_target in enumerate(
        target_values,
        start=1
    ):

        summary = run_single_target(
            f_target
        )

        result = {
            "f_target": f_target,
            **summary
        }

        results.append(result)

        print(
            f"[{index:02d}] "
            f"F_target={f_target:.2f} | "
            f"C={summary['mean_transformative_capacity']:.4f} | "
            f"H={summary['mean_human_agency']:.4f} | "
            f"F={summary['mean_friction']:.4f}"
        )

    return results


# ============================================================
# Save Results
# ============================================================

def save_results(results):
    """
    Save the complete parameter sweep to CSV.
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

        writer.writerows(results)


# ============================================================
# Find Optimal Targets
# ============================================================

def find_optima(results):
    """
    Identify target values that maximize:

    1. Transformative capacity
    2. Human agency
    3. A combined adaptive score
    """

    best_capacity = max(
        results,
        key=lambda x:
        x["mean_transformative_capacity"]
    )

    best_agency = max(
        results,
        key=lambda x:
        x["mean_human_agency"]
    )

    # --------------------------------------------------------
    # Combined score
    #
    # Equal weighting is intentionally used for the first
    # experiment. This can be replaced by a multi-objective
    # weighting model later.
    # --------------------------------------------------------

    for result in results:

        result["adaptive_score"] = (
            result["mean_transformative_capacity"]
            +
            result["mean_human_agency"]
        ) / 2.0

    best_combined = max(
        results,
        key=lambda x:
        x["adaptive_score"]
    )

    return (
        best_capacity,
        best_agency,
        best_combined
    )


# ============================================================
# Analyze Friction Window
# ============================================================

def analyze_friction_window(results):
    """
    Identify target regions associated with high
    transformative capacity.

    The analysis is deliberately descriptive rather
    than assuming the location of the optimal window.
    """

    capacity_values = [
        r["mean_transformative_capacity"]
        for r in results
    ]

    maximum = max(
        capacity_values
    )

    threshold = 0.90 * maximum

    adaptive_candidates = [
        r
        for r in results
        if r["mean_transformative_capacity"]
        >= threshold
    ]

    return {
        "maximum_capacity": maximum,
        "90_percent_threshold": threshold,
        "adaptive_candidates": adaptive_candidates
    }


# ============================================================
# Print Results
# ============================================================

def print_analysis(
    results,
    optima,
    window_analysis
):
    """
    Print a compact research summary.
    """

    (
        best_capacity,
        best_agency,
        best_combined
    ) = optima

    print()
    print("==============================================")
    print(" Parameter Sweep Analysis")
    print("==============================================")
    print()

    print("Maximum Transformative Capacity")
    print("--------------------------------")
    print(
        f"F_target = "
        f"{best_capacity['f_target']:.2f}"
    )

    print(
        f"C = "
        f"{best_capacity['mean_transformative_capacity']:.4f}"
    )

    print()

    print("Maximum Human Agency")
    print("---------------------")
    print(
        f"F_target = "
        f"{best_agency['f_target']:.2f}"
    )

    print(
        f"H = "
        f"{best_agency['mean_human_agency']:.4f}"
    )

    print()

    print("Maximum Combined Adaptive Score")
    print("--------------------------------")
    print(
        f"F_target = "
        f"{best_combined['f_target']:.2f}"
    )

    print(
        f"Score = "
        f"{best_combined['adaptive_score']:.4f}"
    )

    print()

    print("Candidate Adaptive Window")
    print("-------------------------")

    candidates = (
        window_analysis[
            "adaptive_candidates"
        ]
    )

    if not candidates:
        print(
            "No candidate window detected."
        )

    else:

        for result in candidates:

            print(
                f"F_target={result['f_target']:.2f} | "
                f"C={result['mean_transformative_capacity']:.4f} | "
                f"H={result['mean_human_agency']:.4f}"
            )

    print()

    print(
        "90% capacity threshold = "
        f"{window_analysis['90_percent_threshold']:.4f}"
    )


# ============================================================
# Main
# ============================================================

def main():

    results = run_parameter_sweep()

    (
        best_capacity,
        best_agency,
        best_combined
    ) = find_optima(results)

    window_analysis = (
        analyze_friction_window(
            results
        )
    )

    save_results(
        results
    )

    print_analysis(
        results,
        (
            best_capacity,
            best_agency,
            best_combined
        ),
        window_analysis
    )

    print()
    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print()

    print(
        "Next experiment:"
    )

    print(
        "02b — Sensitivity analysis"
    )


if __name__ == "__main__":
    main()
