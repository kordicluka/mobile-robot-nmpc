import numpy as np
from dataclasses import dataclass


@dataclass
class Circle:
    cx: float
    cy: float
    r: float

    def to_tuple(self):
        return (self.cx, self.cy, self.r)


@dataclass
class Rectangle:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def to_circles(self, r: float = 0.2) -> list[Circle]:
        circles = []
        x = self.x_min + r
        while x <= self.x_max:
            y = self.y_min + r
            while y <= self.y_max:
                circles.append(Circle(x, y, r))
                y += r * 1.5
            x += r * 1.5
        return circles


def to_acados_list(obstacles: list) -> list[tuple]:
    result = []
    for obs in obstacles:
        if isinstance(obs, Circle):
            result.append(obs.to_tuple())
        elif isinstance(obs, Rectangle):
            result.extend(c.to_tuple() for c in obs.to_circles())
    return result
