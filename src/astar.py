import heapq
import numpy as np
import yaml
from src.obstacles import to_acados_list


def load_params(path="config/params.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def plan(start: np.ndarray, goal: np.ndarray, obstacles: list) -> np.ndarray:
    p = load_params()
    env = p["environment"]
    res = p["astar"]["grid_resolution"]
    inflation = p["astar"]["obstacle_inflation"] + p["robot"]["radius"]

    xs = np.arange(env["x_min"], env["x_max"] + res, res)
    ys = np.arange(env["y_min"], env["y_max"] + res, res)
    nx, ny = len(xs), len(ys)

    def world_to_grid(pt):
        i = int(round((pt[0] - env["x_min"]) / res))
        j = int(round((pt[1] - env["y_min"]) / res))
        return (np.clip(i, 0, nx - 1), np.clip(j, 0, ny - 1))

    def grid_to_world(i, j):
        return np.array([env["x_min"] + i * res, env["y_min"] + j * res])

    occupied = np.zeros((nx, ny), dtype=bool)
    for (cx, cy, r) in to_acados_list(obstacles):
        for i in range(nx):
            for j in range(ny):
                wx, wy = grid_to_world(i, j)
                if (wx - cx)**2 + (wy - cy)**2 <= (r + inflation)**2:
                    occupied[i, j] = True

    start_g = world_to_grid(start)
    goal_g  = world_to_grid(goal)

    def heuristic(a, b):
        return np.hypot(a[0] - b[0], a[1] - b[1])

    open_set = [(heuristic(start_g, goal_g), 0.0, start_g)]
    came_from = {}
    g_score = {start_g: 0.0}
    neighbours = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

    while open_set:
        _, g, current = heapq.heappop(open_set)

        if current == goal_g:
            path = []
            while current in came_from:
                path.append(grid_to_world(*current))
                current = came_from[current]
            path.append(grid_to_world(*start_g))
            return np.array(path[::-1])

        for di, dj in neighbours:
            nb = (current[0] + di, current[1] + dj)
            if not (0 <= nb[0] < nx and 0 <= nb[1] < ny):
                continue
            if occupied[nb]:
                continue
            step = np.hypot(di, dj)
            new_g = g + step
            if new_g < g_score.get(nb, np.inf):
                g_score[nb] = new_g
                came_from[nb] = current
                f = new_g + heuristic(nb, goal_g)
                heapq.heappush(open_set, (f, new_g, nb))

    raise RuntimeError("A*: nema puta od starta do cilja")
