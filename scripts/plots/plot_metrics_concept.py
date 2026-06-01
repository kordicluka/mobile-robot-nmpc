import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

                                                                                
ax = axes[0]

wp_x = np.array([0.0, 2.0, 4.0, 6.0])
wp_y = np.zeros(4)
ax.plot(wp_x, wp_y, '--', color='#888888', lw=1.5, zorder=1)
ax.scatter(wp_x, wp_y, s=60, color='#555555', zorder=3)
for i, (x, y) in enumerate(zip(wp_x, wp_y)):
    if i == 1:
        continue                                     
    ax.text(x, y - 0.09, f'$w_{i}$', ha='center', va='top', fontsize=9, color='#555555')

       
rx, ry = 1.5, 0.75
ax.scatter(rx, ry, s=150, color='#2166ac', zorder=5)
ax.text(rx - 0.12, ry + 0.07, r'robot $(p_k)$', ha='right', va='bottom',
        fontsize=9, color='#2166ac', fontweight='bold')

                                             
nearest_wp = np.array([2.0, 0.0])
d_k = np.linalg.norm(np.array([rx, ry]) - nearest_wp)
ax.scatter(*nearest_wp, s=200, color='#fee090', edgecolors='#d73027', lw=2.0, zorder=4)
ax.text(nearest_wp[0] + 0.12, nearest_wp[1] - 0.09, r'$w_{j^*}$' + '\n(najbliži)',
        ha='left', va='top', fontsize=8.5, color='#d73027')

ax.plot([rx, nearest_wp[0]], [ry, nearest_wp[1]], '-', color='#d73027', lw=2.2, zorder=4)
ax.text(1.88, 0.45, f'$d_k = {d_k:.2f}$ m  ' + r'$\rightarrow$ RMSE',
        fontsize=9, color='#d73027', ha='left')

                                                                               
foot = np.array([rx, 0.0])
cte = ry
ax.scatter(*foot, s=80, color='#c2e699', edgecolors='#4dac26', lw=1.5, zorder=4)
ax.plot([rx, foot[0]], [ry, foot[1]], '-', color='#4dac26', lw=2.2, zorder=4)
ax.text(rx - 0.12, ry / 2, f'$\\mathrm{{CTE}} = {cte:.2f}$ m', fontsize=9,
        color='#4dac26', ha='right', va='center')

                              
sq = 0.07
ax.plot([rx + sq, rx + sq, rx], [0.0, sq, sq], color='#4dac26', lw=1.2, zorder=5)

ax.set_title('(a) RMSE i CTE', fontsize=10, pad=7)
ax.set_xlim(-0.4, 7.0)
ax.set_ylim(-0.35, 1.35)
ax.set_xlabel('x [m]', fontsize=10)
ax.set_ylabel('y [m]', fontsize=10)
ax.grid(True, alpha=0.2)
ax.axhline(0, color='#cccccc', lw=0.8, zorder=0)

                                                                                
ax = axes[1]

path_angle_deg = 30
path_angle = np.radians(path_angle_deg)
robot_angle_deg = 52
robot_angle = np.radians(robot_angle_deg)
heading_err_deg = robot_angle_deg - path_angle_deg

px0, py0 = 0.4, 0.2
path_len = 4.5
ax.plot([px0, px0 + path_len * np.cos(path_angle)],
        [py0, py0 + path_len * np.sin(path_angle)],
        '--', color='#888888', lw=1.5, zorder=1)

                  
t = 2.0
robot_x = px0 + t * np.cos(path_angle)
robot_y = py0 + t * np.sin(path_angle)
ax.scatter(robot_x, robot_y, s=150, color='#2166ac', zorder=5)
ax.text(robot_x - 0.12, robot_y - 0.12, 'robot', ha='right', va='top',
        fontsize=9, color='#2166ac', fontweight='bold')

                               
arrow_len = 1.3
ax.annotate('', xy=(robot_x + arrow_len * np.cos(path_angle),
                     robot_y + arrow_len * np.sin(path_angle)),
            xytext=(robot_x, robot_y),
            arrowprops=dict(arrowstyle='->', color='#4dac26', lw=2.0))
ax.text(robot_x + (arrow_len + 0.15) * np.cos(path_angle),
        robot_y + (arrow_len + 0.15) * np.sin(path_angle) - 0.12,
        r'$\theta_{ref}$', fontsize=11, color='#4dac26', va='top', ha='center')

                                
ax.annotate('', xy=(robot_x + arrow_len * np.cos(robot_angle),
                     robot_y + arrow_len * np.sin(robot_angle)),
            xytext=(robot_x, robot_y),
            arrowprops=dict(arrowstyle='->', color='#d73027', lw=2.0))
ax.text(robot_x + (arrow_len + 0.15) * np.cos(robot_angle),
        robot_y + (arrow_len + 0.15) * np.sin(robot_angle) + 0.05,
        r'$\theta$', fontsize=11, color='#d73027', va='bottom', ha='center')

                                 
arc_r = 0.62
arc_angles = np.linspace(path_angle, robot_angle, 40)
ax.plot(robot_x + arc_r * np.cos(arc_angles),
        robot_y + arc_r * np.sin(arc_angles),
        color='#7b2d8b', lw=2.0, zorder=4)

                                                               
mid_ang = (path_angle + robot_angle) / 2
ax.text(robot_x + (arc_r + 0.28) * np.cos(mid_ang) - 0.35,
        robot_y + (arc_r + 0.28) * np.sin(mid_ang),
        f'$e_{{\\theta}} = {heading_err_deg}°$', fontsize=10, color='#7b2d8b',
        ha='right', va='center')

ax.set_title('(b) Greška smjera', fontsize=10, pad=7)
ax.set_xlim(0.0, 5.5)
ax.set_ylim(0.0, 3.5)
ax.set_xlabel('x [m]', fontsize=10)
ax.set_ylabel('y [m]', fontsize=10)
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('latex/figures/metrics_concept.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/metrics_concept.png")
