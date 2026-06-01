import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
fig.subplots_adjust(wspace=0.08)

wp_x = np.array([0.0, 1.5, 3.0, 4.5, 6.0, 7.5])
wp_y = np.zeros(len(wp_x))

                                                     
                                                                
configs = [
    (3.2, 0.28, r'(a) Robot blizu $w_2$: $d_{next} > d_{curr}$ — wp_idx stoji'),
    (3.9, 0.28, r'(b) Robot prošao polovicu: $d_{next} \leq d_{curr}$ — wp_idx napreduje'),
]

for ax, (rx, ry, panel_title) in zip(axes, configs):
    robot_pos = np.array([rx, ry])
    w_curr = np.array([wp_x[2], 0.0])                         
    w_next = np.array([wp_x[3], 0.0])                           

    d_curr = np.linalg.norm(robot_pos - w_curr)
    d_next = np.linalg.norm(robot_pos - w_next)
    advancing = d_next <= d_curr

                        
    ax.plot(wp_x, wp_y, '--', color='#888888', lw=1.5, zorder=1)
    ax.scatter(wp_x, wp_y, s=55, color='#555555', zorder=3)
    for i, (x, y) in enumerate(zip(wp_x, wp_y)):
        ax.text(x, y - 0.09, f'$w_{i}$', ha='center', va='top', fontsize=9,
                color='#555555')

                                                  
    ax.scatter(*w_curr, s=200, color='#fee090', edgecolors='#d73027', lw=2.0, zorder=4)
    ax.text(wp_x[2], -0.22, 'wp_idx', ha='center', va='top', fontsize=8,
            color='#d73027', style='italic')

                                                                 
    if advancing:
        ax.scatter(*w_next, s=200, color='#a6d96a', edgecolors='#4dac26', lw=2.0, zorder=4)
        ax.text(wp_x[3], -0.22, 'wp_idx + 1\n→ postaje wp_idx', ha='center', va='top',
                fontsize=7.5, color='#4dac26', style='italic')
    else:
        ax.scatter(*w_next, s=80, color='#dddddd', edgecolors='#888888', lw=1.0, zorder=4)

                        
    ax.plot([rx, w_curr[0]], [ry, w_curr[1]], '-', color='#d73027', lw=2.2, zorder=3)
    ax.plot([rx, w_next[0]], [ry, w_next[1]], '-', color='#4dac26', lw=2.2, zorder=3)

                                              
    mx_c = (rx + w_curr[0]) / 2
    my_c = (ry + w_curr[1]) / 2
    mx_n = (rx + w_next[0]) / 2
    my_n = (ry + w_next[1]) / 2

    ax.text(mx_c - 0.1, my_c + 0.11,
            f'$d_{{curr}} = {d_curr:.2f}$ m', fontsize=9, color='#d73027', ha='right')
    ax.text(mx_n + 0.1, my_n + 0.11,
            f'$d_{{next}} = {d_next:.2f}$ m', fontsize=9, color='#4dac26', ha='left')

                  
    ax.scatter(*robot_pos, s=150, color='#2166ac', zorder=5)
    ax.text(rx, ry + 0.09, 'robot', ha='center', va='bottom', fontsize=9,
            color='#2166ac', fontweight='bold')

    ax.set_title(panel_title, fontsize=10, pad=7)
    ax.set_xlim(-0.3, 8.2)
    ax.set_ylim(-0.48, 0.82)
    ax.set_xlabel('x [m]', fontsize=10)
    ax.grid(True, alpha=0.2)
    ax.axhline(0, color='#cccccc', lw=0.8, zorder=0)

axes[0].set_ylabel('y [m]', fontsize=10)

plt.tight_layout()
plt.savefig('latex/figures/waypoint_tracking.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/waypoint_tracking.png")
