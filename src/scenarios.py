import numpy as np
from src.obstacles import Circle, Rectangle


def get_scenario(name: str) -> dict:
    scenarios = {
        "baseline":       _baseline,
        "one_obstacle":   _one_obstacle,
        "narrow":         _narrow,
        "l_corridor":     _l_corridor,
        "u_shape":        _u_shape,
        "perturbation":   _perturbation,
        "cluttered":      _cluttered,
        "blocked":        _blocked,
    }
    if name not in scenarios:
        raise ValueError(f"Nepoznati scenarij '{name}'. Dostupni: {list(scenarios)}")
    return scenarios[name]()


def _baseline():
    return {
        "name": "baseline",
        "start": np.array([0.5, 0.5, 0.0]),
        "goal":  np.array([9.5, 9.5]),
        "obstacles": [],
        "perturbation": None,
    }


def _one_obstacle():
    return {
        "name": "one_obstacle",
        "start": np.array([0.5, 0.5, 0.0]),
        "goal":  np.array([9.5, 9.5]),
        "obstacles": [Circle(5.0, 5.0, 1.0)],
        "perturbation": None,
    }


def _narrow():
    return {
        "name": "narrow",
        "start": np.array([0.5, 5.0, 0.0]),
        "goal":  np.array([9.5, 5.0]),
        "obstacles": [
            Circle(5.0, 3.5, 1.2),
            Circle(5.0, 6.5, 1.2),
        ],
        "perturbation": None,
    }


def _l_corridor():
    return {
        "name": "l_corridor",
        "start": np.array([0.5, 1.0, 0.0]),
        "goal":  np.array([9.0, 9.0]),
        "obstacles": [
            Rectangle(0.0, 3.5, 7.5, 10.0),
        ],
        "perturbation": None,
    }


def _u_shape():
    return {
        "name": "u_shape",
        "start": np.array([5.0, 0.5, np.pi / 2]),
        "goal":  np.array([5.0, 9.5]),
        "obstacles": [
            Rectangle(2.0, 2.0, 3.0, 7.0),
            Rectangle(7.0, 2.0, 8.0, 7.0),
            Rectangle(2.0, 7.0, 8.0, 8.0),
        ],
        "perturbation": None,
    }


def _perturbation():
    return {
        "name": "perturbation",
        "start": np.array([0.5, 5.0, 0.0]),
        "goal":  np.array([9.5, 5.0]),
        "obstacles": [],
        "perturbation": {"step": 30, "dx": 0.0, "dy": 1.0},
    }


def _blocked():
    return {
        "name": "blocked",
        "start": np.array([0.5, 5.0, 0.0]),
        "goal":  np.array([9.5, 5.0]),
        "obstacles": [
            Circle(5.0, 0.0,  1.5),
            Circle(5.0, 2.5,  1.5),
            Circle(5.0, 5.0,  1.5),
            Circle(5.0, 7.5,  1.5),
            Circle(5.0, 10.0, 1.5),
        ],
        "perturbation": None,
    }


def _cluttered():
    return {
        "name": "cluttered",
        "start": np.array([0.5, 0.5, 0.0]),
        "goal":  np.array([9.5, 9.5]),
        "obstacles": [
            Circle(2.5, 2.0, 0.7),
            Circle(5.5, 1.5, 0.6),
            Circle(1.5, 5.5, 0.8),
            Circle(4.5, 4.5, 0.7),
            Circle(7.5, 3.5, 0.6),
            Circle(3.0, 8.0, 0.7),
            Circle(6.5, 7.0, 0.8),
        ],
        "perturbation": None,
    }
