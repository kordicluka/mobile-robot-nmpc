import numpy as np
import time
import yaml

from acados_template import AcadosOcpSolver


def load_params(path="config/params.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def _rk4_step(x, u, dt):
    def f(x, u):
        v, w = x[3], x[4]
        dv, dw = u
        return np.array([v * np.cos(x[2]), v * np.sin(x[2]), w, dv, dw])

    k1 = f(x, u)
    k2 = f(x + dt / 2 * k1, u)
    k3 = f(x + dt / 2 * k2, u)
    k4 = f(x + dt * k3, u)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def run_simulation(
    solver: AcadosOcpSolver,
    waypoints: np.ndarray,
    x0: np.ndarray,
    perturbation: dict = None,
) -> dict:
    p = load_params()
    dt = p["mpc"]["dt"]
    N = p["mpc"]["N"]
    max_steps = p["simulation"]["max_steps"]
    tol = p["simulation"]["goal_tolerance"]

    x = np.concatenate([x0[:3], [0.0, 0.0]])
    wp_idx = 0
    goal = waypoints[-1]
    states, controls, solve_times = [x.copy()], [], []

    for k in range(N + 1):
        ref_idx = min(k, len(waypoints) - 1)
        xr, yr = waypoints[ref_idx]
        if ref_idx + 1 < len(waypoints):
            theta_k = np.arctan2(waypoints[ref_idx + 1][1] - yr,
                                 waypoints[ref_idx + 1][0] - xr)
        else:
            theta_k = x[2]
        solver.set(k, "x", np.array([xr, yr, theta_k, 0.3, 0.0]))
        if k < N:
            solver.set(k, "u", np.array([0.0, 0.0]))

    for step in range(max_steps):

        while wp_idx < len(waypoints) - 1:
            d_curr = np.linalg.norm(x[:2] - waypoints[wp_idx])
            d_next = np.linalg.norm(x[:2] - waypoints[wp_idx + 1])
            if d_next <= d_curr:
                wp_idx += 1
            else:
                break

        for k in range(N):
            ref_idx = min(wp_idx + k, len(waypoints) - 1)
            xr, yr = waypoints[ref_idx]
            if ref_idx + 1 < len(waypoints):
                dx = waypoints[ref_idx + 1][0] - xr
                dy = waypoints[ref_idx + 1][1] - yr
                theta_ref = np.arctan2(dy, dx)
            else:
                theta_ref = x[2]
            solver.set(k, "yref", np.array([xr, yr, theta_ref, 0.0, 0.0]))

        xr, yr = waypoints[min(wp_idx + N, len(waypoints) - 1)]
        solver.set(N, "yref", np.array([xr, yr, x[2]]))

        solver.set(0, "lbx", x)
        solver.set(0, "ubx", x)

        t0 = time.perf_counter()
        solver.solve()
        solve_times.append(time.perf_counter() - t0)

        u = solver.get(0, "u")
        x = _rk4_step(x, u, dt)

        if perturbation and step == perturbation.get("step", -1):
            x[0] += perturbation.get("dx", 0.0)
            x[1] += perturbation.get("dy", 0.0)

        states.append(x.copy())
        controls.append(u.copy())

        if np.linalg.norm(x[:2] - goal) < tol:
            break

    return {
        "states": np.array(states),
        "controls": np.array(controls),
        "solve_times": np.array(solve_times),
        "reached_goal": np.linalg.norm(x[:2] - goal) < tol,
        "steps": len(controls),
        "dt": dt,
    }
