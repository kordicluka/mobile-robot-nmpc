import numpy as np
from scipy.interpolate import splprep, splev


def smooth(waypoints: np.ndarray, n_points: int = 200, smoothing: float = 0.5) -> np.ndarray:
    _, idx = np.unique(waypoints, axis=0, return_index=True)
    pts = waypoints[np.sort(idx)]

    if len(pts) < 4:
        return pts

    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=smoothing, k=3)
    t = np.linspace(0, 1, n_points)
    x_s, y_s = splev(t, tck)
    return np.column_stack([x_s, y_s])


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
