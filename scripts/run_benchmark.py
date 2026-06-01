import sys
import os
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.benchmark import run_all as run_benchmark
from src.tuning import run_all as run_tuning
from src.scenarios import get_scenario
from src.obstacles import to_acados_list
from src.astar import plan
from src.path_smoother import smooth, velocity_profile
from src.mpc_solver import create_solver
from src.simulation import run_simulation
from src.plot import plot_trajectory, plot_controls, plot_tracking_error, plot_environment

import numpy as np
import matplotlib.pyplot as plt

def plot_tuning(horizon_results, weight_results):
    os.makedirs("results/figures", exist_ok=True)

                     
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    Ns    = [r["N"]      for r in horizon_results]
    rmses = [r["rmse"]   for r in horizon_results]
    cpus  = [r["cpu_ms"] for r in horizon_results]

    ax1.plot(Ns, rmses, "b-o")
    ax1.set_xlabel("N (horizont)")
    ax1.set_ylabel("RMSE [m]")
    ax1.set_title("Horizont vs. greška praćenja")
    ax1.grid(True, alpha=0.3)

    ax2.plot(Ns, cpus, "r-o")
    ax2.set_xlabel("N (horizont)")
    ax2.set_ylabel("CPU [ms/korak]")
    ax2.set_title("Horizont vs. računalna složenost")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("results/figures/tuning_horizon.png", dpi=150)
    plt.close()

                 
    fig, ax = plt.subplots(figsize=(8, 4))
    labels = [r["label"].split("(")[0].strip() for r in weight_results]
    rmses  = [r["rmse"] for r in weight_results]
    ax.bar(labels, rmses, color="steelblue", alpha=0.8)
    ax.set_ylabel("RMSE [m]")
    ax.set_title("Utjecaj omjera Q/R na grešku praćenja")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig("results/figures/tuning_weights.png", dpi=150)
    plt.close()

    print("Tuning grafovi spremljeni.")

def plot_all_scenarios():
    scenarios = ["baseline", "one_obstacle", "narrow", "l_corridor", "u_shape", "perturbation", "cluttered"]
    for name in scenarios:
        try:
            s = get_scenario(name)
            path = smooth(plan(s["start"][:2], s["goal"], s["obstacles"]))
            with open("config/params.yaml") as f:
                v_max = yaml.safe_load(f)["robot"]["v_max"]
            v_ref = velocity_profile(path, v_max)
            solver = create_solver(obstacles=to_acados_list(s["obstacles"]))
            result = run_simulation(solver, path, s["start"], s["perturbation"])
            plot_trajectory(result, s, path, f"results/figures/{name}_traj.png")
            plot_controls(result, s, v_ref=v_ref, save_path=f"results/figures/{name}_controls.png")
            plot_tracking_error(result, path, s, f"results/figures/{name}_error.png")
            print(f"  [{name}] grafovi spremljeni")
        except Exception as e:
            print(f"  [{name}] greška: {e}")

                                                                            
    s = get_scenario("blocked")
    plot_environment(s, save_path="results/figures/blocked_env.png")
    print("  [blocked] graf okoline spremljen")

def main():
    print("=" * 50)
    print("BENCHMARK — svi scenariji")
    print("=" * 50)
    run_benchmark(solver_types=("SQP_RTI", "SQP"))

    print("\n" + "=" * 50)
    print("TUNING ANALIZA")
    print("=" * 50)
    horizon_r, weight_r = run_tuning()
    plot_tuning(horizon_r, weight_r)

    print("\n" + "=" * 50)
    print("GRAFOVI ZA RAD")
    print("=" * 50)
    plot_all_scenarios()

    print("\nGotovo. Sve u results/")

if __name__ == "__main__":
    main()
