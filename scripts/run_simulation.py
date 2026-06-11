import sys
import os
import argparse
import yaml
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.scenarios import get_scenario
from src.obstacles import to_acados_list
from src.astar import plan
from src.path_smoother import smooth, velocity_profile
from src.mpc_solver import create_solver
from src.simulation import run_simulation
from src.metrics import compute, print_metrics
from src.plot import plot_trajectory, plot_controls, plot_tracking_error, plot_environment
from src.animate import animate

SCENARIOS = ["baseline", "one_obstacle", "narrow", "l_corridor", "u_shape",
             "perturbation", "cluttered", "blocked"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=SCENARIOS)
    parser.add_argument("--save",    action="store_true", help="Spremi grafove u results/figures/")
    parser.add_argument("--animate", action="store_true", help="Pokreni animaciju")
    parser.add_argument("--speed",   type=float, default=3.0, help="Brzina animacije (default 3x)")
    args = parser.parse_args()

    os.makedirs("results/figures", exist_ok=True)
    prefix = f"results/figures/{args.scenario}"

    print(f"\nScenarij: {args.scenario}")
    print("-" * 40)

    s = get_scenario(args.scenario)

    print("Planiram putanju (A*)...")

    try:
        raw_path = plan(s["start"][:2], s["goal"], s["obstacles"])

    except RuntimeError as e:
        print(f"\n  ✗ A* nije pronašao put: {e}")
        print("  Cilj je nedostižan — prikazujem okolinu.")

        plot_environment(s, save_path=f"{prefix}_env.png" if args.save else None)

        if args.save:
            print(f"\nGraf okoline spremljen u results/figures/{args.scenario}_env.png")

        return

    obs_list = to_acados_list(s["obstacles"])
    path = smooth(raw_path, obstacles=obs_list)

    with open("config/params.yaml") as f:
        params = yaml.safe_load(f)
        v_max = params["robot"]["v_max"]

    if obs_list:
        from src.path_smoother import _min_obstacle_dist
        clearance = _min_obstacle_dist(path, obs_list)
        print(f"  {len(raw_path)} → {len(path)} točaka (izglađeno), min. udaljenost od prepreka: {clearance:.4f} m")
    else:
        print(f"  {len(raw_path)} → {len(path)} točaka (izglađeno)")

    v_ref = velocity_profile(path, v_max)

    print("Kreiram NMPC solver...")

    solver = create_solver(obstacles=to_acados_list(s["obstacles"]))

    print("Pokrećem simulaciju...")

    result = run_simulation(solver, path, s["start"], s["perturbation"])

    print("\nMetrike:")
    m = compute(result, path, s)
    print_metrics(m)

    save = args.save

    plot_trajectory(result, s, path,  save_path=f"{prefix}_traj.png"     if save else None)
    plot_controls(result, s, v_ref=v_ref, save_path=f"{prefix}_controls.png"  if save else None)
    plot_tracking_error(result, path, s, save_path=f"{prefix}_error.png"  if save else None)

    if args.animate:
        gif = f"{prefix}.gif" if save else None
        animate(result, s, path, speed=args.speed, save_path=gif)

    if save:
        print(f"\nGrafovi spremljeni u results/figures/{args.scenario}_*.png")

if __name__ == "__main__":
    main()
