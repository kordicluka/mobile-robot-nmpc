import numpy as np
import yaml
import os
import csv
from src.scenarios import get_scenario
from src.obstacles import to_acados_list
from src.astar import plan
from src.path_smoother import smooth
from src.mpc_solver import create_solver
from src.simulation import run_simulation
from src.metrics import compute


def _update_params(updates: dict):
    with open("config/params.yaml") as f:
        p = yaml.safe_load(f)
    for key, val in updates.items():
        keys = key.split(".")
        d = p
        for k in keys[:-1]:
            d = d[k]
        d[keys[-1]] = val
    with open("config/params.yaml", "w") as f:
        yaml.dump(p, f, allow_unicode=True)


def _run_scenario(scenario_name="one_obstacle") -> tuple:
    s = get_scenario(scenario_name)
    path = smooth(plan(s["start"][:2], s["goal"], s["obstacles"]))
    solver = create_solver(obstacles=to_acados_list(s["obstacles"]))
    result = run_simulation(solver, path, s["start"])
    m = compute(result, path, s)
    return m["rmse"], m["cpu_mean_ms"]


def tune_horizon(N_values=(5, 10, 15, 20, 30, 40), scenario="one_obstacle") -> list[dict]:
    results = []
    print("Tuning horizonta N...")
    for N in N_values:
        _update_params({"mpc.N": int(N), "mpc.solver_type": "SQP_RTI"})
        rmse, cpu = _run_scenario(scenario)
        results.append({"N": N, "rmse": rmse, "cpu_ms": cpu})
        print(f"  N={N:3d}  RMSE={rmse:.4f}m  CPU={cpu:.2f}ms")
    _update_params({"mpc.N": 20})
    return results


def tune_weights(scenario="one_obstacle") -> list[dict]:
    configs = [
        {"label": "Q>>R (čvrsto praćenje)", "Q": [50.0, 50.0, 5.0],  "R": [0.01, 0.01]},
        {"label": "Q>R (balansirano)",       "Q": [10.0, 10.0, 1.0],  "R": [0.1,  0.1]},
        {"label": "Q~R (umjereno)",          "Q": [5.0,  5.0,  0.5],  "R": [1.0,  1.0]},
        {"label": "Q<R (glatko upravljanje)","Q": [1.0,  1.0,  0.1],  "R": [5.0,  5.0]},
    ]
    results = []
    print("Tuning težina Q/R...")
    for cfg in configs:
        _update_params({"mpc.Q": cfg["Q"], "mpc.R": cfg["R"]})
        rmse, cpu = _run_scenario(scenario)
        results.append({"label": cfg["label"], "rmse": rmse, "cpu_ms": cpu})
        print(f"  {cfg['label']:35s}  RMSE={rmse:.4f}m  CPU={cpu:.2f}ms")
    _update_params({"mpc.Q": [10.0, 10.0, 1.0], "mpc.R": [0.1, 0.1]})
    return results


def run_all(save_csv=True):
    os.makedirs("results/data", exist_ok=True)

    horizon_results = tune_horizon()
    weight_results = tune_weights()

    if save_csv:
        with open("results/data/tuning_horizon.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["N", "rmse", "cpu_ms"])
            w.writeheader()
            w.writerows(horizon_results)

        with open("results/data/tuning_weights.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["label", "rmse", "cpu_ms"])
            w.writeheader()
            w.writerows(weight_results)

        print("\nRezultati spremljeni u results/data/")

    return horizon_results, weight_results
