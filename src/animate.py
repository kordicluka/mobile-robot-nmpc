import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from src.obstacles import Circle, Rectangle


def animate(result: dict, scenario: dict, path: np.ndarray,
            speed: float = 3.0, save_path: str = None):
    states = result["states"]
    dt = result["dt"]
    interval_ms = int(dt * 1000 / speed)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title(f"Simulacija — {scenario['name']}")

    for obs in scenario["obstacles"]:
        if isinstance(obs, Circle):
            ax.add_patch(plt.Circle((obs.cx, obs.cy), obs.r, color="gray", alpha=0.6))
        elif isinstance(obs, Rectangle):
            w = obs.x_max - obs.x_min
            h = obs.y_max - obs.y_min
            ax.add_patch(patches.Rectangle(
                (obs.x_min, obs.y_min), w, h, color="gray", alpha=0.6))

    ax.plot(path[:, 0], path[:, 1], "b--", linewidth=1.0, alpha=0.5, label="Ref. putanja")
    ax.plot(*scenario["start"][:2], "go", markersize=10)
    ax.plot(*scenario["goal"], "r*", markersize=12)

    trail, = ax.plot([], [], "r-", linewidth=1.5, alpha=0.7)
    robot_dot, = ax.plot([], [], "ro", markersize=8)

    arrow_len = 0.4
    arrow = ax.annotate("", xy=(0, 0), xytext=(0, 0),
                         arrowprops=dict(arrowstyle="->", color="darkred", lw=2))

    time_text = ax.text(0.02, 0.96, "", transform=ax.transAxes, fontsize=9)
    ax.legend(loc="upper right", fontsize=8)

    def update(frame):
        x, y, theta = states[frame, :3]

        trail.set_data(states[:frame+1, 0], states[:frame+1, 1])
        robot_dot.set_data([x], [y])

        arrow.set_position((x, y))
        arrow.xy = (x + arrow_len * np.cos(theta), y + arrow_len * np.sin(theta))
        arrow.xytext = (x, y)

        time_text.set_text(f"t = {frame * dt:.1f}s")
        return trail, robot_dot, arrow, time_text

    anim = FuncAnimation(fig, update, frames=len(states),
                         interval=interval_ms, blit=False)

    if save_path:
        anim.save(save_path, writer="pillow" if save_path.endswith(".gif") else "ffmpeg")
        print(f"Animacija spremljena: {save_path}")
    else:
        plt.show()

    plt.close()
