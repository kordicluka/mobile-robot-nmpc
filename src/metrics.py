import numpy as np


def compute(result: dict, path: np.ndarray, scenario: dict) -> dict:
    states = result["states"]
    controls = result["controls"]
    solve_times = result["solve_times"]
    dt = result["dt"]

    errors = []
    cte_list = []
    heading_errors = []

    for i, state in enumerate(states[:-1]):
        dists = np.linalg.norm(path - state[:2], axis=1)
        idx = np.argmin(dists)
        errors.append(dists[idx])

        if idx + 1 < len(path):
            seg = path[idx + 1] - path[idx]
            seg_norm = seg / (np.linalg.norm(seg) + 1e-9)
            diff = state[:2] - path[idx]
            cte = abs(diff[0] * seg_norm[1] - diff[1] * seg_norm[0])
        else:
            cte = dists[idx]
        cte_list.append(cte)

        if idx + 1 < len(path):
            seg = path[idx + 1] - path[idx]
            theta_ref = np.arctan2(seg[1], seg[0])
        else:
            theta_ref = state[2]
        he = abs(np.arctan2(np.sin(state[2] - theta_ref), np.cos(state[2] - theta_ref)))
        heading_errors.append(he)

    errors = np.array(errors)
    cte_list = np.array(cte_list)
    heading_errors = np.array(heading_errors)

    cpu_mean_ms = solve_times.mean() * 1000
    cpu_max_ms = solve_times.max() * 1000

    recovery_steps = None
    if scenario.get("perturbation"):
        p_step = scenario["perturbation"]["step"]
        threshold = 0.3
        for i in range(p_step + 1, len(errors)):
            if errors[i] < threshold:
                recovery_steps = i - p_step
                break

    return {
        "rmse":             float(np.sqrt(np.mean(errors**2))),
        "cte_mean":         float(cte_list.mean()),
        "cte_max":          float(cte_list.max()),
        "heading_err_mean": float(np.degrees(heading_errors.mean())),
        "heading_err_max":  float(np.degrees(heading_errors.max())),
        "time_to_goal_s":   float(result["steps"] * dt),
        "cpu_mean_ms":      float(cpu_mean_ms),
        "cpu_max_ms":       float(cpu_max_ms),
        "reached_goal":     result["reached_goal"],
        "recovery_steps":   recovery_steps,
    }


def print_metrics(m: dict):
    print(f"  RMSE:              {m['rmse']:.4f} m")
    print(f"  CTE srednji:       {m['cte_mean']:.4f} m")
    print(f"  CTE max:           {m['cte_max']:.4f} m")
    print(f"  Heading err:       {m['heading_err_mean']:.2f}° (max {m['heading_err_max']:.2f}°)")
    print(f"  Vrijeme do cilja:  {m['time_to_goal_s']:.2f} s")
    print(f"  CPU prosjek:       {m['cpu_mean_ms']:.2f} ms")
    print(f"  CPU max:           {m['cpu_max_ms']:.2f} ms")
    print(f"  Stigao do cilja:   {m['reached_goal']}")
    if m["recovery_steps"] is not None:
        print(f"  Oporavak:          {m['recovery_steps']} koraka")
