import numpy as np
import csv
import os
import yaml
from src.scenarios import get_scenario
from src.obstacles import to_acados_list
from src.astar import plan
from src.path_smoother import smooth
from src.mpc_solver import create_solver
from src.simulation import run_simulation
from src.metrics import compute


SCENARIOS = ["baseline", "one_obstacle", "narrow", "l_corridor", "u_shape", "perturbation", "cluttered"]


def _set_param(key: str, value):
    with open("config/params.yaml") as f:
        p = yaml.safe_load(f)
    keys = key.split(".")
    d = p
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value
    with open("config/params.yaml", "w") as f:
        yaml.dump(p, f, allow_unicode=True)


def run_all(solver_types=("SQP_RTI", "SQP"), save_csv=True) -> list[dict]:
    results = []

    for scenario_name in SCENARIOS:
        s = get_scenario(scenario_name)
        obs_list = to_acados_list(s["obstacles"])

        try:
            raw_path = plan(s["start"][:2], s["goal"], s["obstacles"])
            path = smooth(raw_path)
        except RuntimeError as e:
            print(f"[{scenario_name}] A* greška: {e}")
            continue

        for solver_type in solver_types:
            _set_solver_type(solver_type)
            try:
                solver = create_solver(obstacles=obs_list)
                sim_result = run_simulation(solver, path, s["start"], s["perturbation"])
                m = compute(sim_result, path, s)
                m["scenario"] = scenario_name
                m["solver_type"] = solver_type
                results.append(m)
                print(f"[{scenario_name:15}] [{solver_type:7}] "
                      f"RMSE={m['rmse']:.3f}m  "
                      f"CPU={m['cpu_mean_ms']:.2f}ms  "
                      f"t={m['time_to_goal_s']:.1f}s  "
                      f"stigao={m['reached_goal']}")
            except Exception as e:
                print(f"[{scenario_name}] [{solver_type}] greška: {e}")

    if save_csv and results:
        _save_csv(results)

    return results


def _set_solver_type(solver_type: str):
    _set_param("mpc.solver_type", solver_type)


def _save_csv(results: list[dict]):
    os.makedirs("results/data", exist_ok=True)
    keys = ["scenario", "solver_type", "rmse", "cte_mean", "cte_max",
            "heading_err_mean", "time_to_goal_s", "cpu_mean_ms", "cpu_max_ms",
            "reached_goal", "recovery_steps"]
    with open("results/data/benchmark.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    print("\nRezultati spremljeni u results/data/benchmark.csv")
