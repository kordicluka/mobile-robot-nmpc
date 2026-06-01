import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from src.obstacles import Circle, Rectangle


def plot_trajectory(result: dict, scenario: dict, path: np.ndarray, save_path: str = None):
    fig, ax = plt.subplots(figsize=(8, 8))

    for obs in scenario["obstacles"]:
        if isinstance(obs, Circle):
            ax.add_patch(plt.Circle((obs.cx, obs.cy), obs.r, color="gray", alpha=0.6))
        elif isinstance(obs, Rectangle):
            w = obs.x_max - obs.x_min
            h = obs.y_max - obs.y_min
            ax.add_patch(patches.Rectangle((obs.x_min, obs.y_min), w, h, color="gray", alpha=0.6))

    ax.plot(path[:, 0], path[:, 1], "b--", linewidth=1.2, label="Referentna putanja")

    states = result["states"]
    ax.plot(states[:, 0], states[:, 1], "r-", linewidth=1.8, label="Stvarna putanja")

    ax.plot(*scenario["start"][:2], "go", markersize=10, label="Start")
    ax.plot(*scenario["goal"], "r*", markersize=12, label="Cilj")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title(f"Putanja — {scenario['name']}")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()
    plt.close()


def plot_environment(scenario: dict, save_path: str = None):
    fig, ax = plt.subplots(figsize=(8, 8))

    for obs in scenario["obstacles"]:
        if isinstance(obs, Circle):
            ax.add_patch(plt.Circle((obs.cx, obs.cy), obs.r, color="gray", alpha=0.6))
        elif isinstance(obs, Rectangle):
            w = obs.x_max - obs.x_min
            h = obs.y_max - obs.y_min
            ax.add_patch(patches.Rectangle((obs.x_min, obs.y_min), w, h, color="gray", alpha=0.6))

    ax.plot(*scenario["start"][:2], "go", markersize=10, label="Start")
    ax.plot(*scenario["goal"], "r*", markersize=12, label="Cilj")

    ax.annotate("Start", scenario["start"][:2], textcoords="offset points",
                xytext=(10, 5), fontsize=10)
    ax.annotate("Cilj", scenario["goal"], textcoords="offset points",
                xytext=(10, 5), fontsize=10)

    ax.text(5.0, 5.2, "PUT NIJE\nPRONAĐEN", ha="center", va="center",
            fontsize=14, fontweight="bold", color="red",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="red", alpha=0.8))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title(f"Okolina — {scenario['name']} (A* nije pronašao put)")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()
    plt.close()


def plot_controls(result: dict, scenario: dict, v_ref: np.ndarray = None, save_path: str = None):
    states = result["states"]
    t = np.arange(len(states)) * result["dt"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)

    ax1.plot(t, states[:, 3], "b-", linewidth=1.5, label="v stvarna")
    if v_ref is not None:
        t_ref = np.linspace(0, t[-1], len(v_ref))
        ax1.plot(t_ref, v_ref, "b--", linewidth=1.0, alpha=0.6, label="v referentna")
        ax1.legend(fontsize=8)
    ax1.set_ylabel("v [m/s]")
    ax1.grid(True, alpha=0.3)
    ax1.set_title(f"Upravljački signali — {scenario['name']}")

    ax2.plot(t, states[:, 4], "r-", linewidth=1.5)
    ax2.set_ylabel("ω [rad/s]")
    ax2.set_xlabel("t [s]")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()
    plt.close()


def plot_tracking_error(result: dict, path: np.ndarray, scenario: dict, save_path: str = None):
    states = result["states"]
    n = min(len(states), len(path))

    errors = []
    for state in states[:n]:
        dists = np.linalg.norm(path - state[:2], axis=1)
        errors.append(dists.min())

    t = np.arange(len(errors)) * result["dt"]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, errors, "g-", linewidth=1.5)
    ax.set_ylabel("Greška [m]")
    ax.set_xlabel("t [s]")
    ax.set_title(f"Greška praćenja putanje — {scenario['name']}")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()
    plt.close()
