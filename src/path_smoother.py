import numpy as np
from scipy.interpolate import splprep, splev


def _min_obstacle_dist(path: np.ndarray, obstacles: list) -> float:
    """Minimum signed distance from path points to obstacle boundaries."""
    min_dist = np.inf
    for (cx, cy, r) in obstacles:
        dists = np.sqrt((path[:, 0] - cx) ** 2 + (path[:, 1] - cy) ** 2) - r
        min_dist = min(min_dist, float(np.min(dists)))
    return min_dist


def smooth(waypoints: np.ndarray, n_points: int = 200, smoothing: float = 0.5,
           obstacles: list | None = None, r_rob: float = 0.2) -> np.ndarray:
    _, idx = np.unique(waypoints, axis=0, return_index=True)
    pts = waypoints[np.sort(idx)]

    if len(pts) < 4:
        return pts

    s_values = [smoothing, 0.3, 0.1, 0.0]
    for s in s_values:
        tck, _ = splprep([pts[:, 0], pts[:, 1]], s=s, k=3)
        t = np.linspace(0, 1, n_points)
        x_s, y_s = splev(t, tck)
        path = np.column_stack([x_s, y_s])

        if obstacles is None:
            return path

        if _min_obstacle_dist(path, obstacles) >= r_rob:
            return path

    return path  # s=0.0 passes through A* points, safe by construction


def min_smoothed_clearance(waypoints: np.ndarray, obstacles: list,
                           n_points: int = 200, smoothing: float = 0.5,
                           r_rob: float = 0.2) -> float:
    """Returns minimum clearance (m) of smoothed path from obstacle boundaries."""
    path = smooth(waypoints, n_points=n_points, smoothing=smoothing,
                  obstacles=obstacles, r_rob=r_rob)
    if not obstacles:
        return np.inf
    return _min_obstacle_dist(path, obstacles)


def velocity_profile(path: np.ndarray, v_max: float, k_curv: float = 0.5) -> np.ndarray:
    n = len(path)
    kappa = np.zeros(n)

    for i in range(1, n - 1):
        dx1 = path[i][0] - path[i-1][0]
        dy1 = path[i][1] - path[i-1][1]
        dx2 = path[i+1][0] - path[i][0]
        dy2 = path[i+1][1] - path[i][1]
        cross = dx1 * dy2 - dy1 * dx2
        norm = (np.hypot(dx1, dy1) * np.hypot(dx2, dy2)) + 1e-9
        seg_len = (np.hypot(dx1, dy1) + np.hypot(dx2, dy2)) / 2 + 1e-9
        kappa[i] = abs(cross) / (norm * seg_len)

    return v_max / (1.0 + k_curv * kappa)
