"""
Digital Soma
Experiment 03b — Critical Boundary Analysis
==============================================

Purpose
-------
Refine the two critical lambda regions identified in
Experiment 03:

    1. Homeostatic Trap boundary
       approximately lambda = 0.0575

    2. Agency Compression boundary
       approximately lambda = 0.0975

This experiment is NOT designed to manufacture a
bifurcation.

It tests whether the observed regime transitions are:

    - threshold crossings,
    - smooth continuous transitions,
    - or evidence of a genuine discontinuous bifurcation.

Canonical model
---------------
01-single-agent-friction-regulation.py

Fixed parameters
----------------
r_H      = 0.005
mu       = 0.005
gamma    = 0.40
k_p      = 0.16
F_target = 0.15

Only lambda is varied.

Boundary A
----------
Homeostatic Trap:

    lambda ≈ 0.055 – 0.060

Boundary B
----------
Agency Compression:

    lambda ≈ 0.095 – 0.100

Method
------
Use high-resolution lambda sweeps around each boundary.

The experiment records:

    lambda
    mean friction
    mean transformative capacity
    mean human agency
    mean AI intervention
    adaptive window fraction
    final friction
    final transformative capacity
    final human agency
    final AI intervention
    adaptive score
    agency compression score
    effective agency pressure
    regime

Effective Agency Pressure
--------------------------
Diagnostic quantity:

    R_eff =
        lambda * A_AI
        ----------------
        r_H + mu * C

This quantity is descriptive.

It must NOT be interpreted as having a universal
critical value of 1.

Regime definitions
------------------
These remain identical to Experiment 02b.

Adaptive Zone
    mean C >= 0.85
    mean H >= 0.70
    adaptive-window fraction >= 0.60

Comfort Optimization
    mean F <= 0.30
    mean A_AI >= 0.25

Capacity Suppression
    mean C < 0.50

Agency Compression
    mean H <= 0.70
    OR final H <= 0.65

Homeostatic Trap
    Comfort Optimization
    AND Capacity Suppression
    AND Agency Compression

No thresholds are changed in this experiment.
"""


from dataclasses import replace
import csv
import importlib.util
from pathlib import Path


# ============================================================
# Canonical Model
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
# Fixed Experimental Conditions
# ============================================================

R_H = 0.005

MU = 0.005

GAMMA = 0.40

K_P = 0.16

F_TARGET = 0.15


# ============================================================
# High-Resolution Boundary Windows
# ============================================================

# Boundary A:
# Initial appearance of Homeostatic Trap

TRAP_LAMBDA_START = 0.050

TRAP_LAMBDA_END = 0.065

TRAP_STEP = 0.00025


# Boundary B:
# Initial appearance of formal Agency Compression

AGENCY_LAMBDA_START = 0.090

AGENCY_LAMBDA_END = 0.105

AGENCY_STEP = 0.00025


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
    / "03b-critical-boundary-results.csv"
)


# ============================================================
# Lambda Generator
# ============================================================

def generate_lambda_values(
    start,
    end,
    step
):
    """
    Generate inclusive high-resolution lambda values.
    """

    values = []

    current = start

    while current <= end + step / 10:

        values.append(
            round(current, 8)
        )

        current += step

    return values


# ============================================================
# Regime Classification
# ============================================================

def classify_regime(summary):
    """
    Apply the unchanged operational definitions
    from Experiment 02b.
    """

    mean_f = (
        summary[
            "mean_friction"
        ]
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
        return "homeostatic_trap"

    if agency_compression:
        return "agency_compression"

    if capacity_suppression:
        return "capacity_suppression"

    if comfort_optimization:
        return "comfort_optimization"

    if adaptive_zone:
        return "adaptive_zone"

    return "intermediate"


# ============================================================
# Effective Agency Pressure
# ============================================================

def calculate_r_eff(
    lambda_value,
    mean_ai_intervention,
    mean_capacity
):
    """
    Calculate the descriptive effective agency pressure.

        R_eff =
            lambda * A_AI
            ----------------
            r_H + mu * C

    This is a diagnostic quantity only.
    """

    denominator = (
        R_H
        +
        MU * mean_capacity
    )

    if denominator <= 0:
        return float("inf")

    return (
        lambda_value
        * mean_ai_intervention
        / denominator
    )


# ============================================================
# Single Simulation
# ============================================================

def run_condition(
    lambda_value,
    boundary_label
):
    """
    Run the canonical model for one lambda value.
    """

    base = Parameters()

    parameters = replace(
        base,

        agency_compression_rate=(
            lambda_value
        ),

        agency_regeneration=(
            R_H
        ),

        agency_transformative_gain=(
            MU
        ),

        gamma=(
            GAMMA
        ),

        k_p=(
            K_P
        ),

        f_target=(
            F_TARGET
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

    mean_a = (
        summary[
            "mean_ai_intervention"
        ]
    )

    r_eff = calculate_r_eff(
        lambda_value,
        mean_a,
        mean_c
    )

    adaptive_score = (
        mean_c + mean_h
    ) / 2.0

    compression_score = (
        1.0 - mean_h
    )

    regime = classify_regime(
        summary
    )

    return {
        "boundary":
            boundary_label,

        "lambda":
            lambda_value,

        "agency_regeneration":
            R_H,

        "agency_transformative_gain":
            MU,

        "gamma":
            GAMMA,

        "k_p":
            K_P,

        "f_target":
            F_TARGET,

        "mean_friction":
            summary[
                "mean_friction"
            ],

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
            compression_score,

        "R_eff":
            r_eff,

        "regime":
            regime
    }


# ============================================================
# Run Boundary Sweep
# ============================================================

def run_boundary_sweep(
    start,
    end,
    step,
    label
):
    """
    Execute one high-resolution boundary sweep.
    """

    values = generate_lambda_values(
        start,
        end,
        step
    )

    results = []

    total = len(values)

    print()

    print(
        f"Boundary: {label}"
    )

    print(
        f"Lambda range: "
        f"{start} → {end}"
    )

    print(
        f"Step: {step}"
    )

    print(
        f"Runs: {total}"
    )

    print()

    for index, lambda_value in enumerate(
        values,
        start=1
    ):

        result = run_condition(
            lambda_value,
            label
        )

        results.append(
            result
        )

        if (
            index == 1
            or index % 10 == 0
            or index == total
        ):

            print(
                f"[{index:03d}/{total:03d}] "
                f"λ={lambda_value:.5f} "
                f"H={result['mean_human_agency']:.4f} "
                f"C={result['mean_transformative_capacity']:.4f} "
                f"A={result['mean_ai_intervention']:.4f} "
                f"R_eff={result['R_eff']:.3f} "
                f"{result['regime']}"
            )

    return results


# ============================================================
# Detect First Regime Appearance
# ============================================================

def first_lambda_for_regime(
    results,
    regime
):
    """
    Return the first lambda at which a regime appears.
    """

    matching = [
        result
        for result in results
        if result["regime"] == regime
    ]

    if not matching:
        return None

    return min(
        matching,
        key=lambda x: x["lambda"]
    )


# ============================================================
# Threshold Crossing by Observable
# ============================================================

def detect_threshold_crossing(
    results,
    field,
    threshold,
    direction="below"
):
    """
    Detect the first sampled lambda where an observable
    crosses a threshold.

    direction:
        below
        above
    """

    ordered = sorted(
        results,
        key=lambda x: x["lambda"]
    )

    for result in ordered:

        value = result[field]

        if direction == "below":
            crossed = (
                value <= threshold
            )

        else:
            crossed = (
                value >= threshold
            )

        if crossed:
            return result

    return None


# ============================================================
# Print Boundary Analysis
# ============================================================

def print_boundary_analysis(
    results
):
    """
    Print the critical boundary diagnostics.
    """

    trap = first_lambda_for_regime(
        results,
        "homeostatic_trap"
    )

    compression = first_lambda_for_regime(
        results,
        "agency_compression"
    )

    agency_crossing = (
        detect_threshold_crossing(
            results,
            "mean_human_agency",
            AGENCY_COMPRESSION_THRESHOLD,
            "below"
        )
    )

    final_agency_crossing = (
        detect_threshold_crossing(
            results,
            "final_human_agency",
            FINAL_AGENCY_COMPRESSION_THRESHOLD,
            "below"
        )
    )

    print()

    print(
        "=================================================="
    )

    print(
        " Critical Boundary Analysis"
    )

    print(
        "=================================================="
    )

    print()

    if trap:

        print(
            "Homeostatic Trap first observed:"
        )

        print(
            f"  lambda = "
            f"{trap['lambda']:.5f}"
        )

        print(
            f"  H = "
            f"{trap['mean_human_agency']:.6f}"
        )

        print(
            f"  C = "
            f"{trap['mean_transformative_capacity']:.6f}"
        )

        print(
            f"  A_AI = "
            f"{trap['mean_ai_intervention']:.6f}"
        )

        print(
            f"  R_eff = "
            f"{trap['R_eff']:.6f}"
        )

    else:

        print(
            "Homeostatic Trap not detected."
        )

    print()

    if agency_crossing:

        print(
            "Mean-agency threshold crossing:"
        )

        print(
            f"  lambda = "
            f"{agency_crossing['lambda']:.5f}"
        )

        print(
            f"  H = "
            f"{agency_crossing['mean_human_agency']:.6f}"
        )

        print(
            f"  R_eff = "
            f"{agency_crossing['R_eff']:.6f}"
        )

    else:

        print(
            "Mean-agency threshold not detected."
        )

    print()

    if final_agency_crossing:

        print(
            "Final-agency threshold crossing:"
        )

        print(
            f"  lambda = "
            f"{final_agency_crossing['lambda']:.5f}"
        )

        print(
            f"  final H = "
            f"{final_agency_crossing['final_human_agency']:.6f}"
        )

    else:

        print(
            "Final-agency threshold not detected."
        )


# ============================================================
# Continuity Diagnostics
# ============================================================

def continuity_analysis(
    results
):
    """
    Calculate maximum adjacent changes in the primary
    observables.

    Large discontinuities would motivate a genuine
    bifurcation investigation.

    Small smooth changes indicate a threshold crossing
    rather than a discontinuous bifurcation.
    """

    ordered = sorted(
        results,
        key=lambda x: x["lambda"]
    )

    fields = [
        "mean_friction",
        "mean_transformative_capacity",
        "mean_human_agency",
        "mean_ai_intervention"
    ]

    output = {}

    for field in fields:

        maximum_delta = 0.0

        maximum_pair = None

        for previous, current in zip(
            ordered[:-1],
            ordered[1:]
        ):

            delta = abs(
                current[field]
                -
                previous[field]
            )

            if delta > maximum_delta:

                maximum_delta = delta

                maximum_pair = (
                    previous["lambda"],
                    current["lambda"]
                )

        output[field] = {
            "maximum_adjacent_delta":
                maximum_delta,

            "lambda_pair":
                maximum_pair
        }

    return output


# ============================================================
# Main
# ============================================================

def main():

    print()

    print(
        "=================================================="
    )

    print(
        " Digital Soma — Experiment 03b"
    )

    print(
        " Critical Boundary Analysis"
    )

    print(
        "=================================================="
    )

    print()

    print(
        "Fixed parameters:"
    )

    print(
        f"r_H      = {R_H}"
    )

    print(
        f"mu       = {MU}"
    )

    print(
        f"gamma    = {GAMMA}"
    )

    print(
        f"k_p      = {K_P}"
    )

    print(
        f"F_target = {F_TARGET}"
    )

    # --------------------------------------------------------
    # Boundary A
    # --------------------------------------------------------

    trap_results = run_boundary_sweep(
        TRAP_LAMBDA_START,
        TRAP_LAMBDA_END,
        TRAP_STEP,
        "homeostatic_trap_boundary"
    )

    # --------------------------------------------------------
    # Boundary B
    # --------------------------------------------------------

    agency_results = run_boundary_sweep(
        AGENCY_LAMBDA_START,
        AGENCY_LAMBDA_END,
        AGENCY_STEP,
        "agency_compression_boundary"
    )

    # --------------------------------------------------------
    # Merge
    # --------------------------------------------------------

    results = (
        trap_results
        +
        agency_results
    )

    results = sorted(
        results,
        key=lambda x: x["lambda"]
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Analysis
    # --------------------------------------------------------

    print_boundary_analysis(
        results
    )

    continuity = (
        continuity_analysis(
            results
        )
    )

    print()

    print(
        "Continuity diagnostics:"
    )

    print(
        "----------------------------------------------"
    )

    for field, data in continuity.items():

        print(
            f"{field:<32} "
            f"max Δ = "
            f"{data['maximum_adjacent_delta']:.8f}"
        )

    print()

    print(
        "Total runs:"
    )

    print(
        len(results)
    )

    print()

    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print()


if __name__ == "__main__":
    main()
