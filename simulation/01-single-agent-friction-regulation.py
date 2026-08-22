"""
Digital Soma
Single-Agent Friction Regulation Simulation
=============================================

Simulation Layer: 1.0.0
Model: Friction Regulation Model 1.0.0

Purpose
-------
Test whether a Friction Window emerges dynamically under
AI-mediated friction regulation.

Core variables
--------------
G      : biological / behavioral propensity
E      : environmental stress
F      : experienced friction
C      : transformative capacity
H      : human agency
B      : behavioral state
A_AI   : AI intervention intensity

Core hypotheses
---------------
1. Excessive friction reduces transformative capacity.
2. Very low friction may also reduce transformative capacity.
3. AI regulation can stabilize friction around a target.
4. Excessive optimization toward low friction may compress agency.
5. An adaptive friction target may preserve greater transformative
   capacity than aggressive comfort optimization.

This is a conceptual simulation, not an empirical model of human
psychology or genetics.
"""

from dataclasses import dataclass
import math
import csv


@dataclass
class Parameters:
    # Simulation
    steps: int = 1000
    dt: float = 0.01

    # Biological / environmental sensitivity
    alpha: float = 0.35
    beta: float = 0.65
    gamma: float = 0.80

    # Friction window
    f_min: float = 0.25
    f_max: float = 0.85
    f_star: float = 0.55
    sigma_f: float = 0.18
    c_max: float = 1.0

    # AI controller
    k_p: float = 0.08
    f_target: float = 0.55

    # Agency dynamics
    agency_regeneration: float = 0.02
    agency_compression_rate: float = 0.015
    agency_transformative_gain: float = 0.025

    # Behavioral dynamics
    behavior_learning_rate: float = 0.03
    friction_suppression_rate: float = 0.015

    # Environmental feedback
    behavior_environment_gain: float = 0.015
    environment_decay: float = 0.01

    # Initial conditions
    G: float = 0.50
    E: float = 0.50
    H: float = 1.00
    B: float = 0.50
    A_AI: float = 0.00


@dataclass
class State:
    t: float
    G: float
    E: float
    F: float
    C: float
    H: float
    B: float
    A_AI: float


def clamp(value, lower, upper):
    return max(lower, min(value, upper))


def calculate_friction(G, E, A_AI, p):
    """
    First-order friction equation:

        F = alpha*G + beta*E - gamma*A_AI

    Friction is bounded to [0, 1] for simulation stability.
    """
    F = (
        p.alpha * G
        + p.beta * E
        - p.gamma * A_AI
    )

    return clamp(F, 0.0, 1.0)


def calculate_transformative_capacity(F, p):
    """
    Inverted-U / Gaussian approximation:

        C(F) =
        C_max * exp(-(F - F*)^2 / (2*sigma_F^2))

    Maximum transformative capacity occurs around F*.
    """
    exponent = -(
        (F - p.f_star) ** 2
        / (2.0 * p.sigma_f ** 2)
    )

    return p.c_max * math.exp(exponent)


def update_ai_controller(F, A_AI, p):
    """
    Proportional negative-feedback controller:

        A_AI(t+1)
        =
        A_AI(t)
        +
        k_p * (F - F_target)

    If friction exceeds the target:
        AI intervention increases.

    If friction falls below the target:
        AI intervention decreases.
    """
    error = F - p.f_target

    A_next = A_AI + p.k_p * error

    return clamp(A_next, 0.0, 1.0)


def update_agency(H, A_AI, C, p):
    """
    Human agency dynamics:

        dH/dt =
            regeneration
            - AI compression
            + transformative development

    This avoids assuming that AI intervention automatically
    causes irreversible agency collapse.
    """
    dH = (
        p.agency_regeneration
        - p.agency_compression_rate * A_AI * H
        + p.agency_transformative_gain * C
    )

    H_next = H + p.dt * dH

    return clamp(H_next, 0.0, 1.0)


def update_behavior(B, C, F, p):
    """
    Simplified behavioral dynamics:

        dB/dt =
            learning from transformative capacity
            - suppression from excessive friction
    """
    dB = (
        p.behavior_learning_rate * C
        - p.friction_suppression_rate * F
    )

    B_next = B + p.dt * dB

    return clamp(B_next, 0.0, 1.0)


def update_environment(E, B, p):
    """
    Behavioral feedback into environment:

        dE/dt =
            behavior-environment coupling
            - environmental relaxation
    """
    dE = (
        p.behavior_environment_gain * B
        - p.environment_decay * E
    )

    E_next = E + p.dt * dE

    return clamp(E_next, 0.0, 1.0)


def run_simulation(p=None):
    if p is None:
        p = Parameters()

    G = p.G
    E = p.E
    H = p.H
    B = p.B
    A_AI = p.A_AI

    history = []

    for step in range(p.steps):

        t = step * p.dt

        # 1. Experienced friction
        F = calculate_friction(
            G=G,
            E=E,
            A_AI=A_AI,
            p=p
        )

        # 2. Transformative capacity
        C = calculate_transformative_capacity(
            F=F,
            p=p
        )

        # 3. Record current state
        history.append(
            State(
                t=t,
                G=G,
                E=E,
                F=F,
                C=C,
                H=H,
                B=B,
                A_AI=A_AI
            )
        )

        # 4. AI friction regulation
        A_AI = update_ai_controller(
            F=F,
            A_AI=A_AI,
            p=p
        )

        # 5. Human agency dynamics
        H = update_agency(
            H=H,
            A_AI=A_AI,
            C=C,
            p=p
        )

        # 6. Behavioral dynamics
        B = update_behavior(
            B=B,
            C=C,
            F=F,
            p=p
        )

        # 7. Environmental feedback
        E = update_environment(
            E=E,
            B=B,
            p=p
        )

    return history


def summarize(history, p):
    """
    Generate a compact summary of the simulation.
    """

    friction = [x.F for x in history]
    capacity = [x.C for x in history]
    agency = [x.H for x in history]
    intervention = [x.A_AI for x in history]

    mean_friction = sum(friction) / len(friction)
    mean_capacity = sum(capacity) / len(capacity)
    mean_agency = sum(agency) / len(agency)
    mean_intervention = (
        sum(intervention) / len(intervention)
    )

    adaptive_fraction = sum(
        p.f_min <= f <= p.f_max
        for f in friction
    ) / len(friction)

    return {
        "mean_friction": mean_friction,
        "mean_transformative_capacity": mean_capacity,
        "mean_human_agency": mean_agency,
        "mean_ai_intervention": mean_intervention,
        "adaptive_window_fraction": adaptive_fraction,
        "final_friction": friction[-1],
        "final_transformative_capacity": capacity[-1],
        "final_human_agency": agency[-1],
        "final_ai_intervention": intervention[-1],
    }


def save_csv(history, filename="friction-regulation-timeseries.csv"):
    """
    Export simulation data for downstream analysis.
    """

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "time",
            "G",
            "E",
            "F",
            "C",
            "H",
            "B",
            "A_AI"
        ])

        for state in history:
            writer.writerow([
                state.t,
                state.G,
                state.E,
                state.F,
                state.C,
                state.H,
                state.B,
                state.A_AI
            ])


def print_summary(summary):
    print("\n=== Digital Soma: Friction Regulation ===")
    print()

    print(
        f"Mean Friction: "
        f"{summary['mean_friction']:.4f}"
    )

    print(
        f"Mean Transformative Capacity: "
        f"{summary['mean_transformative_capacity']:.4f}"
    )

    print(
        f"Mean Human Agency: "
        f"{summary['mean_human_agency']:.4f}"
    )

    print(
        f"Mean AI Intervention: "
        f"{summary['mean_ai_intervention']:.4f}"
    )

    print(
        f"Adaptive Window Fraction: "
        f"{summary['adaptive_window_fraction']:.2%}"
    )

    print()

    print(
        f"Final Friction: "
        f"{summary['final_friction']:.4f}"
    )

    print(
        f"Final Transformative Capacity: "
        f"{summary['final_transformative_capacity']:.4f}"
    )

    print(
        f"Final Human Agency: "
        f"{summary['final_human_agency']:.4f}"
    )

    print(
        f"Final AI Intervention: "
        f"{summary['final_ai_intervention']:.4f}"
    )


def main():
    params = Parameters()

    history = run_simulation(params)

    summary = summarize(
        history,
        params
    )

    print_summary(summary)

    save_csv(history)

    print()
    print(
        "Time-series data saved to:"
        " friction-regulation-timeseries.csv"
    )


if __name__ == "__main__":
    main()
