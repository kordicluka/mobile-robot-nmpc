import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7, 7))

                             
res = 0.2
r_obs = 0.6                           
r_robot = 0.2                       
delta_inf = 0.2                        
inflation = r_robot + delta_inf              

cx, cy = 2.0, 2.0                   

                 
x_min, x_max = 0.0, 4.2
y_min, y_max = 0.0, 4.2

xs = np.arange(x_min, x_max + res, res)
ys = np.arange(y_min, y_max + res, res)

                         
for x in xs:
    for y in ys:
        if (x - cx)**2 + (y - cy)**2 <= (r_obs + inflation)**2:
            rect = plt.Rectangle((x - res/2, y - res/2), res, res,
                                  color='lightcoral', alpha=0.6, zorder=1)
            ax.add_patch(rect)

       
for x in np.arange(x_min, x_max + res, res):
    ax.axvline(x, color='gray', linewidth=0.4, alpha=0.5, zorder=2)
for y in np.arange(y_min, y_max + res, res):
    ax.axhline(y, color='gray', linewidth=0.4, alpha=0.5, zorder=2)

                  
obs_circle = Circle((cx, cy), r_obs, color='dimgray', zorder=4, label=f'Prepreka ($r = {r_obs}$ m)')
ax.add_patch(obs_circle)

                                
inf_circle = Circle((cx, cy), r_obs + inflation, fill=False,
                    edgecolor='tomato', linewidth=2.0, linestyle='--',
                    zorder=5, label=f'Proširena zona ($r + {inflation}$ m = $r + 0{{,}}4$ m)')
ax.add_patch(inf_circle)

                              
robot_angle = np.radians(45)
rx = cx + (r_obs + inflation) * np.cos(robot_angle)
ry = cy + (r_obs + inflation) * np.sin(robot_angle)
robot_circle = Circle((rx, ry), r_robot, color='steelblue', alpha=0.8,
                       zorder=6, label=f'Robot ($r_{{rob}} = {r_robot}$ m)')
ax.add_patch(robot_circle)

                                   
ax.annotate('', xy=(cx + r_obs + inflation, cy), xytext=(cx + r_obs, cy),
            arrowprops=dict(arrowstyle='<->', color='tomato', lw=1.5), zorder=7)
ax.text(cx + r_obs + inflation/2, cy + 0.06, f'$r_{{rob}} + \\delta_{{inf}} = 0{{,}}4$ m',
        ha='center', fontsize=9, color='tomato')

ax.annotate('', xy=(cx + r_obs, cy), xytext=(cx, cy),
            arrowprops=dict(arrowstyle='<->', color='dimgray', lw=1.5), zorder=7)
ax.text(cx + r_obs/2, cy - 0.1, f'$r = {r_obs}$ m',
        ha='center', fontsize=9, color='dimgray')

                        
ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax.set_xlim(x_min - res/2, x_max + res/2)
ax.set_ylim(y_min - res/2, y_max + res/2)
ax.set_aspect('equal')
ax.set_xlabel('$x$ [m]', fontsize=11)
ax.set_ylabel('$y$ [m]', fontsize=11)
ax.set_title('Diskretizacija prostora i proširenje prepreke\n'
             '(crvene ćelije su blokirane za A*)', fontsize=11)

                                    
free_patch = mpatches.Patch(facecolor='white', edgecolor='gray', label='Slobodna ćelija')
blocked_patch = mpatches.Patch(facecolor='lightcoral', alpha=0.6, label='Blokirana ćelija')
leg2 = ax.legend(handles=[free_patch, blocked_patch],
                 loc='lower right', fontsize=9, framealpha=0.9)
ax.add_artist(leg2)
ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig('latex/figures/astar_grid.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/astar_grid.png")
