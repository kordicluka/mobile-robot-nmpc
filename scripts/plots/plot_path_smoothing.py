import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.scenarios import get_scenario
from src.obstacles import to_acados_list
from src.astar import plan
from src.path_smoother import smooth

                                                                               
s = get_scenario("one_obstacle")

raw_path   = plan(s["start"][:2], s["goal"], s["obstacles"])
smooth_path = smooth(raw_path)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

obs_color = '#aaaaaa'

def draw_scene(ax):
    from src.obstacles import to_acados_list
    for (cx, cy, r) in to_acados_list(s["obstacles"]):
        circle = plt.Circle((cx, cy), r, color=obs_color, zorder=2)
        ax.add_patch(circle)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.set_xlabel('$x$ [m]', fontsize=10)
    ax.set_ylabel('$y$ [m]', fontsize=10)
                  
    ax.plot(s["start"][0], s["start"][1], 'o', color='limegreen', markersize=10, zorder=5)
    ax.plot(s["goal"][0],  s["goal"][1],  '*', color='tomato',    markersize=14, zorder=5)

                                  
draw_scene(axes[0])
axes[0].plot(raw_path[:, 0], raw_path[:, 1], 'o-',
             color='steelblue', linewidth=1.5, markersize=4,
             label=f'A* putanja ({len(raw_path)} točaka)', zorder=3)
axes[0].set_title(f'Gruba A* putanja\n({len(raw_path)} točaka, oštre promjene smjera)', fontsize=10)
axes[0].legend(fontsize=9, loc='upper left')

                                  
draw_scene(axes[1])
axes[1].plot(raw_path[:, 0], raw_path[:, 1], 'o',
             color='steelblue', linewidth=1.0, markersize=3,
             alpha=0.4, label=f'A* točke ({len(raw_path)})', zorder=3)
axes[1].plot(smooth_path[:, 0], smooth_path[:, 1], '-',
             color='tomato', linewidth=2.5,
             label=f'B-spline ({len(smooth_path)} točaka)', zorder=4)
axes[1].set_title(f'Izglađena B-spline krivulja\n({len(smooth_path)} točaka, glatki zavoji)', fontsize=10)
axes[1].legend(fontsize=9, loc='upper left')

plt.tight_layout()
plt.savefig('latex/figures/path_smoothing.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Slika spremljena. A* točaka: {len(raw_path)}, B-spline točaka: {len(smooth_path)}")
