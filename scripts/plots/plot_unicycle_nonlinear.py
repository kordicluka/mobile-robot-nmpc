import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrow

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

                                               
thetas = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
labels = ['$0°$', '$45°$', '$90°$', '$135°$', '$180°$']
colors = ['steelblue', 'mediumseagreen', 'tomato', 'mediumpurple', 'darkorange']

v = 1.0
positions = [(0, 0), (2.5, 1.5), (5, 0), (7.5, 1.5), (10, 0)]

for (px, py), theta, label, color in zip(positions, thetas, labels, colors):
                              
    dx = v * np.cos(theta) * 1.2
    dy = v * np.sin(theta) * 1.2
    ax1.annotate('', xy=(px + dx, py + dy), xytext=(px, py),
                 arrowprops=dict(arrowstyle='->', color=color, lw=2.5))

                  
    circle = plt.Circle((px, py), 0.25, color=color, zorder=5)
    ax1.add_patch(circle)

               
    ax1.text(px, py - 0.7, label, ha='center', fontsize=11, color=color, fontweight='bold')

ax1.set_xlim(-1.5, 11.5)
ax1.set_ylim(-1.5, 3.0)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Isti $v = 1$ m/s, različiti kutovi $\\theta$\n→ potpuno različiti smjerovi kretanja',
              fontsize=11, pad=10)

               
ax1.text(5, 2.6, '$v = 1$ m/s za sve robote', ha='center', fontsize=10,
         style='italic', color='gray')

                                      
theta_range = np.linspace(-np.pi, np.pi, 300)
x_velocity = np.cos(theta_range)       

                                               
linear = 1 - (theta_range**2) * 0                                                
ax2.axhline(y=0, color='gray', linewidth=0.8, linestyle='-', alpha=0.5)
ax2.axvline(x=0, color='gray', linewidth=0.8, linestyle='-', alpha=0.5)

ax2.plot(np.degrees(theta_range), x_velocity, color='tomato', linewidth=2.5,
         label='$v_x = v\\cos\\theta$')

                      
key_thetas = [0, 90, -90, 180, -180]
key_vals = [1, 0, 0, -1, -1]
for t, val in zip(key_thetas, key_vals):
    ax2.plot(t, np.cos(np.radians(t)), 'o', color='tomato', markersize=7, zorder=5)
    if t == 0:
        ax2.annotate(f'  ({t}°, {val})', xy=(t, val), fontsize=9, color='tomato',
                     xytext=(10, val + 0.05))
    elif t == 90:
        ax2.annotate(f'  ({t}°, {val})', xy=(t, val), fontsize=9, color='tomato',
                     xytext=(95, 0.08))
    elif t == -90:
        ax2.annotate(f'({t}°, {val})', xy=(t, val), fontsize=9, color='tomato',
                     xytext=(-135, 0.08))

ax2.set_xlabel('Kut orijentacije $\\theta$ [°]', fontsize=11)
ax2.set_ylabel('x-komponenta brzine $v_x$ [m/s]', fontsize=11)
ax2.set_title('$v_x = v\\cos\\theta$ nije ravna crta\n→ sustav je nelinearan', fontsize=11, pad=10)
ax2.set_xticks([-180, -90, 0, 90, 180])
ax2.set_xticklabels(['-180°', '-90°', '0°', '90°', '180°'])
ax2.legend(fontsize=10, loc='lower center')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(-1.4, 1.4)

plt.tight_layout()
plt.savefig('latex/figures/unicycle_nonlinear.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/unicycle_nonlinear.png")
